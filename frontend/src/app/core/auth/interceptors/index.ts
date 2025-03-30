import { HTTP_INTERCEPTORS } from '@angular/common/http';
// Add your authentication interceptors here (e.g., for adding JWT tokens)

export const authInterceptorProviders = [
  // { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
];
