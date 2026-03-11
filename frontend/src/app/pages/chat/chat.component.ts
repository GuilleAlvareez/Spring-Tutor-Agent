import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../service/chat.service';
import { marked } from 'marked';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { NavBarComponent } from '../nav-bar/nav-bar.component';
import hljs from 'highlight.js';

interface Message {
  role: 'USER' | 'ASSISTANT';
  content: string;
}

@Component({
  selector: 'app-chat',
  imports: [CommonModule, FormsModule, RouterModule, NavBarComponent],
  templateUrl: './chat.component.html',
})
export class ChatComponent {
  messages: Message[] = [];
  inputMessage: string = '';
  isLoading: boolean = false;

  private chatService = inject(ChatService);
  private sanitizer = inject(DomSanitizer);

  constructor() {
    marked.use({
      renderer: {
        code(token: any) {
          const lang = token.lang || '';
          const code = token.text;
          if (lang && hljs.getLanguage(lang)) {
            const highlighted = hljs.highlight(code, { language: lang }).value;
            return `<pre><code class="hljs language-${lang}">${highlighted}</code></pre>`;
          }
          const highlighted = hljs.highlightAuto(code).value;
          return `<pre><code class="hljs">${highlighted}</code></pre>`;
        },
      },
    });
  }

  renderMarkdown(content: string): SafeHtml {
    const html = marked.parse(content) as string;
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }

  sendMessage() {
    if (!this.inputMessage.trim() || this.isLoading) return;

    this.messages.push({ role: 'USER', content: this.inputMessage });

    const userMessage = this.inputMessage;
    this.inputMessage = '';
    this.isLoading = true;

    this.chatService.sendMessage(userMessage).subscribe({
      next: (res) => {
        this.messages.push({ role: 'ASSISTANT', content: res.response });
        this.isLoading = false;
      },
      error: (err) => {
        this.messages.push({
          role: 'ASSISTANT',
          content: err.error.error || 'Error al conectar con el servidor.',
        });
        this.isLoading = false;
      },
    });
  }

  onKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }
}
