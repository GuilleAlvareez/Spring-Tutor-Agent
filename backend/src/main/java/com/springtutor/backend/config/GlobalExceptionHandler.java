package com.springtutor.backend.config;

import com.springtutor.backend.agent.AgentUnavailableException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

  @ExceptionHandler(AgentUnavailableException.class)
  public ResponseEntity<Map<String, String>> handleAgentUnavailable(AgentUnavailableException ex) {
    return ResponseEntity
        .status(HttpStatus.SERVICE_UNAVAILABLE)
        .body(Map.of("error", ex.getMessage()));
  }
}