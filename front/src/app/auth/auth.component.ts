import { Component } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import { ApiService } from "../api.service";
import { CookieService } from "ngx-cookie-service";
import {Router} from "@angular/router";
import {response} from "express";

@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [],
  templateUrl: './auth.component.html',
  styleUrl: './auth.component.scss'
})
export class AuthComponent {
  registrationForm!: FormGroup;
  loginForm!: FormGroup;


  constructor(
    private fromBuilder: FormBuilder,
    private apiService: ApiService,
    private cookieService: CookieService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.registrationForm = this.fromBuilder.group({
      email: ['', Validators.required],
      username: ['', Validators.required, Validators.minLength(7)],
      password: ['', Validators.required],
      password_confirm: ['', Validators.required],
      photo: [null, [Validators.required, this.imageFileValidator]],
      birth_date: ['', Validators.required],
      gender: [''],
      phone: ['', Validators.required],
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
    }, {validators: this.passwordMatchValidator});

    this.loginForm = new FormGroup({
      username: new FormControl(''),
      password: new FormControl(''),
    });
  }

  onSubmitLogin(): void {
    if (this.loginForm.valid) {
      console.log('ok')
      console.log(this.loginForm)
      const formData = this.loginForm.value;

      this.apiService.login(formData).subscribe(
        (response) => {
          console.log(response)
          this.saveTokenToCookie(response.access);
        },
        (error) => {
          console.error('Error: ', error);
        }
      );
    }
  }

  onSubmitRegistration(): void {
    if (this.registrationForm.valid) {
      const formData = this.registrationForm.value;
      const imageFile = formData.photo;
      delete formData.photo;

      this.apiService.register(formData, imageFile).subscribe(
        (response) => {
          this.apiService.login(formData).subscribe(
            (response) => {
              this.saveTokenToCookie(response.access);
            },
            (error) => {
              console.error('Error: ', error);
            }
          );
          // this.router.navigate(['main']);
        },
        (error) => {
          console.log('Error: ', error)
        }
      );
    }
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    this.registrationForm.patchValue({ photo: file });
  }

  private saveTokenToCookie(token: string): void {
    this.cookieService.set('token', token);
  }

  passwordMatchValidator(group: FormGroup) {
    const password = group.get('password')?.value;
    const confirmPassword = group.get('password_confirm')?.value;
    return password === confirmPassword ? null : { passwordMismatch: true };
  }

  imageFileValidator(control: any) {
    const file = control.value;
    return file && file.type.includes('image') ? null : { invalidImage: true };
  }

}
