import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-button',
  standalone: false,
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.scss'],
})
export class ButtonComponent {
  @Input() label: string = 'Submit';
  @Input() type: 'button' | 'submit' = 'button';
  @Input() disabled: boolean = false;
}
