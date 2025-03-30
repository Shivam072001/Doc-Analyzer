import { Component } from '@angular/core';
import { AuthService } from '../../../auth/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: false,
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent {
  constructor(
    public readonly authService: AuthService,
    private readonly router: Router
  ) {}

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/auth/signin']);
  }

  handleNavigation(event: Event): void {
    // You can add logic here if needed before navigation
    // For now, the routerLink directive in the template will handle navigation
  }

  getUsername(): string | null {
    // Call the getUsername method from the AuthService
    return this.authService.getUsername();
  }
}
