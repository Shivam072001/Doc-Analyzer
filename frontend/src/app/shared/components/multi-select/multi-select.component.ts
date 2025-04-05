import {
  Component,
  Input,
  Output,
  EventEmitter,
  HostListener,
  ElementRef,
  OnInit,
} from '@angular/core';

@Component({
  selector: 'app-multi-select',
  standalone: false,
  templateUrl: './multi-select.component.html',
  styleUrls: ['./multi-select.component.scss'],
})
export class MultiSelectDropdownComponent implements OnInit {
  @Input() options: any[] = [];
  @Input() placeholder = 'Select options';
  @Output() selectionChange = new EventEmitter<any[]>();

  isOpen = false;
  searchTerm = '';
  selectedOptions: any[] = [];
  filteredOptions: any[] = [];
  isExactMatch = false;

  constructor(private readonly elementRef: ElementRef) {}

  ngOnInit(): void {
    this.filteredOptions = [...this.options];
  }

  toggleDropdown(): void {
    this.isOpen = !this.isOpen;
    if (this.isOpen) {
      this.filterOptions();
    }
  }

  updateSearchTerm(event: Event): void {
    this.searchTerm = (event.target as HTMLInputElement)?.value || '';
    console.log(this.searchTerm);
    this.filterOptions();
  }

  toggleExactMatch(): void {
    this.isExactMatch = !this.isExactMatch;
    this.filterOptions();
  }

  filterOptions(): void {
    this.filteredOptions = this.options.filter((option) => {
      const searchTermLower = this.searchTerm.toLowerCase();

      if (this.isExactMatch) {
        return option.startsWith(searchTermLower);
      } else {
        return option.includes(searchTermLower);
      }
    });
  }

  onOptionSelect(option: any): void {
    const index = this.selectedOptions.indexOf(option);
    if (index > -1) {
      this.selectedOptions.splice(index, 1);
    } else {
      this.selectedOptions.push(option);
    }
    this.selectionChange.emit(this.selectedOptions);
  }

  isSelected(option: any): boolean {
    return this.selectedOptions.includes(option);
  }

  removeSelection(option: any): void {
    const index = this.selectedOptions.indexOf(option);
    if (index > -1) {
      this.selectedOptions.splice(index, 1);
      this.selectionChange.emit(this.selectedOptions);
    }
  }

  clearSearch(): void {
    this.searchTerm = '';
    this.filterOptions();
  }

  clearAllSelection(event: Event): void {
    this.selectedOptions = [];
    this.selectionChange.emit(this.selectedOptions);
    event.stopPropagation(); // Prevent dropdown toggle when clicking clear all
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent): void {
    if (!this.elementRef.nativeElement.contains(event.target)) {
      this.isOpen = false;
    }
  }
}
