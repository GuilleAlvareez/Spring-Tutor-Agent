## Te explico cada capa del backend:

controller/ → solo recibe peticiones HTTP y delega. No tiene lógica.
service/ → toda la lógica de negocio vive aquí.
repository/ → solo acceso a base de datos.
model/ → las entidades JPA (tablas de la base de datos).
dto/ → objetos de transferencia de datos. ChatRequest y ChatResponse son DTOs — no son tablas, solo transportan datos entre el frontend y el backend.
