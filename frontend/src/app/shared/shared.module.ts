import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // If you need forms in shared components
import { RouterModule } from '@angular/router';
import { ButtonComponent } from './components/button/button.component';
import { SpinnerComponent } from './components/spinner/spinner.component';
import { ToastComponent } from './components/toast/toast.component';
import { ToastService } from './components/toast/toast.service';

@NgModule({
  declarations: [ButtonComponent, SpinnerComponent, ToastComponent],
  imports: [CommonModule, FormsModule, RouterModule],
  exports: [
    CommonModule,
    FormsModule,
    RouterModule,
    ButtonComponent,
    SpinnerComponent,
    ToastComponent,
  ],
  providers: [ToastService],
})
export class SharedModule {}
