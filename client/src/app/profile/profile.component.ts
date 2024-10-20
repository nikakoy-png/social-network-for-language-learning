import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {CookieService} from 'ngx-cookie-service';
import {ApiService} from '../../api.service';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {environment} from "../../environments/environment";

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>; // Объявление переменной fileInput
  fileInputVisible = true;

  openFileInput(): void {
    if (this.fileInput) {
      this.fileInput.nativeElement.click();
    } else {
      console.error('File input not found.');
    }
  }

  environmentApiGateWayUrl = environment.apiGateWayUrl
  userData: any;
  originalData: any;
  languageForm!: FormGroup;
  listLanguages!: any;
  loading: boolean = false;

  listProficiencyLevels = [
    {title: 'A1'},
    {title: 'A2'},
    {title: 'B1'},
    {title: 'B2'},
    {title: 'C1'},
    {title: 'C2'}
  ];

  constructor(private cookieService: CookieService,
              private apiService: ApiService,
              private formBuilder: FormBuilder) {
  }

  onFileSelected(event: any): void {
    const file: File = event.target.files[0];
    if (file) {
      this.uploadFile(file);
    }
  }


  ngOnInit(): void {
    this.loading = false;
    this.languageForm = this.formBuilder.group({
      language: ['', Validators.required],
      proficiencyLevel: ['', Validators.required],
      learning: false
    });

    this.apiService.getProfile(this.cookieService.get('token')).subscribe(
      (user: any) => {
        console.log(user);
        this.userData = user;
        this.originalData = {...this.userData};
        this.userData.photo = `${this.environmentApiGateWayUrl}user_service${this.userData.photo}`;
      },
      error => {
        console.error('Error fetching user data:', error);
      }
    );

    this.apiService.getListLanguages(this.cookieService.get('token')).subscribe(
      (result: any) => {
        console.log(result);
        this.listLanguages = result;
      }
    );
    this.loading = true;
  }

  isDataChanged(): boolean {
    if (!this.userData || !this.originalData) {
      return true;
    }
    return JSON.stringify(this.userData) !== JSON.stringify(this.originalData);
  }

  saveChanges() {
    this.originalData = {...this.userData};
    this.apiService.updateDataUserProfile(this.cookieService.get('token'), this.userData).subscribe(
      (result: any) => {
        console.log(result);
      },
      error => {
        console.error('Error fetching user data:', error);
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
      console.log(newLanguageForBack);
      this.userData.languages.push(newLanguageForBack);
      this.apiService.addLanguageUser(this.cookieService.get('token'), newLanguageForBack).subscribe(
        (result: any) => {
          console.log(result);
        },
        error => {
          console.log(error);
        }
      );

      this.languageForm.reset();
    } else {
      this.languageForm.markAllAsTouched();
    }
  }

  removeLanguage(index: number, language_id: number) {
    this.userData.languages.splice(index, 1);
    this.apiService.deleteLanguageUser(this.cookieService.get('token'), language_id).subscribe(
      (result) => {
        console.log(result);
      },
      error => {
        console.log(error);
      }
    );
  }

  uploadFile(file: File): void {
    const formData = new FormData();
    formData.append('file', file);


        console.log(324234)

    this.apiService.updPhotoProfileUser(this.cookieService.get('token'), formData).subscribe(
      (result: any) => {
        console.log(result);
      },
      error => {

        console.log(error)
      });
  }
}
