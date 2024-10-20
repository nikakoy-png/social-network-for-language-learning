import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../api.service';
import {CookieService} from 'ngx-cookie-service';
import {MatDialog} from '@angular/material/dialog';
import {ActivatedRoute, Router} from '@angular/router';
import {forkJoin} from 'rxjs';
import {environment} from '../../environments/environment';

@Component({
  selector: 'app-admin-list-dialogs-users',
  templateUrl: './admin-list-dialogs-users.component.html',
  styleUrls: ['./admin-list-dialogs-users.component.scss']
})
export class AdminListDialogsUsersComponent implements OnInit {
  dialogs: any;
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
        this.apiService.getListDialogsUserForAdmin(this.cookieService.get('token'), userId).subscribe(
          (result: any) => {
            this.dialogs = result;
            const requests = this.dialogs.map((dialog: any) => {
              return this.apiService.getDetailsDialogs(this.cookieService.get('token'), dialog.dialog);
            });
            forkJoin(requests).subscribe(
              (detailsResults: any) => {
                detailsResults.forEach((details: any, index: number) => {
                  this.dialogs[index].details = details;
                  this.dialogs[index].details.users.forEach((user: any) => {
                    user.photo = `${environment.apiGateWayUrl}user_service${user.photo}`;
                  });
                });
                this.isLoaded = true;
              }
            );
          }
        );
      }
    });
  }

  commonLanguages(user1Languages: any[], user2Languages: any[]): any[] {
    console.log(user1Languages.filter(lang1 =>
      user2Languages.some(lang2 => lang1.language.id === lang2.language.id)
    ))
    return user1Languages.filter(lang1 =>
      user2Languages.some(lang2 => lang1.language.id === lang2.language.id)
    );
  }

  redirectToDialogMessages(dialogId: number): void {
    this.router.navigate(['admin/main/user_dialog_messages'], {queryParams: {dialogId: dialogId}});
  }
}
