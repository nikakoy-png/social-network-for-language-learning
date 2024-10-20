import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {ApiService} from "../../api.service";
import {CookieService} from "ngx-cookie-service";

@Component({
  selector: 'app-resolution-dialog',
  templateUrl: './resolution-dialog.component.html',
  styleUrl: './resolution-dialog.component.scss'
})
export class ResolutionDialogComponent {
  resolutionText: string = '';
  complaint_id!: number;

  constructor(public dialogRef: MatDialogRef<ResolutionDialogComponent>,
              private apiService: ApiService,
              private cookieService: CookieService,
              @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.complaint_id = data.complaint_id;
  }

  Save(): void {
    this.apiService.setResolution(this.cookieService.get("token"), this.complaint_id, this.resolutionText).subscribe(
      (result: any) => {
        console.log('Successful')
        this.dialogRef.close();
      }
    );
  }


  onCancel(): void {
    this.dialogRef.close();
  }
}
