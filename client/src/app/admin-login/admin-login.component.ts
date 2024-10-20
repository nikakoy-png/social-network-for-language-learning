import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {ApiService} from "../../api.service";
import {CookieService} from "ngx-cookie-service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-admin-login',
  templateUrl: './admin-login.component.html',
  styleUrls: ['./admin-login.component.scss']
})
export class AdminLoginComponent implements OnInit {
  loginForm!: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private apiService: ApiService,
    private cookieService: CookieService,
    private router: Router
  ) {
  }

  private saveTokenToCookie(token: string): void {
    this.cookieService.set('token', token);
  }

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]],
    });

  }

  onSubmitLogin(): void {
    if (this.loginForm.valid) {
      const formData = this.loginForm.value;
      this.apiService.login_admin(formData).subscribe(
        (response) => {
          console.log(response);
          this.saveTokenToCookie(response.access);
          this.router.navigate(['/admin/main']);
        },
        (error) => {
          console.error('Error: ', error);
        }
      );
    }
  }
}
