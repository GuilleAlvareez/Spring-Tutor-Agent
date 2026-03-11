package com.springtutor.backend.agent;

import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class AgentClient {

  private final RestTemplate restTemplate;
  private final String agentUrl;

  public AgentClient() {
    String agentUrl = System.getenv("AGENT_URL") != null
        ? System.getenv("AGENT_URL")
        : "http://localhost:8000";

    this.restTemplate = new RestTemplate();
    this.agentUrl = agentUrl;
  }

  public String sendMessage(String message) {
    String url = agentUrl + "/chat";

    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);

    String jsonBody = "{\"message\":\"" + message + "\"}";
    HttpEntity<String> entity = new HttpEntity<>(jsonBody, headers);

    try {
      ResponseEntity<AgentResponse> response = restTemplate.exchange(
          url,
          HttpMethod.POST,
          entity,
          AgentResponse.class);

      AgentResponse body = response.getBody();
      return body != null ? body.getResponse() : "Sin respuesta del agente";
    } catch (Exception e) {
      throw new AgentUnavailableException("El agente de IA no está disponible en este momento");
    }
  }
}