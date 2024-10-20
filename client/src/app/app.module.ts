import {NgModule} from '@angular/core';
import {BrowserModule, provideClientHydration} from '@angular/platform-browser';

import {AppComponent} from './app.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {AuthComponent} from "./auth/auth.component";
import {AppRoutingModule} from "./app-routing.module";
import {RouterModule} from "@angular/router";
import {MainComponent} from "./main/main.component";
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import {MatSelectModule} from "@angular/material/select";
import {MatCheckboxModule} from "@angular/material/checkbox";
import {MatIconModule} from "@angular/material/icon";
import {MatButtonModule} from "@angular/material/button";
import {SearchComponent} from "./search/search.component";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {MatDialogModule} from "@angular/material/dialog";
import {EditMessageDialogComponent} from "./edit-message-dialog/edit-message-dialog.component";
import {ShowFeedbackDialogComponent} from "./show-feedback-dialog/show-feedback-dialog.component";
import {CreateComplaintComponent} from "./create-complaint/create-complaint.component";
import {TopBarComponent} from "./top-bar/top-bar.component";
import {ProfileComponent} from "./profile/profile.component";
import {NoLanguagesUserComponent} from "./no-languages-user/no-languages-user.component";
import {LoaderComponent} from "./loader/loader.component";
import {AdminLoginComponent} from "./admin-login/admin-login.component";
import {AdminMainMenuComponent} from "./admin-main-menu/admin-main-menu.component";
import {AdminUsersComponent} from "./admin-users/admin-users.component";
import {MoreDetailsUserComponent} from "./more-details-user/more-details-user.component";
import {ComplaintsComponent} from "./complaints/complaints.component";
import {AdminListDialogsUsersComponent} from "./admin-list-dialogs-users/admin-list-dialogs-users.component";
import {AdminUserDialogComponent} from "./admin-user-dialog/admin-user-dialog.component";
import {AdminCreateReportComponent} from "./admin-create-report/admin-create-report.component";
import {AdminListPerformanceComponent} from "./admin-list-performance/admin-list-performance.component";
import {DatePipe} from "@angular/common";
import {ResolutionDialogComponent} from "./resolution-dialog/resolution-dialog.component";


@NgModule({
  declarations: [
    AppComponent,
    AuthComponent,
    MainComponent,
    SearchComponent,
    EditMessageDialogComponent,
    ShowFeedbackDialogComponent,
    CreateComplaintComponent,
    TopBarComponent,
    ProfileComponent,
    NoLanguagesUserComponent,
    LoaderComponent,
    AdminLoginComponent,
    AdminMainMenuComponent,
    AdminUsersComponent,
    MoreDetailsUserComponent,
    ComplaintsComponent,
    AdminListDialogsUsersComponent,
    AdminUserDialogComponent,
    AdminCreateReportComponent,
    AdminListPerformanceComponent,
    ResolutionDialogComponent
  ],
  imports: [
    BrowserModule,
    DatePipe,
    HttpClientModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    FormsModule,
    AppRoutingModule,
    MatSelectModule,
    MatCheckboxModule,
    MatIconModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatDialogModule,
  ],
  providers: [
    provideAnimationsAsync()
  ],
  exports: [
    TopBarComponent,
    LoaderComponent
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
