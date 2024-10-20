import {Component, OnInit} from '@angular/core';
import {ApiService} from "../../api.service";
import {CookieService} from "ngx-cookie-service";
import {MoreDetailsUserComponent} from "../more-details-user/more-details-user.component";
import {MatDialog} from "@angular/material/dialog";
import {environment} from "../../environments/environment";
import {forkJoin} from "rxjs";
import {ActivatedRoute, Router} from "@angular/router";
import {enUS} from 'date-fns/locale'; // для локализации на русский язык
import { format } from 'date-fns';
import {ResolutionDialogComponent} from "../resolution-dialog/resolution-dialog.component";

@Component({
  selector: 'app-complaints',
  templateUrl: './complaints.component.html',
  styleUrl: './complaints.component.scss'
})
export class ComplaintsComponent implements OnInit {
  complaints!: any;
  is_answer: boolean = false;
  page_number: number = 1;
  page_size: number = 10
  isLoaded: boolean = false
  searchTerm: string = '';
  currentPage: number = 1;

  constructor(
    private apiService: ApiService,
    private cookieService: CookieService,
    private dialog: MatDialog,
    private route: ActivatedRoute,
    private router: Router,
  ) {
  }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      const userId = params['userId'];
      if (userId) {
        this.apiService.getComplaintsByUserID(this.cookieService.get('token'), userId, this.is_answer).subscribe(
          (result: any) => {
            this.complaints = result;
            const requests = this.complaints.map((complaint: any) => {
              return this.apiService.getDetailsDialogs(this.cookieService.get('token'), complaint.dialog);
            });
            forkJoin(requests).subscribe(
              (detailsResults: any) => {
                detailsResults.forEach((details: any, index: number) => {
                  this.complaints[index].details = details;
                  this.transformComplaintDates(this.complaints[index]);
                });
                this.isLoaded = true;
                console.log(this.complaints);
              }
            );
          }
        );
        return;
      }
    });
    this.loadComplaints();

  }

  onPageChange(page: number): void {
    this.currentPage = page;
    this.isLoaded = false;
    this.loadComplaints();
  }

  loadComplaints(): void {
    this.apiService.getComplaints(this.cookieService.get('token'), this.page_number, this.page_size, this.is_answer).subscribe(
      (result: any) => {
        this.complaints = result;
        const requests = this.complaints.map((complaint: any) => {
          return this.apiService.getDetailsDialogs(this.cookieService.get('token'), complaint.dialog);
        });
        forkJoin(requests).subscribe(
          (detailsResults: any) => {
            detailsResults.forEach((details: any, index: number) => {
              this.complaints[index].details = details;
              this.transformComplaintDates(this.complaints[index]);
            });
            this.isLoaded = true;
            console.log(this.complaints);
          }
        );
      }
    );
  }

  openModal(dialogId: number): void {
    this.router.navigate(['admin/main/user_dialog_messages'], {queryParams: {dialogId: dialogId}});
  }

  transformComplaintDates(complaint: any): void {
    complaint.created_at = this.transformDate(complaint.created_at);
    complaint.details.dialog.created_at = this.transformDate(complaint.details.dialog.created_at);
    complaint.details.dialog.end_date = complaint.details.dialog.end_date ? this.transformDate(complaint.details.dialog.end_date) : '';
    complaint.details.dialog.last_activity = this.transformDate(complaint.details.dialog.last_activity);
  }

  transformDate(date: string): string {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric',
      second: 'numeric'
    }).format(new Date(date));
  }

  openResolutionDialog(complaint: any): void {
    const dialogRef = this.dialog.open(ResolutionDialogComponent, {
      width: '300px',
      data: { complaint, "complaint_id":  complaint.id}
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        console.log('Resolution submitted:', result);
        complaint.resolution = result;
        this.loadComplaints();
      }
    });
  }

  searchComplaints(): void {
    this.isLoaded = false;
    this.apiService.getComplaintsByUserID(this.cookieService.get('token'), this.searchTerm, this.is_answer).subscribe(
      (result: any) => {
        this.complaints = result;
        const requests = this.complaints.map((complaint: any) => {
          return this.apiService.getDetailsDialogs(this.cookieService.get('token'), complaint.dialog);
        });
        forkJoin(requests).subscribe(
          (detailsResults: any) => {
            detailsResults.forEach((details: any, index: number) => {
              this.complaints[index].details = details;
            });
            this.isLoaded = true;
            console.log(this.complaints);
          }
        );
      }
    )
  }
  changeStatus(user: any): void {
    console.log(user)
    this.apiService.updateActiveStatus(this.cookieService.get("token"), user.id).subscribe(
      (result: any) => {
        console.log(result)
          user.is_active = !user.is_active;

      }
    )
  }
}
