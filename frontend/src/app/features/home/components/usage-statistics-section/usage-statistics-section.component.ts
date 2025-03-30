import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-usage-statistics-section',
  standalone: false,
  templateUrl: './usage-statistics-section.component.html',
  styleUrls: ['./usage-statistics-section.component.scss'],
})
export class UsageStatisticsSectionComponent implements OnChanges {
  @Input() pdfUsage: any;
  @Input() queryUsage: any;

  pdfUsageKeys: string[] = [];
  queryUsageKeys: string[] = [];

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['pdfUsage']) {
      this.pdfUsageKeys = Object.keys(this.pdfUsage);
    }
    if (changes['queryUsage']) {
      this.queryUsageKeys = Object.keys(this.queryUsage);
    }
  }
}
