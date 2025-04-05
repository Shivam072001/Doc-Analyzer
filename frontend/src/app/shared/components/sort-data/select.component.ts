import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';

interface SelectOption {
  label: string;
  value: string;
}

@Component({
  selector: 'app-select',
  standalone: false,
  templateUrl: './select.component.html',
  styleUrls: ['./select.component.scss'],
})
export class SelectComponent implements OnInit {
  @Input() id: string = '';
  @Input() label: string = '';
  @Input() options: SelectOption[] = [];
  @Input() selectedValue: string = '';
  @Output() selectionChange = new EventEmitter<string>();

  ngOnInit(): void {}

  onSelectChange(newValue: string): void {
    // Changed parameter to newValue of type string
    this.selectedValue = newValue;
    this.selectionChange.emit(this.selectedValue);
  }
}
