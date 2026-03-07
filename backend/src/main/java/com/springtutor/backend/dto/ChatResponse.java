package com.springtutor.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

//@Data genera autmaticamente los getter y setter, y el constructor por defecto
@Data
@AllArgsConstructor
public class ChatResponse {
  private String response;
}
