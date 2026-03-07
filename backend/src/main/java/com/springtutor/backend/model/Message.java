package com.springtutor.backend.model;

import java.time.LocalDateTime;
import java.util.UUID;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "messages")
public class Message {

  // @Id: marca este campo como clave primaria de la tabla
  @Id

  // @GeneratedValue: el valor del id se genera automáticamente
  // IDENTITY significa que lo genera la propia base de datos (autoincrement)
  @GeneratedValue(strategy = GenerationType.UUID)
  private UUID id;

  @Column(nullable = false, columnDefinition = "TEXT")
  private String content;

  @Column(nullable = false)
  private String role;

  @Column(name = "sent_at", nullable = false)
  private LocalDateTime sentAt;

  // @PrePersist: este método se ejecuta automáticamente ANTES de guardar
  // el objeto en la base de datos, aquí lo usamos para poner la fecha actual
  @PrePersist
  public void prePersist() {
    sentAt = LocalDateTime.now();
  }
}