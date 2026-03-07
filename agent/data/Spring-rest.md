# Spring REST — Endpoints y controladores

## Anotaciones de mapeo HTTP

### @RequestMapping

Mapea una URL a una clase o método. Se puede especificar
el método HTTP con el atributo method.

### @GetMapping

Mapea peticiones HTTP GET a un método.
Se usa para obtener recursos sin modificarlos.

### @PostMapping

Mapea peticiones HTTP POST a un método.
Se usa para crear nuevos recursos.

### @PutMapping

Mapea peticiones HTTP PUT a un método.
Se usa para actualizar un recurso completo.

### @PatchMapping

Mapea peticiones HTTP PATCH a un método.
Se usa para actualizar parcialmente un recurso.

### @DeleteMapping

Mapea peticiones HTTP DELETE a un método.
Se usa para eliminar recursos.

## Anotaciones de parámetros

### @RequestBody

Convierte el cuerpo JSON de la petición en un objeto Java.
Spring usa Jackson para la deserialización automáticamente.

### @PathVariable

Extrae un valor de la URL.
Ejemplo: @GetMapping("/users/{id}") con @PathVariable Long id

### @RequestParam

Extrae un parámetro de la query string.
Ejemplo: GET /users?page=1 con @RequestParam int page

### @ResponseStatus

Especifica el código HTTP que devuelve el endpoint.
Por defecto los endpoints devuelven 200 OK.

## ResponseEntity

Clase de Spring que permite controlar completamente la respuesta HTTP:

- El cuerpo de la respuesta
- Los headers
- El código de estado HTTP

Ejemplo: return ResponseEntity.status(201).body(nuevoUsuario);
