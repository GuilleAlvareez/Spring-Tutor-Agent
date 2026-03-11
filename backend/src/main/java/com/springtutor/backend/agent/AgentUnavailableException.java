package com.springtutor.backend.agent;

public class AgentUnavailableException extends RuntimeException {
  public AgentUnavailableException(String message) {
    super(message);
  }
}