import { Component, OnDestroy } from '@angular/core';
import { ToastService } from './toast.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-toast',
  standalone: false,
  templateUrl: './toast.component.html',
  styleUrls: ['./toast.component.scss'],
})
export class ToastComponent implements OnDestroy {
  message: string = '';
  type: 'success' | 'error' | 'warning' | 'info' = 'info';
  isVisible: boolean = false;
  private toastSubscription: Subscription;

  constructor(private readonly toastService: ToastService) {
    this.toastSubscription = this.toastService.toast$.subscribe((toast) => {
      this.message = toast.message;
      this.type = toast.type;
      this.isVisible = true;
      setTimeout(() => {
        this.isVisible = false;
      }, 3000); // Adjust timeout as needed
    });
  }

  ngOnDestroy(): void {
    this.toastSubscription.unsubscribe();
  }
}
