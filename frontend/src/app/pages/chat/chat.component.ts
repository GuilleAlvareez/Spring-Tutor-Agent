import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../service/chat.service';
import { marked } from 'marked';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

interface Message {
  role: 'USER' | 'ASSISTANT';
  content: string;
}

@Component({
  selector: 'app-chat',
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
})
export class ChatComponent {
  messages: Message[] = [];
  inputMessage: string = '';
  isLoading: boolean = false;

  private chatService = inject(ChatService);
  private sanitizer = inject(DomSanitizer);

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
      error: () => {
        this.messages.push({
          role: 'ASSISTANT',
          content: 'Error al conectar con el servidor.',
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
