import {Component, OnInit} from '@angular/core';
import {CookieService} from "ngx-cookie-service";
import {ApiService} from "../../api.service";
import {ActivatedRoute, Router} from "@angular/router";
import {MatDialog} from "@angular/material/dialog";
import {NoLanguagesUserComponent} from "../no-languages-user/no-languages-user.component";
import {environment} from "../../environments/environment";

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrl: './search.component.scss'
})
export class SearchComponent implements OnInit {
  partners!: any;
  selfUserId!: number;
  loading: boolean = false;

  envGW = environment.apiGateWayUrl;
  constructor(
    private cookieService: CookieService,
    private apiService: ApiService,
    private route: ActivatedRoute,
    private router: Router,
    private dialog: MatDialog
  ) {
  }

  ngOnInit(): void {
    this.loading = false;
    this.apiService.getProfile(this.cookieService.get("token")).subscribe(
      (user: any) => {
        console.log(user)
        this.selfUserId = user.id;
      },
      error => {
        console.error('Error fetching user data:', error);
      }
    );
    this.apiService.GetSuitableUsers(this.cookieService.get("token")).subscribe(
      (listUsers: any) => {
        this.partners = listUsers;
        console.log(this.partners);
        if (this.partners.length == 0) {
          const dialogRef = this.dialog.open(NoLanguagesUserComponent, {
            width: "400px",
          });
          dialogRef.afterClosed().subscribe((result: any) => {
            if (result) {
              console.log(result);
              this.apiService.GetSuitableUsers(this.cookieService.get("token")).subscribe(
                (listUsers: any) => {
                  this.partners = listUsers;
                  this.partners.forEach((user: { photo: string; }) => {
                    user.photo = `${environment.apiGateWayUrl}user_service${user.photo}`;
                  });
                }
              )
            }
          });
        }
        this.loading = true;
      },
      error => {
        console.error('Error fetching user data:', error);
      }
    );
  }


  createDialog(user_id_2: number): void {
    this.apiService.createDialog(this.selfUserId, user_id_2).subscribe(
      (result: any) => {
        console.log(result.dialog_id);
        this.router.navigate(['/main'], { queryParams: { dialogId: result.dialog_id } });
      },
      error => {
        console.error('Error')
      }
    )
  }
}
