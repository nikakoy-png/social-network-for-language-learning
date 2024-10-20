import {Component, Inject} from '@angular/core';
import {MatButton} from "@angular/material/button";
import {
  MAT_DIALOG_DATA,
  MatDialogActions,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle
} from "@angular/material/dialog";
import {MatError, MatFormField, MatLabel} from "@angular/material/form-field";
import {MatInput} from "@angular/material/input";
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {MatOption, MatSelect} from "@angular/material/select";
import {NgForOf, NgIf} from "@angular/common";
import {MatCheckbox} from "@angular/material/checkbox";
import {CookieService} from "ngx-cookie-service";
import {ApiService} from "../../api.service";
import {EditMessageDialogComponent} from "../edit-message-dialog/edit-message-dialog.component";

@Component({
  selector: 'app-no-languages-user',
  templateUrl: './no-languages-user.component.html',
  styleUrl: './no-languages-user.component.scss'
})
export class NoLanguagesUserComponent {
  listProficiencyLevels = [
    {title: 'A1'},
    {title: 'A2'},
    {title: 'B1'},
    {title: 'B2'},
    {title: 'C1'},
    {title: 'C2'}
  ];
  languageForm!: FormGroup;
  listLanguages!: any;


  constructor(
    public dialogRef: MatDialogRef<EditMessageDialogComponent>,
    private cookieService: CookieService,
    private apiService: ApiService,
    private formBuilder: FormBuilder,
    @Inject(MAT_DIALOG_DATA) public data: { dialogRef: MatDialogRef<NoLanguagesUserComponent> }
  ) {
    this.languageForm = this.formBuilder.group({
      language: ['', Validators.required],
      proficiencyLevel: ['', Validators.required],
      learning: false
    });
    this.apiService.getListLanguages(this.cookieService.get('token')).subscribe(
      (result: any) => {
        console.log(result);
        this.listLanguages = result;
      }
    );
  }

  addLanguage() {
    if (this.languageForm.valid) {
      const newLanguageForBack = {
        language: this.languageForm.value.language,
        proficiency_level: this.languageForm.value.proficiencyLevel,
        is_learning: this.languageForm.value.learning,
      };
      this.apiService.addLanguageUser(this.cookieService.get('token'), newLanguageForBack).subscribe(
        (result: any) => {
          console.log(result);
          this.dialogRef.close(true);
        },
        error => {
          console.log(error);
          this.dialogRef.close(false);
        }
      );
      this.languageForm.reset();
    } else {
      this.languageForm.markAllAsTouched();
    }
    this.dialogRef.close(true);
  }
}
