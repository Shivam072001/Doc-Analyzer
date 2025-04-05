import {
  Component,
  Output,
  EventEmitter,
  Input,
  ViewChild,
  ElementRef,
} from '@angular/core';
import { ToastService } from '../../../../shared/components/toast/toast.service';

@Component({
  selector: 'app-document-upload',
  standalone: false,
  templateUrl: './pdf-upload.component.html',
  styleUrls: ['./pdf-upload.component.scss'],
})
export class PdfUploadComponent {
  @Output() upload = new EventEmitter<File>(); // Emit the File object
  @Input() isLoading: boolean = false;

  @ViewChild('pdfFile') pdfFileInput!: ElementRef<HTMLInputElement>;

  selectedFile: File | null = null;

  constructor(private readonly toastService: ToastService) {}

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  uploadFile(): void {
    if (this.selectedFile) {
      this.upload.emit(this.selectedFile);
      this.selectedFile = null;
      console.log('pdfFileInput:', this.pdfFileInput); // <--- ADD THIS LINE

      if (this.pdfFileInput) {
        this.pdfFileInput.nativeElement.value = '';
        console.log(
          'pdfFileInput.nativeElement:',
          this.pdfFileInput.nativeElement
        ); // <--- ADD THIS LINE
      }
    } else {
      this.toastService.showToast(
        'Please select a PDF file to upload.',
        'warning'
      );
    }
  }
}
