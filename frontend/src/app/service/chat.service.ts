import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

// @Injectable: le dice a Angular que este servicio puede ser inyectado
// en cualquier componente, igual que @Service en Spring
@Injectable({
  providedIn: 'root',
})
export class ChatService {
  // URL del backend Spring Boot
  private apiUrl = environment.apiUrl;
  // HttpClient es el equivalente a RestClient de Spring
  // Angular lo inyecta automáticamente
  constructor(private http: HttpClient) {}

  sendMessage(message: string): Observable<{ response: string }> {
    return this.http.post<{ response: string }>(`${this.apiUrl}/message`, {
      message,
    });
  }
}
