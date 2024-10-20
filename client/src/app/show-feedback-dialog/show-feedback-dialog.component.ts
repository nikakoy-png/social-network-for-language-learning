import {Component, Inject} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {MatButton} from "@angular/material/button";
import {
  MAT_DIALOG_DATA,
  MatDialogActions,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle
} from "@angular/material/dialog";
import {MatFormField} from "@angular/material/form-field";
import {MatInput} from "@angular/material/input";

@Component({
  selector: 'app-show-feedback-dialog',
  templateUrl: './show-feedback-dialog.component.html',
  styleUrl: './show-feedback-dialog.component.scss'
})
export class ShowFeedbackDialogComponent {
  editedMessage: string = '';
  description: string = '';

  constructor(
    public dialogRef: MatDialogRef<ShowFeedbackDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.editedMessage = data.messageText;
    this.description = data.description;
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
