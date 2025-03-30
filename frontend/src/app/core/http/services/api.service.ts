import { Injectable } from '@angular/core';
import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { environment } from '../../../../environments/environments';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private axiosClient: AxiosInstance;
  private readonly API_BASE_URL = environment.apiUrl; // Assuming you'll configure this

  constructor() {
    this.axiosClient = axios.create({
      baseURL: this.API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async get<T>(url: string, params?: any): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.axiosClient.get(url, {
        params,
      });
      return response.data;
    } catch (error: any) {
      console.error('GET request failed', error);
      throw error;
    }
  }

  async post<T>(url: string, data?: any): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.axiosClient.post(url, data);
      return response.data;
    } catch (error: any) {
      console.error('POST request failed', error);
      throw error;
    }
  }

  async put<T>(url: string, data?: any): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.axiosClient.put(url, data);
      return response.data;
    } catch (error: any) {
      console.error('PUT request failed', error);
      throw error;
    }
  }

  async delete<T>(url: string, params?: any): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.axiosClient.delete(url, {
        params,
      });
      return response.data;
    } catch (error: any) {
      console.error('DELETE request failed', error);
      throw error;
    }
  }

  async postFormData<T>(url: string, formData: FormData): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.axiosClient.post(
        url,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      return response.data;
    } catch (error: any) {
      console.error('POST FormData request failed', error);
      throw error;
    }
  }
}
