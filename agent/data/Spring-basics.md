# Spring Boot — Conceptos básicos

## ¿Qué es Spring Boot?

Spring Boot es un framework de Java que simplifica la creación de aplicaciones Spring.
Su objetivo es eliminar la configuración manual y permitir arrancar un proyecto en minutos.

## Anotaciones principales

### @SpringBootApplication

Marca la clase principal de la aplicación. Combina tres anotaciones:

- @Configuration: define beans de configuración
- @EnableAutoConfiguration: activa la configuración automática
- @ComponentScan: escanea los componentes del proyecto

### @RestController

Marca una clase como controlador REST. Combina @Controller y @ResponseBody.
Todos los métodos devuelven datos JSON directamente.

### @Service

Marca una clase como servicio de lógica de negocio.
Spring la gestiona automáticamente y la inyecta donde se necesite.

### @Repository

Marca una clase como repositorio de acceso a datos.
