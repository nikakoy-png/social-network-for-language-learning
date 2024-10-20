import {Component} from '@angular/core';
import {Router} from "@angular/router";

@Component({
  selector: 'app-admin-main-menu',
  templateUrl: './admin-main-menu.component.html',
  styleUrl: './admin-main-menu.component.scss'
})
export class AdminMainMenuComponent {
  constructor(
    private router: Router
  ) {
  }

  openUsersList() {
    this.router.navigate(['admin/main/users_list']);
  }

  openComplaints() {
    this.router.navigate(['admin/main/complaints_list']);
  }
}
