import { Injectable } from '@angular/core';
import { AuthService } from '../services/auth.service';
import axios, { InternalAxiosRequestConfig } from 'axios';

@Injectable()
export class AuthInterceptor {
  constructor(private readonly authService: AuthService) {}

  setupAxiosInterceptors(): void {
    axios.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = this.authService.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );
  }
}
