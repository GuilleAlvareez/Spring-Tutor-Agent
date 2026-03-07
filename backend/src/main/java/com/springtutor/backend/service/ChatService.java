package com.springtutor.backend.service;

import org.springframework.stereotype.Service;

import com.springtutor.backend.agent.AgentClient;
import com.springtutor.backend.dto.ChatResponse;
import com.springtutor.backend.model.Message;
import com.springtutor.backend.repository.MessageRepository;

@Service
public class ChatService {
  // Spring inyecta automáticamente el repository aquí
  // no necesitamos hacer "new MessageRepository()", Spring lo gestiona
  private final MessageRepository messageRepository;
  private final AgentClient agentClient;

  public ChatService(MessageRepository messageRepository, AgentClient agentClient) {
    this.messageRepository = messageRepository;
    this.agentClient = agentClient;
  }

  public ChatResponse sendMessage(String userMessage) {
    // 1. Guardamos el mensaje del usuario en la base de datos
    Message userMsg = new Message();
    userMsg.setContent(userMessage);
    userMsg.setRole("USER");
    messageRepository.save(userMsg);

    // 2. Por ahora la respuesta es falsa, luego llamaremos al agente Python
    // String assistantResponse = "Respuesta falsa a: " + userMessage;
    String assistantResponse = agentClient.sendMessage(userMessage);

    // 3. Guardamos la respuesta del asistente en la base de datos
    Message assistantMsg = new Message();
    assistantMsg.setContent(assistantResponse);
    assistantMsg.setRole("ASSISTANT");
    messageRepository.save(assistantMsg);

    // 4. Devolvemos la respuesta al controller
    return new ChatResponse(assistantResponse);
  }
}
