import {Component, OnInit} from '@angular/core';
import {ApiService} from "../../api.service";
import {CookieService} from "ngx-cookie-service";
import {MatDialog} from "@angular/material/dialog";
import {ActivatedRoute, Router} from "@angular/router";
import {forkJoin} from "rxjs";
import {environment} from "../../environments/environment";


@Component({
  selector: 'app-admin-list-performance',
  templateUrl: './admin-list-performance.component.html',
  styleUrl: './admin-list-performance.component.scss'
})
export class AdminListPerformanceComponent implements OnInit {
  performances: any;
  isLoaded: boolean = false;
  user: any;

  constructor(
    private apiService: ApiService,
    private cookieService: CookieService,
    private dialog: MatDialog,
    private route: ActivatedRoute,
    private router: Router,
  ) {
  }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      const userId = params['userId'];
      this.apiService.getUserById(userId, this.cookieService.get('token')).subscribe(
        (result: any) => {
          this.user = result;
          console.log(this.user)
        }
      )
      if (userId) {
        this.apiService.getPerformances(this.cookieService.get('token'), userId).subscribe(
          (result: any) => {
            this.performances = result;
            this.performances.forEach((performance: any) => {
              this.apiService.getAdminData(this.cookieService.get('token'), performance.admin).subscribe(
                (result: any) => {
                  performance.admin = result;
                }
              );
            });
            console.log(this.performances)
          },
          error => {
            this.isLoaded = true;
          }
        );
        this.isLoaded = true;
      }
    });
  }

  redirectToUser(): void {
    this.router.navigate(['admin/main/users_list'], {queryParams: {username: this.user.username}});
  }
}
