package com.springtutor.backend.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.RequestMethod;
import com.springtutor.backend.dto.ChatRequest;
import com.springtutor.backend.dto.ChatResponse;
import com.springtutor.backend.service.ChatService;

@RestController
@RequestMapping("/api/chat")
public class ChatController {
  private final ChatService chatService;

  public ChatController(ChatService chatService) {
    this.chatService = chatService;
  }

  @RequestMapping(value = "/health", method = RequestMethod.HEAD)
  public ResponseEntity<Void> healthHead() {
    return ResponseEntity.ok().build();
  }

  @GetMapping("/health")
  public String getChat() {
    return "Chat service is running";
  }

  // @RequestBody le dice a Spring que el cuerpo de la petición HTTP viene en
  // formato JSON y que lo convierta automáticamente al objeto Java indicado.
  @PostMapping("/message")
  public ChatResponse sendMessage(@RequestBody ChatRequest request) {
    return chatService.sendMessage(request.getMessage());
  }
}
