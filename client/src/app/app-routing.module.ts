import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {AuthComponent} from "./auth/auth.component";
import {MainComponent} from "./main/main.component";
import {SearchComponent} from "./search/search.component";
import {ProfileComponent} from "./profile/profile.component";
import {AdminLoginComponent} from "./admin-login/admin-login.component";
import {AdminMainMenuComponent} from "./admin-main-menu/admin-main-menu.component";
import {AdminUsersComponent} from "./admin-users/admin-users.component";
import {ComplaintsComponent} from "./complaints/complaints.component";
import {AdminListDialogsUsersComponent} from "./admin-list-dialogs-users/admin-list-dialogs-users.component";
import {AdminUserDialogComponent} from "./admin-user-dialog/admin-user-dialog.component";
import {AdminListPerformanceComponent} from "./admin-list-performance/admin-list-performance.component";


const routes: Routes = [
  {path: 'auth', component: AuthComponent},
  {path: '', component: AuthComponent},
  {path: 'main', component: MainComponent},
  {path: 'search', component: SearchComponent},
  {path: 'profile', component: ProfileComponent},
  {path: 'admin/auth', component: AdminLoginComponent},
  {path: 'admin/main', component: AdminMainMenuComponent},
  {path: 'admin/main/users_list', component: AdminUsersComponent},
  {path: 'admin/main/complaints_list', component: ComplaintsComponent},
  {path: 'admin/main/user_dialogs', component: AdminListDialogsUsersComponent},
  {path: 'admin/main/user_dialog_messages', component: AdminUserDialogComponent},
  {path: 'admin/main/user_performances', component: AdminListPerformanceComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
