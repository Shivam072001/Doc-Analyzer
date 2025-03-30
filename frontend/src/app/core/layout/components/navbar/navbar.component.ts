import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: false,
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent {
  constructor(private router: Router) {}

  handleNavigation(event: Event): void {
    // You can add logic here if needed before navigation
    // For now, the routerLink directive in the template will handle navigation
  }
}
