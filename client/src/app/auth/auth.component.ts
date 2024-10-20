import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../../api.service';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';
import { format } from 'date-fns';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.scss']
})
export class AuthComponent implements OnInit {
  registrationForm!: FormGroup;
  loginForm!: FormGroup;
  isRegisterFormVisible = true;

  constructor(
    private formBuilder: FormBuilder,
    private apiService: ApiService,
    private cookieService: CookieService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.registrationForm = this.formBuilder.group(
      {
        email: ['', [Validators.required]],
        username: ['', [Validators.required, Validators.minLength(7)]],
        password: ['', [Validators.required]],
        password_confirm: ['', [Validators.required]],
        photo: [null, [Validators.required]],
        birth_date: ['', [Validators.required]],
        gender: [''],
        phone: ['', [Validators.required]],
        first_name: ['', [Validators.required]],
        last_name: ['', [Validators.required]]
      },
      { validators: this.passwordMatchValidator }
    );

    this.loginForm = this.formBuilder.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });
  }

  onSubmitLogin(): void {
    if (this.loginForm.valid) {
      const formData = this.loginForm.value;
      this.apiService.login(formData).subscribe(
        (response) => {
          console.log(response);
          this.saveTokenToCookie(response.access);
          this.router.navigate(['/main']);
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

      // Преобразуем дату в нужный формат YYYY-MM-DD
      if (formData.birth_date) {
        try {
          formData.birth_date = format(new Date(formData.birth_date), 'yyyy-MM-dd');
          console.log('Formatted birth_date:', formData.birth_date);
        } catch (error) {
          console.error('Error formatting date: ', error);
          return;
        }
      }

      this.apiService.register(formData, imageFile).subscribe(
        (response) => {
          this.apiService.login(formData).subscribe(
            (response) => {
              this.saveTokenToCookie(response.access);
              this.router.navigate(['/main']);
            },
            (error) => {
              console.error('Error: ', error);
            }
          );
        },
        (error) => {
          console.log('Error: ', error);
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

  toggleForm(event: Event): void {
    event.preventDefault();
    this.isRegisterFormVisible = !this.isRegisterFormVisible;
  }
}
