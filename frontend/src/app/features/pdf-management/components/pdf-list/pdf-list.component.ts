import {
  Component,
  Input,
  Output,
  EventEmitter,
  OnInit,
  OnChanges,
  SimpleChanges,
} from '@angular/core';

interface DocumentItem {
  filename: string;
  type: string;
  size?: number; // Optional file size in bytes
  uploadDate?: string; // Optional upload date string (e.g., ISO 8601)
}

interface SortOption {
  label: string;
  value: string;
}

@Component({
  selector: 'app-document-list',
  standalone: false,
  templateUrl: './pdf-list.component.html',
  styleUrls: ['./pdf-list.component.scss'],
})
export class PdfListComponent implements OnInit, OnChanges {
  @Input() documentList: DocumentItem[] = [];
  @Input() isLoading: boolean = false;
  @Output() delete = new EventEmitter<{ filename: string; type: string }>();

  availableFileTypes: string[] = [];
  selectedFileTypes: string[] = [];
  sortedDocumentList: DocumentItem[] = [];
  sortOptions: SortOption[] = [
    { label: 'File Name', value: 'filename' },
    { label: 'File Size', value: 'size' },
    { label: 'Upload Date', value: 'uploadDate' },
  ];
  sortBy: string = '';
  sortOrder: 'asc' | 'desc' = 'asc';

  ngOnInit(): void {
    this.extractAvailableFileTypes();
    this.sortData(); // Initial sort
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['documentList']) {
      this.extractAvailableFileTypes();
      this.filterDocumentsByTypes(this.selectedFileTypes);
      this.sortData(); // Re-sort on new document list
    }
  }

  extractAvailableFileTypes(): void {
    this.availableFileTypes = [
      ...new Set(this.documentList.map((doc) => doc.type)),
    ].sort();
  }

  filterDocumentsByTypes(selectedTypes: any[]): void {
    this.selectedFileTypes = selectedTypes.map((type) => type.toLowerCase());
    this.sortData(); // Re-sort after filtering
  }

  handleSortByChange(sortByValue: string): void {
    this.sortBy = sortByValue;
    this.sortData();
  }

  toggleSortOrder(): void {
    this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    this.sortData();
  }

  sortData(): void {
    let filteredList = [...this.documentList];

    // Apply file type filter
    if (this.selectedFileTypes.length > 0) {
      filteredList = filteredList.filter((doc) =>
        this.selectedFileTypes.includes(doc.type.toLowerCase())
      );
    }

    // Apply sorting
    if (!this.sortBy) {
      this.sortedDocumentList = filteredList;
      return;
    }

    this.sortedDocumentList = [...filteredList].sort((a, b) => {
      const valueA = a[this.sortBy as keyof DocumentItem];
      const valueB = b[this.sortBy as keyof DocumentItem];

      let comparison = 0;

      // Handle undefined values
      if (valueA === undefined && valueB === undefined) {
        return 0;
      }
      if (valueA === undefined) {
        return this.sortOrder === 'asc' ? 1 : -1;
      }
      if (valueB === undefined) {
        return this.sortOrder === 'asc' ? -1 : 1;
      }

      if (this.sortBy === 'uploadDate') {
        const dateA = valueA ? new Date(valueA as string) : null;
        const dateB = valueB ? new Date(valueB as string) : null;

        if (
          dateA instanceof Date &&
          !isNaN(dateA.getTime()) &&
          dateB instanceof Date &&
          !isNaN(dateB.getTime())
        ) {
          comparison = dateA.getTime() - dateB.getTime();
        } else {
          if (valueA > valueB) comparison = 1;
          if (valueA < valueB) comparison = -1;
        }
      } else if (typeof valueA === 'string' && typeof valueB === 'string') {
        comparison = valueA.localeCompare(valueB);
      } else if (typeof valueA === 'number' && typeof valueB === 'number') {
        comparison = (valueA as number) - (valueB as number);
      } else if (valueA > valueB) {
        comparison = 1;
      } else if (valueA < valueB) {
        comparison = -1;
      }

      return this.sortOrder === 'asc' ? comparison : comparison * -1;
    });
  }

  onDelete(fileName: string, type: string): void {
    this.delete.emit({ filename: fileName, type: type });
  }

  viewDocument(document: DocumentItem): void {
    window.open(`/documents/${document.type}/${document.filename}`, '_blank');
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  formatDate(dateString: string): string {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    } catch (error) {
      return 'N/A';
    }
  }
}
