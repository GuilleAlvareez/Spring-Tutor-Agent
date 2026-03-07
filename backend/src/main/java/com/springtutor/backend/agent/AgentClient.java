package com.springtutor.backend.agent;

import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class AgentClient {

  private final RestTemplate restTemplate;

  public AgentClient() {
    this.restTemplate = new RestTemplate();
  }

  public String sendMessage(String message) {
    String url = "http://localhost:8000/chat";

    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);

    String jsonBody = "{\"message\":\"" + message + "\"}";
    HttpEntity<String> entity = new HttpEntity<>(jsonBody, headers);

    ResponseEntity<AgentResponse> response = restTemplate.exchange(
        url,
        HttpMethod.POST,
        entity,
        AgentResponse.class);

    AgentResponse body = response.getBody();
    return body != null ? body.getResponse() : "Sin respuesta del agente";
  }
}