import {Component, OnInit} from '@angular/core';
import {CookieService} from "ngx-cookie-service";
import {ApiService} from "../../api.service";
import {environment} from "../../environments/environment";


@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrl: './top-bar.component.scss'
})
export class TopBarComponent implements OnInit {
  selfUser!: any;
  isShow: boolean = false;

  constructor(
    private cookieService: CookieService,
    private apiService: ApiService,
  ) {
  }

  ngOnInit(): void {
    if (!this.cookieService.get("token")) {
      return
    }
    this.apiService.getProfile(this.cookieService.get("token")).subscribe(
      (user: any) => {
        console.log(user)
        this.selfUser = user;
        if (!this.selfUser) {
          return
        }
        this.isShow = true;
        this.selfUser.photo = `${environment.apiGateWayUrl}user_service${this.selfUser.photo}`;
      },
      error => {
        console.error('Error fetching user data:', error);
        this.isShow = false;
      }
    );
  }
}
