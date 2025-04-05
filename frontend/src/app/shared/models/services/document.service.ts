import { Injectable } from '@angular/core';
import { AxiosResponse } from 'axios';
import { ApiService } from '../../../core/http/services/api.service';

@Injectable({
  providedIn: 'root',
})
export class DocumentService {
  constructor(private readonly apiService: ApiService) {}

  async getFileManagementStats<T>(): Promise<T> {
    try {
      return await this.apiService.get<T>('/documentManagement');
    } catch (error: any) {
      console.error('Error fetching file management stats:', error);
      throw error;
    }
  }

  async uploadFile<T>(file: File): Promise<T> {
    try {
      const formData = new FormData();
      formData.append('file', file);
      return await this.apiService.postFormData<T>(
        '/upload_document',
        formData
      );
    } catch (error: any) {
      console.error('Error uploading file:', error);
      throw error;
    }
  }

  async listDocuments<T>(): Promise<T> {
    try {
      return await this.apiService.get<T>('/list_documents');
    } catch (error: any) {
      console.error('Error listing documents:', error);
      throw error;
    }
  }

  async deleteDocument<T>(fileName: string, fileType: string): Promise<T> {
    try {
      return await this.apiService.post<T>('/delete_document', {
        file_name: fileName,
        file_type: fileType,
      });
    } catch (error: any) {
      console.error('Error deleting file:', error);
      throw error;
    }
  }

  async serveFile<T>(filename: string, filetype: string): Promise<void> {
    try {
      const response = (await this.apiService.get<T>(
        `/documents/${filetype}/${filename}`,
        { responseType: 'blob' }
      )) as any;

      return response;
    } catch (error: any) {
      console.error('Error serving file:', error);
      throw error;
    }
  }

  async getPrompts<T>(): Promise<T> {
    try {
      return await this.apiService.get<T>('/prompts');
    } catch (error: any) {
      console.error('Error fetching prompts:', error);
      throw error;
    }
  }

  async askAi<T>(query: string): Promise<T> {
    try {
      return await this.apiService.post<T>('/ai', { query });
    } catch (error: any) {
      console.error('Error asking AI:', error);
      throw error;
    }
  }

  async askDocument<T>(query: string, promptType: string): Promise<T> {
    try {
      return await this.apiService.post<T>('/ask_document', {
        query,
        promptType,
      });
    } catch (error: any) {
      console.error('Error asking document:', error);
      throw error;
    }
  }

  async clearChatHistory<T>(): Promise<T> {
    try {
      return await this.apiService.post<T>('/clear_chat_history', {});
    } catch (error: any) {
      console.error('Error clearing chat history:', error);
      throw error;
    }
  }

  async clearDb<T>(): Promise<T> {
    try {
      return await this.apiService.post<T>('/clear_db', {});
    } catch (error: any) {
      console.error('Error clearing database:', error);
      throw error;
    }
  }

  async getAvailableModels<T>(): Promise<T> {
    try {
      return await this.apiService.get<T>('/available_models');
    } catch (error: any) {
      console.error('Error fetching available models:', error);
      throw error;
    }
  }

  async setModel<T>(modelName: string): Promise<T> {
    try {
      return await this.apiService.post<T>('/set_model', {
        model_name: modelName,
      });
    } catch (error: any) {
      console.error('Error setting model:', error);
      throw error;
    }
  }

  async classifyDocument<T>(documentTextToClassify: string): Promise<T> {
    try {
      return await this.apiService.post<T>('/classify', {
        document_text: documentTextToClassify,
      });
    } catch (error: any) {
      console.error('Error classifying document:', error);
      throw error;
    }
  }
}
