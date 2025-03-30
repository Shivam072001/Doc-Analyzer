import { Component } from '@angular/core';

@Component({
  selector: 'app-header',
  standalone: false,
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {
  title = 'AskItRight';
  poweredBy = 'AI-Powered PDF Query App (Ollama3.1) 🚀';
  dashboardTitle = 'Document Interaction Dashboard';
  dashboardDescription =
    'Manage your PDFs, ask questions, and view usage statistics all in one place.';
}
