# API Usuarios con Flask

CRUD completo con validaciones.

## Documentación Swagger

Ejecuta el proyecto y visita:

http://localhost:5000/apidocs

## Endpoints

GET /usuarios  
GET /usuarios/{id}  
POST /usuarios  
PUT /usuarios/{id}  
PATCH /usuarios/{id}  
DELETE /usuarios/{id}  

## Ejemplo POST

{
  "nombre": "Juan",
  "edad": 25,
  "usuario": "juan123"
}