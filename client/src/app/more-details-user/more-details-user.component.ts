import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {Route, Router} from "@angular/router";
import {ApiService} from "../../api.service";
import {CookieService} from "ngx-cookie-service";

@Component({
  selector: 'app-more-details-user',
  templateUrl: './more-details-user.component.html',
  styleUrls: ['./more-details-user.component.scss']
})
export class MoreDetailsUserComponent {
  msg: any;
  performances: any;
  userId: number;
  is_active: boolean;

  constructor(
    public dialogRef: MatDialogRef<MoreDetailsUserComponent>,
    private router: Router,
    private cookieService: CookieService,
    private apiService: ApiService,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.msg = data.msg;
    this.performances = data.performance;
    this.userId = data.user_id;
    this.is_active = data.user_active_status;
    console.log(this.is_active)
  }

  closeModal(): void {
    this.dialogRef.close();
  }

  openComplaints(): void {
    this.router.navigate(['admin/main/complaints_list'], {queryParams: {userId: this.userId}});
    this.dialogRef.close();
  }

  openDialogs(): void {
    this.router.navigate(['admin/main/user_dialogs'], {queryParams: {userId: this.userId}});
    this.dialogRef.close();
  }

  openActiveDialogs(): void {
    this.router.navigate(['admin/main/user_dialogs'], {queryParams: {userId: this.userId, is_active: true}});
    this.dialogRef.close();
  }

  openPerformance(): void {
    this.router.navigate(['admin/main/user_performances'], {queryParams: {userId: this.userId}});
    this.dialogRef.close();
  }

  changeStatus(): void {
    this.apiService.updateActiveStatus(this.cookieService.get("token"), this.userId).subscribe(
      (result: any) => {
        console.log(result)
          this.is_active = !this.is_active;

      }
    )
  }
}
