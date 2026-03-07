# Spring Tutor Agent — Backend

Backend del proyecto Spring Tutor Agent. API REST construida con Spring Boot 3.5 y Java 21 que actúa como capa intermedia entre el frontend Angular y el agente de IA Python. Gestiona el chat, persiste el historial de mensajes en PostgreSQL y proxifica las peticiones al agente.

---

## Stack

| Tecnología            | Versión | Rol                      |
| --------------------- | ------- | ------------------------ |
| Java                  | 21      | Lenguaje                 |
| Spring Boot           | 3.5.11  | Framework principal      |
| Spring Web            | —       | API REST                 |
| Spring Data JPA       | —       | Acceso a base de datos   |
| Hibernate             | 6.6     | ORM                      |
| PostgreSQL (Supabase) | 15      | Base de datos            |
| Lombok                | —       | Reducción de boilerplate |
| Maven                 | 3.x     | Gestión de dependencias  |

---

## Estructura del proyecto

```
backend/
└── src/main/java/com/springtutor/backend/
    ├── controller/
    │   └── ChatController.java       → endpoints REST
    ├── service/
    │   └── ChatService.java          → lógica de negocio
    ├── repository/
    │   └── MessageRepository.java    → acceso a base de datos
    ├── model/
    │   └── Message.java              → entidad JPA (tabla messages)
    ├── dto/
    │   ├── ChatRequest.java          → objeto de entrada del endpoint
    │   └── ChatResponse.java         → objeto de salida del endpoint
    └── BackendApplication.java       → clase main, arranca el servidor
```

### ¿Por qué esta estructura?

El proyecto sigue una arquitectura en capas donde cada capa tiene una responsabilidad única:

- **controller** — solo recibe peticiones HTTP y delega en el servicio. No contiene lógica.
- **service** — contiene toda la lógica de negocio. Es la única capa que decide qué hacer con los datos.
- **repository** — única capa que habla con la base de datos. El resto del código nunca toca SQL directamente.
- **model** — clases que representan tablas en la base de datos (entidades JPA).
- **dto** — objetos de transferencia de datos. No son tablas, solo transportan información entre el cliente y la API.

---

## Flujo de una petición

```
Cliente (Postman / Angular)
        |
        | POST /api/chat/message
        | Body: { "message": "¿Qué es Spring Boot?" }
        ↓
ChatController.java
  - Recibe la petición HTTP
  - Extrae el body y lo convierte en ChatRequest
  - Delega en ChatService
        |
        ↓
ChatService.java
  - Guarda el mensaje del usuario en la base de datos (role: USER)
  - Llama al agente Python (próximamente)
  - Guarda la respuesta del agente en la base de datos (role: ASSISTANT)
  - Devuelve un ChatResponse al controller
        |
        ↓
MessageRepository.java
  - Ejecuta el INSERT en PostgreSQL via JPA
  - Spring genera el SQL automáticamente
        |
        ↓
PostgreSQL (Supabase)
  - Tabla messages
  - Guarda id (UUID), content, role, sent_at
        |
        ↓ (respuesta sube por la misma cadena)
        |
Cliente recibe:
  { "response": "Respuesta del agente..." }
```

---

## Endpoints

### GET `/api/chat/health`

Comprueba que el servidor está activo.

**Respuesta:**

```
200 OK
"Chat service is running!"
```

---

### POST `/api/chat/message`

Envía un mensaje al tutor y devuelve su respuesta. Persiste tanto el mensaje del usuario como la respuesta del agente en la base de datos.

**Body:**

```json
{
  "message": "¿Qué es la inyección de dependencias en Spring?"
}
```

**Respuesta:**

```json
{
  "response": "La inyección de dependencias es un patrón..."
}
```

---

## Modelo de datos

### Tabla `messages`

| Campo   | Tipo      | Descripción                                        |
| ------- | --------- | -------------------------------------------------- |
| id      | UUID      | Clave primaria, generada automáticamente           |
| content | VARCHAR   | Contenido del mensaje                              |
| role    | VARCHAR   | `USER` o `ASSISTANT`                               |
| sent_at | TIMESTAMP | Fecha y hora de creación, generada automáticamente |

La tabla es creada automáticamente por Hibernate al arrancar la aplicación gracias a `spring.jpa.hibernate.ddl-auto=update`.

---

## Clases principales

### `Message.java` — Entidad JPA

Representa una fila en la tabla `messages`. Las anotaciones JPA le dicen a Hibernate cómo mapear la clase a la base de datos.

```java
@Entity           // esta clase es una tabla
@Table(name = "messages")
public class Message {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;          // generado automáticamente

    @Column(nullable = false)
    private String content;   // texto del mensaje

    @Column(nullable = false)
    private String role;      // "USER" o "ASSISTANT"

    @PrePersist               // se ejecuta antes de guardar
    public void prePersist() {
        sentAt = LocalDateTime.now();
    }
}
```

### `MessageRepository.java` — Repositorio JPA

Interfaz que extiende `JpaRepository`. Spring genera la implementación automáticamente al arrancar. No hay que escribir SQL para las operaciones básicas.

Métodos disponibles de forma gratuita:

- `save(message)` — INSERT o UPDATE
- `findAll()` — SELECT \*
- `findById(id)` — SELECT por id
- `deleteById(id)` — DELETE por id

### `ChatService.java` — Servicio

Orquesta el flujo completo: guarda el mensaje del usuario, obtiene la respuesta del agente y guarda la respuesta. Es la única clase que tiene acceso al repositorio.

### `ChatController.java` — Controlador

Define los endpoints REST. Usa `@RestController` para que Spring serialice automáticamente los objetos Java a JSON. Solo delega en el servicio, no contiene lógica.

### `ChatRequest.java` y `ChatResponse.java` — DTOs

Objetos simples que representan el JSON de entrada y salida de la API. Lombok genera getters, setters y constructores automáticamente con `@Data`.

---

## Configuración

El archivo `application.properties` contiene la configuración de la aplicación. **No se sube a git** ya que contiene credenciales.

```properties
# Conexión a PostgreSQL (Supabase)
spring.datasource.url=jdbc:postgresql://HOST:5432/postgres
spring.datasource.username=TU_USERNAME
spring.datasource.password=TU_PASSWORD

# Hibernate crea/actualiza las tablas automáticamente
spring.jpa.hibernate.ddl-auto=update

# Muestra el SQL generado en la terminal (útil para desarrollo)
spring.jpa.show-sql=true
```

Usa `application.properties.example` como plantilla y crea tu propio `application.properties` con las credenciales reales.

---

## Arrancar el proyecto

**Requisitos previos:**

- Java 21
- Maven (incluido en el proyecto via `mvnw`)
- Una base de datos PostgreSQL (o proyecto en Supabase)

**Pasos:**

1. Clona el repositorio
2. Copia `application.properties.example` a `application.properties` y rellena las credenciales
3. Arranca el servidor:

```bash
# Linux / Mac
./mvnw spring-boot:run

# Windows
mvnw.cmd spring-boot:run
```

El servidor arrancará en `http://localhost:8080`.

---

## Próximos pasos

- [ ] Conectar con el agente Python (FastAPI) via HTTP
- [ ] Añadir autenticación JWT con Spring Security
- [ ] Gestión de conversaciones (agrupar mensajes)
- [ ] Endpoint para recuperar historial de mensajes
- [ ] Tests unitarios e de integración
