import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';
import { HomePageComponent } from './containers/home-page/home-page.component';
import { PdfQuerySectionComponent } from './components/pdf-query-section/pdf-query-section.component';
import { AiQuerySectionComponent } from './components/ai-query-section/ai-query-section.component';
import { UsageStatisticsSectionComponent } from './components/usage-statistics-section/usage-statistics-section.component';
import { FormsModule } from '@angular/forms';
import { LayoutModule } from '../../core/layout/layout.module';

const routes: Routes = [{ path: '', component: HomePageComponent }];

@NgModule({
  declarations: [
    HomePageComponent,
    PdfQuerySectionComponent,
    AiQuerySectionComponent,
    UsageStatisticsSectionComponent,
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    SharedModule,
    LayoutModule,
    FormsModule,
  ],
})
export class HomeModule {}
