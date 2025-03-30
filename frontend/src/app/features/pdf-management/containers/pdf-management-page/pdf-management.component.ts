import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../../core/http/services/api.service';
import { ToastService } from '../../../../shared/components/toast/toast.service';

interface PDFStatistic {
  pdf_count: number;
  doc_count: number;
}

@Component({
  selector: 'app-pdf-management-page',
  standalone: false,
  templateUrl: './pdf-management-page.component.html',
  styleUrls: ['./pdf-management-page.component.scss'],
})
export class PdfManagementPageComponent implements OnInit {
  pdfStatistic: PDFStatistic = { pdf_count: 0, doc_count: 0 };
  pdfList: string[] = [];
  isLoadingUpload: boolean = false;
  isLoadingList: boolean = false;
  isClearingDatabase: boolean = false;

  constructor(
    private apiService: ApiService,
    private toastService: ToastService
  ) {}

  ngOnInit(): void {
    this.loadStatistics();
    this.listPDFs();
  }

  async loadStatistics(): Promise<void> {
    try {
      const stats = await this.apiService.get<PDFStatistic>('/pdfManagement');
      this.pdfStatistic = stats;
    } catch (error: any) {
      this.toastService.showToast(
        `Error loading statistics: ${error.message}`,
        'error'
      );
    }
  }

  async uploadPDF(file: File): Promise<void> {
    // Receive the File object
    if (!file) {
      this.toastService.showToast(
        'Please select a PDF file to upload.',
        'warning'
      );
      return;
    }

    this.isLoadingUpload = true;
    const formData = new FormData();
    formData.append('file', file);

    try {
      const result: any = await this.apiService.postFormData('/pdf', formData);
      console.log(result);
      if (result.status === 'success') {
        this.toastService.showToast(
          `Success: ${result.status}\nFilename: ${result.filename}\nLoaded ${result.doc_len} documents\nLoaded len=${result.chunk_len} chunks`,
          'success'
        );
        this.listPDFs();
        this.loadStatistics();
      } else {
        this.toastService.showToast(
          result.error || 'An error occurred during the upload.',
          'error'
        );
      }
    } catch (error: any) {
      const errorMessage = error.message.includes('Status: 400')
        ? `${error.message.split('Response: ')[1]}`
        : `An error occurred while uploading the PDF: ${error.message}`;
      this.toastService.showToast(errorMessage, 'error');
    } finally {
      this.isLoadingUpload = false;
      // Clear the file input (optional, might be handled in PdfUploadComponent)
      const fileInput = document.getElementById('pdfFile') as HTMLInputElement;
      if (fileInput) {
        fileInput.value = '';
      }
    }
  }

  async listPDFs(): Promise<void> {
    this.isLoadingList = true;
    try {
      const result: any = await this.apiService.get('/list_documents');
      if (result.documents && result.documents.length > 0) {
        const seenPDFs = new Set<string>();
        this.pdfList = result.documents
          .map((doc: any) => doc.source)
          .filter((source: string) => {
            if (!seenPDFs.has(source)) {
              seenPDFs.add(source);
              return true;
            }
            return false;
          });
      } else {
        this.pdfList = [];
        this.toastService.showToast('No documents found.', 'info');
      }
    } catch (error: any) {
      this.toastService.showToast(
        `Error listing PDFs: ${error.message}`,
        'error'
      );
    } finally {
      this.isLoadingList = false;
    }
  }

  async deletePDF(fileName: string): Promise<void> {
    if (!confirm(`Are you sure you want to delete ${fileName}?`)) return;

    try {
      const result: any = await this.apiService.post('/delete_pdf', {
        file_name: fileName,
      });
      if (result.status === 'success') {
        this.toastService.showToast('PDF deleted successfully.', 'success');
        this.listPDFs();
        this.loadStatistics();
      } else {
        this.toastService.showToast(
          `Failed to delete PDF: ${result.error || 'Unknown error'}`,
          'error'
        );
      }
    } catch (error: any) {
      this.toastService.showToast(
        `Error deleting PDF: ${error.message}`,
        'error'
      );
    }
  }

  async clearDatabase(): Promise<void> {
    if (
      !confirm(
        'Are you sure you want to delete all PDFs and clear the database?'
      )
    )
      return;
    this.isClearingDatabase = true;
    try {
      const result: any = await this.apiService.post('/clear_db');
      this.toastService.showToast(
        result.error
          ? `Error: ${result.error}`
          : 'Database and files cleared successfully',
        result.error ? 'error' : 'success'
      );
      this.listPDFs();
      this.loadStatistics();
    } catch (error: any) {
      this.toastService.showToast(`Network Error: ${error.message}`, 'error');
    } finally {
      this.isClearingDatabase = false;
    }
  }

  handleNavigation(event: Event): void {
    // You can add logic here if needed before navigation
  }
}
