import {Component, OnInit, EventEmitter, Output} from '@angular/core';
import {ApiService} from "../../api.service";
import {CookieService} from "ngx-cookie-service";
import {environment} from "../../environments/environment";
import {MatDialog} from "@angular/material/dialog";
import {MoreDetailsUserComponent} from "../more-details-user/more-details-user.component";
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-admin-users',
  templateUrl: './admin-users.component.html',
  styleUrls: ['./admin-users.component.scss']
})
export class AdminUsersComponent implements OnInit {
  users: any[] = [];
  currentPage: number = 1;
  pageSize: number = 10;
  searchTerm: string = '';
  isLoaded: boolean = false;

  constructor(
    private apiService: ApiService,
    private cookieService: CookieService,
    private dialog: MatDialog,
    private router: Router,
    private route: ActivatedRoute,
  ) {
  }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      const username = params['username'];
      if (username) {
        this.searchTerm = username;
        this.searchUsers()
      } else {
        this.loadUsers();

      }
      return;
    });
  }

  openModal(user_id: number, is_active: boolean): void {
    this.apiService.getStatisticUserForAdmin(this.cookieService.get('token'), user_id).subscribe(
      (result: any) => {
        this.apiService.getCountPerformances(this.cookieService.get('token'), user_id).subscribe(
          (result_per: any) => {
            const dialogRef = this.dialog.open(MoreDetailsUserComponent, {
              width: '400px',
              data: {msg: result.data, performance: result_per, user_id: user_id, user_active_status: is_active}
            });
          }
        );
      }
    );
  }

  loadUsers(): void {
    this.apiService.getListUsersForAdmin(this.cookieService.get('token'), this.currentPage, this.pageSize).subscribe(
      (response: any) => {
        if (Array.isArray(response.data)) {
          this.users = response.data.map((user: any) => {
            return {...user, photo: `${environment.apiGateWayUrl}user_service${user.photo}`};
          });
          this.isLoaded = true;
        } else {
          console.error('Invalid response from getListUsersForAdmin API:', response);
        }
      },
      error => {
        console.error('Error fetching users:', error);
      }
    );
  }

  onPageChange(page: number): void {
    this.currentPage = page;
    this.isLoaded = false;
    this.loadUsers();
  }

  searchUsers(): void {
    this.isLoaded = false;
    this.apiService.getUserForAdminUsername(this.cookieService.get('token'), this.searchTerm)
      .subscribe((response: any) => {
        console.log(response)
        this.users = response;
        this.users = this.users.map((user: any) => {
          return {...user, photo: `${environment.apiGateWayUrl}user_service${user.photo}`};
        });
        console.log(this.users)
        this.isLoaded = true;
      }, error => {
        console.error('Error fetching user:', error);
        this.isLoaded = true;
      });
  }

  redirectToDialogMessages(dialogId: number): void {
    this.router.navigate(['admin/main/user_dialog_messages'], {queryParams: {dialogId: dialogId}});
  }
}
