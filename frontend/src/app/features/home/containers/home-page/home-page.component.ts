import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../../core/http/services/api.service';
import { ToastService } from '../../../../shared/components/toast/toast.service';

@Component({
  selector: 'app-home-page',
  standalone: false,
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent implements OnInit {
  promptTypes: string[] = [];
  queryPDF: string = '';
  queryAI: string = '';
  queryResponse: string = '';
  queryResponseAI: string = '';
  documentUsageStats: any = {};
  queryUsageStats: any = {};
  chatHistoryStatus: string = '';
  isLoadingDocumentQuery: boolean = false;
  isLoadingAIQuery: boolean = false;

  constructor(
    private readonly apiService: ApiService,
    private readonly toastService: ToastService
  ) {}

  ngOnInit(): void {
    this.fetchPrompts();
  }

  async fetchPrompts(): Promise<void> {
    try {
      const prompts = await this.apiService.get<{ [key: string]: string }>(
        '/prompts'
      );
      this.promptTypes = Object.keys(prompts);
    } catch (error: any) {
      this.toastService.showToast(
        `Error fetching prompts: ${error.message}`,
        'error'
      );
    }
  }

  async askPDF(): Promise<void> {
    if (!this.queryPDF) {
      this.toastService.showToast(
        'Please enter a query for the PDF.',
        'warning'
      );
      return;
    }
    this.isLoadingDocumentQuery = true;
    this.queryResponse =
      '<div class="spinner"></div><p class="loading-message">Fetching response, please wait...</p>';
    const promptType = (
      document.getElementById('promptType') as HTMLSelectElement
    )?.value;

    try {
      const result: any = await this.apiService.post('/ask_document', {
        query: this.queryPDF,
        promptType,
      });
      console.log(result);
      this.queryResponse = await this.formatResponse(result);
      if (result.document_usage) {
        this.documentUsageStats = result.document_usage;
      }
      if (result.query_usage) {
        this.queryUsageStats = result.query_usage;
      }
    } catch (error: any) {
      this.queryResponse = `<p>An error occurred while processing the PDF query: ${error.message}</p>`;
      this.toastService.showToast(
        `Error querying PDF: ${error.message}`,
        'error'
      );
    } finally {
      this.isLoadingDocumentQuery = false;
    }
  }

  async askAI(): Promise<void> {
    if (!this.queryAI) {
      this.toastService.showToast(
        'Please enter a query for the AI.',
        'warning'
      );
      return;
    }
    this.isLoadingAIQuery = true;
    this.queryResponseAI =
      '<div class="spinner"></div><p class="loading-message">Fetching response, please wait...</p>';
    try {
      const result: any = await this.apiService.post('/ai', {
        query: this.queryAI,
      });
      this.queryResponseAI = await this.formatResponse(result);
    } catch (error: any) {
      this.queryResponseAI = `<p>An error occurred while processing the AI query: ${error.message}</p>`;
      this.toastService.showToast(
        `Error querying AI: ${error.message}`,
        'error'
      );
    } finally {
      this.isLoadingAIQuery = false;
    }
  }

  async copyTextAndSubmit(): Promise<void> {
    this.queryAI = this.queryPDF;
    await this.askAI();
  }

  async clearChatHistory(): Promise<void> {
    try {
      const data: any = await this.apiService.post('/clear_chat_history');
      this.queryResponse = '';
      this.chatHistoryStatus =
        data.status === 'Chat history cleared successfully'
          ? 'Chat history cleared successfully.'
          : 'Failed to clear chat history.';
      setTimeout(() => (this.chatHistoryStatus = ''), 3000);
    } catch (error: any) {
      this.chatHistoryStatus = `An error occurred while clearing chat history: ${error.message}`;
      this.toastService.showToast(
        `Error clearing chat history: ${error.message}`,
        'error'
      );
    }
  }

  private async formatResponse(result: any): Promise<string> {
    if (result.disclaimer) {
      return `<p>${result.disclaimer}</p>`;
    } else if (result.answer) {
      if (this.isValidJSON(result.answer)) {
        return `<pre><code class="json">${this.syntaxHighlightJSON(
          result.answer
        )}</code></pre>`;
      } else {
        return `<p>${
          (await this.markdownToHTML(result.answer)) || 'No response received.'
        }</p>`;
      }
    } else {
      return `<p>${result.error || 'No response received.'}</p>`;
    }
  }

  private isValidJSON(str: string): boolean {
    try {
      JSON.parse(str);
      return true;
    } catch (e) {
      return false;
    }
  }

  private syntaxHighlightJSON(json: string): string {
    json = JSON.stringify(JSON.parse(json), null, 2);
    return json
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  private async markdownToHTML(markdown: string): Promise<string> {
    if (!markdown) return '';
    const { marked } = await import('marked');
    return marked.parse(markdown);
  }

  handleNavigation(event: Event): void {
    // You can add logic here if needed before navigation
    // For now, the routerLink directive in the template will handle navigation
  }
}
