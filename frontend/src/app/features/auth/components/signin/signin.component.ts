import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '../../../../core/auth/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signin',
  standalone: false,
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.scss'],
})
export class SigninComponent implements OnInit {
  signinForm: FormGroup;
  errorMessage: string = '';

  constructor(
    private readonly fb: FormBuilder,
    private readonly authService: AuthService,
    private readonly router: Router
  ) {
    this.signinForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]],
    });
  }

  ngOnInit(): void {}

  async onSubmit(): Promise<void> {
    if (this.signinForm.valid) {
      try {
        const response = await this.authService.signin(this.signinForm.value);
        if (response.status === 'success') {
          console.log('Signin successful', response.message);
          this.router.navigate(['/']);
        }
      } catch (error: any) {
        this.errorMessage = error.message || 'Signin failed';
        console.error('Signin error', error);
      }
    } else {
      this.errorMessage = 'Please enter your username and password.';
    }
  }
}
