import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '../../../../core/auth/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  standalone: false,
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss'],
})
export class SignupComponent implements OnInit {
  signupForm: FormGroup;
  errorMessage: string = '';

  constructor(
    private readonly fb: FormBuilder,
    private readonly authService: AuthService,
    private readonly router: Router
  ) {
    this.signupForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  ngOnInit(): void {}

  async onSubmit(): Promise<void> {
    if (this.signupForm.valid) {
      try {
        const response = await this.authService.signup(this.signupForm.value);
        console.log('Signup successful', response);
        this.router.navigate(['/auth/signin']); // Redirect to signin after successful signup
      } catch (error: any) {
        this.errorMessage = error.message || 'Signup failed';
        console.error('Signup error', error);
      }
    } else {
      this.errorMessage = 'Please fill out all required fields correctly.';
    }
  }
}
