import { Component, OnInit } from '@angular/core';
import { ToastService } from '../../../../shared/components/toast/toast.service';
import { DocumentService } from '../../../../shared/models/services/document.service';

interface DocumentStatistic {
  pdf_count: number;
  docx_count: number;
  csv_count: number;
  xlsx_count: number;
  doc_count: number;
}

@Component({
  selector: 'app-pdf-management-page',
  standalone: false,
  templateUrl: './pdf-management-page.component.html',
  styleUrls: ['./pdf-management-page.component.scss'],
})
export class PdfManagementPageComponent implements OnInit {
  documentStatistic: DocumentStatistic = {
    pdf_count: 0,
    docx_count: 0,
    csv_count: 0,
    xlsx_count: 0,
    doc_count: 0,
  };
  documentList: {
    filename: string;
    type: string;
    size?: number;
    uploadDate?: string;
  }[] = [];
  isLoadingUpload: boolean = false;
  isLoadingList: boolean = false;
  isClearingDatabase: boolean = false;

  constructor(
    private readonly documentService: DocumentService,
    private readonly toastService: ToastService
  ) {}

  ngOnInit(): void {
    this.loadStatistics();
    this.listDocuments();
  }

  async loadStatistics(): Promise<void> {
    try {
      const stats =
        await this.documentService.getFileManagementStats<DocumentStatistic>();
      this.documentStatistic = stats;
    } catch (error: any) {
      this.toastService.showToast(
        `Error loading statistics: ${error.message}`,
        'error'
      );
    }
  }

  async uploadDocument(file: File): Promise<void> {
    if (!file) {
      this.toastService.showToast('Please select a file to upload.', 'warning');
      return;
    }

    this.isLoadingUpload = true;
    const formData = new FormData();
    formData.append('file', file);

    try {
      const result: any = await this.documentService.uploadFile(file);
      console.log(result);
      if (result.status === 'success') {
        this.toastService.showToast(
          `Success: ${result.status}\nFilename: ${result.filename}\nType: ${result.file_type}\nLoaded ${result.doc_len} documents`,
          'success'
        );
        this.listDocuments();
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
        : `An error occurred while uploading the file: ${error.message}`;
      this.toastService.showToast(errorMessage, 'error');
    } finally {
      this.isLoadingUpload = false;
      const fileInput = document.getElementById(
        'documentFile'
      ) as HTMLInputElement;
      if (fileInput) {
        fileInput.value = '';
      }
    }
  }

  async listDocuments(): Promise<void> {
    this.isLoadingList = true;
    try {
      const result: any = await this.documentService.listDocuments();
      console.log('listDocuments: ', result);
      this.documentList = [];
      this.processFiles(result.pdf_files, 'pdf');
      this.processFiles(result.docx_files, 'docx');
      this.processFiles(result.csv_files, 'csv');
      this.processFiles(result.xlsx_files, 'xlsx');
      this.processFiles(result.doc_files, 'doc'); // Assuming you have 'doc_files' as well

      if (this.documentList.length === 0) {
        this.toastService.showToast('No documents found.', 'info');
      }
    } catch (error: any) {
      this.toastService.showToast(
        `Error listing documents: ${error.message}`,
        'error'
      );
    } finally {
      this.isLoadingList = false;
    }
  }

  async deleteDocument(fileName: string, fileType: string): Promise<void> {
    if (!confirm(`Are you sure you want to delete ${fileName}?`)) return;

    try {
      const result: any = await this.documentService.deleteDocument(fileName, fileType);
      if (result.status === 'success') {
        this.toastService.showToast(
          'Document deleted successfully.',
          'success'
        );
        this.listDocuments();
        this.loadStatistics();
      } else {
        this.toastService.showToast(
          `Failed to delete document: ${result.error || 'Unknown error'}`,
          'error'
        );
      }
    } catch (error: any) {
      this.toastService.showToast(
        `Error deleting document: ${error.message}`,
        'error'
      );
    }
  }

  async clearDatabase(): Promise<void> {
    if (
      !confirm(
        'Are you sure you want to delete all documents and clear the database?'
      )
    )
      return;
    this.isClearingDatabase = true;
    try {
      const result: any = await this.documentService.clearDb();
      this.toastService.showToast(
        result.error
          ? `Error: ${result.error}`
          : 'Database and files cleared successfully',
        result.error ? 'error' : 'success'
      );
      this.listDocuments();
      this.loadStatistics();
    } catch (error: any) {
      this.toastService.showToast(`Network Error: ${error.message}`, 'error');
    } finally {
      this.isClearingDatabase = false;
    }
  }

  processFiles = (files: any[], type: string) => {
    if (files && files.length > 0) {
      this.documentList = this.documentList.concat(
        files.map((file: any) => ({
          filename: file.filename,
          type: type,
          size: file.size,
          uploadDate: file.uploadDate,
        }))
      );
    }
  };

  handleNavigation(event: Event): void {
    // You can add logic here if needed before navigation
  }
}
