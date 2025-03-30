import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';

@Component({
  selector: 'app-pdf-list',
  standalone: false,
  templateUrl: './pdf-list.component.html',
  styleUrls: ['./pdf-list.component.scss'],
})
export class PdfListComponent implements OnInit {
  @Input() pdfList: string[] = [];
  @Input() isLoading: boolean = false;
  @Output() delete = new EventEmitter<string>();

  ngOnInit(): void {
    // No direct API call here, data is passed in
  }

  onDelete(fileName: string): void {
    this.delete.emit(fileName);
  }

  viewPDF(fileName: string): void {
    window.open(`/pdfs/${fileName}`, '_blank');
  }
}
