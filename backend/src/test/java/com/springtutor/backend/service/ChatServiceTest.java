package com.springtutor.backend.service;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.springtutor.backend.agent.AgentClient;
import com.springtutor.backend.dto.ChatResponse;
import com.springtutor.backend.model.Message;
import com.springtutor.backend.repository.MessageRepository;
import com.springtutor.backend.service.ChatService;

// @ExtendWith: activa Mockito en este test
// equivalente a configurar jest.mock() globalmente
@ExtendWith(MockitoExtension.class)
class ChatServiceTest {

  // @Mock: crea un objeto falso de estas clases
  // equivalente a jest.mock('./MessageRepository')
  @Mock
  private MessageRepository messageRepository;

  @Mock
  private AgentClient agentClient;

  // @InjectMocks: crea el ChatService real e inyecta los mocks anteriores
  // equivalente a: const service = new ChatService(mockRepo, mockAgent)
  @InjectMocks
  private ChatService chatService;

  @Test
  void deberiaGuardarMensajeUsuario() {
    // ARRANGE — preparamos el escenario
    String userMessage = "¿Qué es @Service?";
    when(agentClient.sendMessage(userMessage)).thenReturn("Respuesta del agente");

    // ACT — ejecutamos el método
    chatService.sendMessage(userMessage);

    // ASSERT — verificamos que se guardó el mensaje del usuario
    // verify comprueba que se llamó al método con los argumentos correctos
    verify(messageRepository, times(2)).save(any(Message.class));
  }

  @Test
  void deberiaLlamarAlAgenteConElMensajeCorrecto() {
    // ARRANGE
    String userMessage = "¿Qué es @Autowired?";
    when(agentClient.sendMessage(userMessage)).thenReturn("Explicación de @Autowired");

    // ACT
    chatService.sendMessage(userMessage);

    // ASSERT — verificamos que el agente recibió el mensaje correcto
    verify(agentClient).sendMessage(userMessage);
  }

  @Test
  void deberiaRetornarRespuestaDelAgente() {
    // ARRANGE
    String userMessage = "¿Qué es Spring Boot?";
    String expectedResponse = "Spring Boot es un framework...";
    when(agentClient.sendMessage(userMessage)).thenReturn(expectedResponse);

    // ACT
    ChatResponse response = chatService.sendMessage(userMessage);

    // ASSERT — verificamos que la respuesta llega correctamente al controller
    assertEquals(expectedResponse, response.getResponse());
  }

  @Test
  void deberieLanzarExcepcionCuandoElAgenteFalla() {
    // ARRANGE — simulamos que el agente lanza una excepción
    String userMessage = "¿Qué es Spring Boot?";
    when(agentClient.sendMessage(userMessage))
        .thenThrow(new RuntimeException("Agente no disponible"));

    // ACT + ASSERT — verificamos que la excepción se propaga
    assertThrows(RuntimeException.class, () -> {
      chatService.sendMessage(userMessage);
    });
  }
}