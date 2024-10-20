import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-edit-message-dialog',
  templateUrl: './edit-message-dialog.component.html',
  styleUrls: ['./edit-message-dialog.component.scss']
})
export class EditMessageDialogComponent {
  editedMessage: string = '';
  description: string = '';

  constructor(
    public dialogRef: MatDialogRef<EditMessageDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.editedMessage = data.messageText;
  }

  saveEdit(): void {
    const editedData = {
      editedMessage: this.editedMessage,
      editedDescription: this.description
    };
    this.dialogRef.close(editedData);
  }

  cancelEdit(): void {
    this.dialogRef.close();
  }
}
