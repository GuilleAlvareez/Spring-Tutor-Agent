# Anotaciones de Spring Boot

## Anotaciones de componentes

### @Component

Marca una clase como componente genérico de Spring.
Spring la detecta automáticamente y la gestiona como un bean.

### @Service

Especialización de @Component para la capa de lógica de negocio.
Semánticamente indica que la clase contiene reglas de negocio.

### @Repository

Especialización de @Component para la capa de acceso a datos.
Añade traducción automática de excepciones de base de datos.

### @Controller

Especialización de @Component para la capa web.
Se usa junto con @ResponseBody o directamente @RestController.

## Anotaciones de inyección

### @Autowired

Inyecta automáticamente una dependencia gestionada por Spring.
Se puede usar en constructores, campos o métodos setter.

### @Qualifier

Se usa junto con @Autowired cuando hay varias implementaciones
de la misma interfaz para especificar cuál inyectar.

### @Value

Inyecta valores desde application.properties directamente en un campo.
Ejemplo: @Value("${server.port}") private int port;

## Anotaciones de configuración

### @Configuration

Marca una clase como fuente de definición de beans.
Equivalente a un archivo XML de configuración de Spring.

### @Bean

Marca un método dentro de @Configuration como productor de un bean.
Spring gestiona el objeto devuelto por ese método.

### @Primary

Cuando hay varias implementaciones, marca cuál es la preferida
para ser inyectada por defecto.
