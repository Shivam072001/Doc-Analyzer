import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { NavbarComponent } from './components/navbar/navbar.component';

@NgModule({
  declarations: [HeaderComponent, FooterComponent, NavbarComponent],
  imports: [CommonModule, RouterModule],
  exports: [HeaderComponent, FooterComponent, NavbarComponent],
})
export class LayoutModule {}
