import { Injectable } from '@angular/core';
import axios from 'axios';
import { User } from '../../../shared/models/interfaces/auth.service.interface';
import { AuthResponse } from '../../../shared/models/interfaces/auth.service.interface';
import { environment } from '../../../../environments/environments';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl: string = environment.apiUrl;
  private authTokenKey: string = 'authToken';
  private usernameKey: string = 'loggedInUsername';

  constructor() {}

  async signup(user: User): Promise<AuthResponse> {
    try {
      const response = await axios.post<AuthResponse>(
        `${this.apiUrl}/auth/signup`,
        user
      );
      // Optionally store token or other user info upon signup if your backend returns it
      // localStorage.setItem(this.authTokenKey, response.data.token);
      // If your signup response includes a username, you can store it here as well
      return response.data;
    } catch (error: any) {
      throw error.response ? error.response.data : error;
    }
  }

  async signin(credentials: User): Promise<AuthResponse> {
    try {
      const response = await axios.post<AuthResponse>(
        `${this.apiUrl}/auth/signin`,
        credentials
      );
      if (response.data.status === 'success') {
        localStorage.setItem(this.authTokenKey, response?.data?.token ?? '');
        localStorage.setItem(this.usernameKey, response.data.username ?? '');
      }
      return response.data;
    } catch (error: any) {
      throw error.response ? error.response.data : error;
    }
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem(this.authTokenKey);
  }

  logout(): void {
    localStorage.removeItem(this.authTokenKey);
    localStorage.removeItem(this.usernameKey);
  }

  getToken(): string | null {
    return localStorage.getItem(this.authTokenKey);
  }

  getUsername(): string | null {
    return localStorage.getItem(this.usernameKey);
  }

  setLoggedInUsername(username: string): void {
    localStorage.setItem(this.usernameKey, username);
  }
}
