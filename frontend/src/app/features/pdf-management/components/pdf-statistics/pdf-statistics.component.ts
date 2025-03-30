import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-pdf-statistics',
  standalone: false,
  templateUrl: './pdf-statistics.component.html',
  styleUrls: ['./pdf-statistics.component.scss'],
})
export class PdfStatisticsComponent {
  @Input() pdfCount: number = 0;
}