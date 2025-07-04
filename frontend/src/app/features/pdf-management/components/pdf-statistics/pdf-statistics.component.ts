import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-document-statistics',
  standalone: false,
  templateUrl: './pdf-statistics.component.html',
  styleUrls: ['./pdf-statistics.component.scss'],
})
export class PdfStatisticsComponent {
  @Input() pdfCount: number = 0;
  @Input() docxCount: number = 0;
  @Input() csvCount: number = 0;
  @Input() xlsxCount: number = 0;
}
