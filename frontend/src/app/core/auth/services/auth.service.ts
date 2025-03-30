import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  isAuthenticated$: Observable<boolean> =
    this.isAuthenticatedSubject.asObservable();

  // Example methods - implement your actual authentication logic
  login(): void {
    this.isAuthenticatedSubject.next(true);
    // Store token or user info
  }

  logout(): void {
    this.isAuthenticatedSubject.next(false);
    // Clear token or user info
  }

  getAuthToken(): string | null {
    // Retrieve authentication token from storage
    return null;
  }
}
