# Spring Data JPA

## ¿Qué es Spring Data JPA?

Spring Data JPA es un módulo de Spring que simplifica el acceso
a bases de datos relacionales usando JPA e Hibernate por debajo.
Elimina la necesidad de escribir SQL para operaciones básicas.

## Anotaciones de entidades

### @Entity

Marca una clase Java como entidad JPA, es decir, como una tabla
en la base de datos.

### @Table

Especifica el nombre de la tabla en la base de datos.
Si no se usa, Hibernate usa el nombre de la clase.

### @Id

Marca el campo que será la clave primaria de la tabla.

### @GeneratedValue

Configura cómo se genera el valor del id automáticamente.
Estrategias principales:

- GenerationType.UUID: genera un UUID aleatorio
- GenerationType.IDENTITY: usa el autoincrement de la base de datos
- GenerationType.SEQUENCE: usa una secuencia de la base de datos

### @Column

Configura una columna de la tabla. Permite definir:

- nullable: si puede ser nulo
- unique: si debe ser único
- columnDefinition: tipo SQL de la columna (ej: TEXT)

### @PrePersist

Método que se ejecuta automáticamente antes de insertar
la entidad en la base de datos.

## JpaRepository

### ¿Qué es?

Interfaz que Spring Data JPA proporciona para acceder a la base de datos.
Al extenderla, Spring genera automáticamente la implementación.

### Métodos disponibles automáticamente

- save(entity): INSERT o UPDATE
- findById(id): SELECT por id
- findAll(): SELECT todos
- deleteById(id): DELETE por id
- count(): cuenta el número de registros
- existsById(id): comprueba si existe un registro

### Query methods

Spring Data JPA genera queries automáticamente según el nombre del método:

- findByEmail(String email): SELECT WHERE email = ?
- findByRoleAndContent(String role, String content): SELECT WHERE role = ? AND content = ?
- findByContentContaining(String text): SELECT WHERE content LIKE %text%
