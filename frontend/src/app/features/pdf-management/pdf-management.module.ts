import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';
import { PdfManagementPageComponent } from './containers/pdf-management-page/pdf-management.component';
import { PdfUploadComponent } from './components/pdf-upload/pdf-upload.component';
import { PdfListComponent } from './components/pdf-list/pdf-list.component';
import { PdfStatisticsComponent } from './components/pdf-statistics/pdf-statistics.component';
import { FormsModule } from '@angular/forms';
import { LayoutModule } from '../../core/layout/layout.module';

const routes: Routes = [{ path: '', component: PdfManagementPageComponent }];

@NgModule({
  declarations: [
    PdfManagementPageComponent,
    PdfUploadComponent,
    PdfListComponent,
    PdfStatisticsComponent,
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    SharedModule,
    LayoutModule,
    FormsModule,
  ],
})
export class PdfManagementModule {}
