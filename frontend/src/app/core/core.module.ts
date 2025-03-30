import { NgModule, Optional, SkipSelf } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http'; // We won't use this directly, but Angular might require it
import { ApiService } from './http/services/api.service';
import { AuthGuard } from './auth/guards/auth.guard';
import { AuthService } from './auth/services/auth.service';
import { httpInterceptorProviders } from './http/interceptors';
import { authInterceptorProviders } from './auth/interceptors';
import { LayoutModule } from './layout/layout.module';

@NgModule({
  imports: [CommonModule, HttpClientModule, LayoutModule],
  providers: [
    ApiService,
    AuthService,
    AuthGuard,
    httpInterceptorProviders,
    authInterceptorProviders,
  ],
  exports: [
    LayoutModule, // Export layout module for use in AppModule
  ],
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
