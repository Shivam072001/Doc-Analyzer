import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // If you need forms in shared components
import { RouterModule } from '@angular/router';
import { ButtonComponent } from './components/button/button.component';
import { SpinnerComponent } from './components/spinner/spinner.component';
import { ToastComponent } from './components/toast/toast.component';
import { ToastService } from './components/toast/toast.service';
import { MultiSelectDropdownComponent } from './components/multi-select/multi-select.component';
import { SelectComponent } from './components/select/select.component';
import { DocumentService } from './models/services/document.service';

@NgModule({
  declarations: [
    ButtonComponent,
    MultiSelectDropdownComponent,
    SpinnerComponent,
    SelectComponent,
    ToastComponent,
  ],
  imports: [CommonModule, FormsModule, RouterModule],
  exports: [
    CommonModule,
    FormsModule,
    RouterModule,
    ButtonComponent,
    MultiSelectDropdownComponent,
    SpinnerComponent,
    SelectComponent,
    ToastComponent,
  ],
  providers: [ToastService, DocumentService],
})
export class SharedModule {}
