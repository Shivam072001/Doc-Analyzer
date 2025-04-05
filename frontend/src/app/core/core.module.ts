import { NgModule, Optional, SkipSelf } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from './http/services/api.service';
import { AuthGuard } from './auth/guards/auth.guard';
import { AuthService } from './auth/services/auth.service';
import { LayoutModule } from './layout/layout.module';

@NgModule({
  imports: [CommonModule, LayoutModule],
  providers: [
    ApiService,
    AuthService,
    AuthGuard,
  ],
  exports: [LayoutModule],
})
export class CoreModule {
  constructor(@Optional() @SkipSelf() parentModule: CoreModule) {
    if (parentModule) {
      throw new Error(
        'CoreModule is already loaded. Import it in the AppModule only.'
      );
    }
  }
}
