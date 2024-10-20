import {Component, Inject} from '@angular/core';
import {
  MAT_DIALOG_DATA,
  MatDialogActions,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle
} from "@angular/material/dialog";


@Component({
  selector: 'app-create-complaint',
  templateUrl: './create-complaint.component.html',
  styleUrl: './create-complaint.component.scss'
})
export class CreateComplaintComponent {
  user_id!: number;
  dialog_id!: number;
  description: string = '';

  constructor(
    public dialogRef: MatDialogRef<CreateComplaintComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.user_id = data.user_id;
    this.dialog_id = data.dialog_id;
  }

  saveEdit(): void {
    const editedData = {
      user_id: this.user_id,
      dialog_id: this.dialog_id,
      description: this.description
    };
    this.dialogRef.close(editedData);
  }

  cancelEdit(): void {
    this.dialogRef.close();
  }
}
