import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

export interface ToastData {
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
}

@Injectable({
  providedIn: 'root',
})
export class ToastService {
  private readonly toastSubject = new Subject<ToastData>();
  toast$ = this.toastSubject.asObservable();

  showToast(
    message: string,
    type: 'success' | 'error' | 'warning' | 'info' = 'info'
  ): void {
    this.toastSubject.next({ message, type });
  }
}
