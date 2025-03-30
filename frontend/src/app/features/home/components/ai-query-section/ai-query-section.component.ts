import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-ai-query-section',
  standalone: false,
  templateUrl: './ai-query-section.component.html',
  styleUrls: ['./ai-query-section.component.scss'],
})
export class AiQuerySectionComponent {
  @Input() query: string = '';
  @Input() response: string = '';
  @Input() isLoading: boolean = false;
  @Output() ask = new EventEmitter<void>();
  @Output() copyAndAsk = new EventEmitter<void>();
  @Output() queryChange = new EventEmitter<string>(); // Added this line

  onAsk(): void {
    this.ask.emit();
  }

  onCopyAndAsk(): void {
    this.copyAndAsk.emit();
  }
}
