import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {ApiService} from "../../api.service";
import {CookieService} from "ngx-cookie-service";

@Component({
  selector: 'app-admin-create-report',
  templateUrl: './admin-create-report.component.html',
  styleUrl: './admin-create-report.component.scss'
})
export class AdminCreateReportComponent {
  users!: any;
  dialog_id!: number;
  report: string = '';
  recommendation: string = '';
  selectedUser: any;

  constructor(
    public dialogRef: MatDialogRef<AdminCreateReportComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.users = data.users;
  }

  saveEdit(): void {
    const reportData = {
      user_id: this.selectedUser,
      report: this.report,
      recommendation: this.recommendation
    };
    this.dialogRef.close(reportData);
  }

  cancelEdit(): void {
    this.dialogRef.close();
  }
}
