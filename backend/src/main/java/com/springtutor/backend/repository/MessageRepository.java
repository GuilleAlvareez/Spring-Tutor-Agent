package com.springtutor.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.springtutor.backend.model.Message;

// @Repository: le dice a Spring que esta interfaz es una capa de acceso a datos
// JpaRepository<Message, String> le dice:
//   - Message → la entidad que gestiona
//   - String → el tipo del id (lo tenemos como String/UUID)
@Repository
public interface MessageRepository extends JpaRepository<Message, String> {

}
