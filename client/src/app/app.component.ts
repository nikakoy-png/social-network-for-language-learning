import {Component} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {RouterModule} from '@angular/router';
import {AuthComponent} from "./auth/auth.component";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'client';
}
