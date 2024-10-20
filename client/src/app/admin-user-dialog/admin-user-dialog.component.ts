import {Component, OnInit} from '@angular/core';
import {CookieService} from "ngx-cookie-service";
import {ApiService} from "../../api.service";
import {MatDialog} from "@angular/material/dialog";
import {ActivatedRoute, Router} from "@angular/router";
import {ShowFeedbackDialogComponent} from "../show-feedback-dialog/show-feedback-dialog.component";
import {environment} from "../../environments/environment";
import {EditMessageDialogComponent} from "../edit-message-dialog/edit-message-dialog.component";
import {AdminCreateReportComponent} from "../admin-create-report/admin-create-report.component";

@Component({
  selector: 'app-admin-user-dialog',
  templateUrl: './admin-user-dialog.component.html',
  styleUrl: './admin-user-dialog.component.scss'
})
export class AdminUserDialogComponent implements OnInit {
  messages: any;
  isLoaded: boolean = false;
  UserId!: string;
  users: any;

  constructor(
    private cookieService: CookieService,
    private apiService: ApiService,
    private dialog: MatDialog,
    private route: ActivatedRoute,
    private router: Router,
  ) {
  }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      const dialogId = params['dialogId'];
      if (dialogId) {
        this.apiService.getListMessagesUserForAdmin(this.cookieService.get("token"), dialogId).subscribe(
          (result: any) => {
            this.messages = result.messages;
            console.log(result);
            this.users = result.users;
            this.users.forEach((user: any) => {
              user.photo = `${environment.apiGateWayUrl}user_service${user.photo}`;
            });
            this.UserId = this.users[1].id;
            this.isLoaded = true;
          }
        )
      }
    });
  }

  openCreatePerformance(): void {
    const dialogRef = this.dialog.open(AdminCreateReportComponent, {
      width: '400px',
      data: {users: this.users}
    });

    dialogRef.afterClosed().subscribe((result: any) => {
      if (result) {
        const performanceData = {
          user_id: result.user_id,
          report: result.report,
          recommendation: result.recommendation
        };
        console.log(performanceData);
        this.apiService.addPerformance(this.cookieService.get("token"), performanceData).subscribe(
          (result: any) => {
            console.log(result);
          },
          error => {
            console.error('Error fetching user data:', error);
          }
        );
      }
    });
  }

  openShowDialog(messageText: string, description: string): void {
    this.dialog.open(ShowFeedbackDialogComponent, {
      width: '400px',
      data: {messageText: messageText, description: description}
    });
  }

  getMessageClasses(messageSenderId: string): string {
    return messageSenderId === this.UserId ? 'outgoing' : 'incoming';
  }

  redirectToUser(username: string): void {
    this.router.navigate(['admin/main/users_list'], {queryParams: {username: username}});
  }
}
