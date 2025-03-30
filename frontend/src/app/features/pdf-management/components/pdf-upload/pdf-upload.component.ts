import { Component, Output, EventEmitter, Input } from '@angular/core';
import { ToastService } from '../../../../shared/components/toast/toast.service';

@Component({
  selector: 'app-pdf-upload',
  standalone: false,
  templateUrl: './pdf-upload.component.html',
  styleUrls: ['./pdf-upload.component.scss'],
})
export class PdfUploadComponent {
  @Output() upload = new EventEmitter<File>(); // Emit the File object
  @Input() isLoading: boolean = false;

  selectedFile: File | null = null;

  constructor(
    private toastService: ToastService
  ) {}

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  uploadFile(): void {
    if (this.selectedFile) {
      this.upload.emit(this.selectedFile);
      this.selectedFile = null; // Optionally clear the selected file
    } else {
      // Optionally show a message if no file is selected
      this.toastService.showToast(
        'Please select a PDF file to upload.',
        'warning'
      );
    }
  }
}
