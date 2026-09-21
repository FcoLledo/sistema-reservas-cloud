# Sistema de Reservas Cloud

Proyecto desarrollado para la Evaluación del Módulo 2 del Bootcamp Arquitecto Cloud.

## 1. Descripción del proyecto

Sistema de reservas basado en una arquitectura de microservicios que permite gestionar reservas de espacios y recursos.

El prototipo implementa las operaciones principales de creación, consulta y cancelación de reservas, además de un servicio independiente de autenticación.

La solución utiliza FastAPI para el desarrollo de las APIs y Docker para ejecutar los microservicios de manera independiente.

## 2. Objetivo

Diseñar e implementar una arquitectura para un sistema de reservas que sea modular, escalable, segura y fácil de mantener.

El prototipo busca demostrar:

- Gestión de reservas.
- Separación de responsabilidades mediante microservicios.
- Autenticación de usuarios.
- Contenerización de los servicios.
- Capacidad de ejecución independiente de cada microservicio.
- Pruebas unitarias.
- Pruebas básicas de carga.

## 3. Arquitectura

La solución está compuesta por dos microservicios independientes:

### Reservation Service

Responsable de gestionar las reservas del sistema.

Se ejecuta en el puerto:

`8001`

Endpoints principales:

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Verifica que el servicio esté disponible |
| GET | `/health` | Health check del servicio |
| POST | `/reservations` | Crea una reserva |
| GET | `/reservations` | Consulta todas las reservas |
| GET | `/reservations/{reservation_id}` | Consulta una reserva por ID |
| DELETE | `/reservations/{reservation_id}` | Cancela una reserva |

Documentación Swagger:

`http://127.0.0.1:8001/docs`

### Auth Service

Responsable de la autenticación básica de usuarios del prototipo.

Se ejecuta en el puerto:

`8002`

Endpoints principales:

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Verifica que el servicio esté disponible |
| GET | `/health` | Health check del servicio |
| POST | `/login` | Autentica un usuario |

Documentación Swagger:

`http://127.0.0.1:8002/docs`

## 4. Tecnologías utilizadas

- Python 3.14
- FastAPI
- Uvicorn
- Pydantic
- Docker
- Docker Compose
- Pytest
- HTTPX
- Git

## 5. Estructura del proyecto

```text
sistema-reservas-cloud/
│
├── services/
│   ├── auth-service/
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── requirements.txt
│   │
│   └── reservation-service/
│       ├── Dockerfile
│       ├── main.py
│       └── requirements.txt
│
├── tests/
│   ├── load/
│   │   └── load_test.py
│   └── test_reservation.py
│
├── docs/
│   ├── architecture/
│   ├── evidencias/
│   │   ├── evidencia-pruebas-unitarias.png
│   │   └── evidencia-prueba-carga.png
│   └── test-report/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 6. Ejecución del sistema

### Requisitos

Para ejecutar el proyecto localmente se requiere:

- Docker
- Docker Compose

### Levantar los microservicios

Desde la carpeta raíz del proyecto ejecutar:

```bash
docker compose up --build -d
```

Docker construirá las imágenes y levantará los dos microservicios.

### Verificar los contenedores

Ejecutar:

```bash
docker compose ps
```

Los servicios deberían aparecer con estado `Up`:

```text
auth-service          → puerto 8002
reservation-service   → puerto 8001
```

### Acceder a las APIs

Reservation Service:

`http://127.0.0.1:8001/docs`

Auth Service:

`http://127.0.0.1:8002/docs`

### Detener el sistema

Ejecutar:

```bash
docker compose down
```

## 7. Pruebas unitarias

Las pruebas unitarias del Reservation Service fueron implementadas utilizando Pytest y FastAPI TestClient.

Para ejecutarlas:

```bash
python -m pytest tests/test_reservation.py -v
```

Resultado obtenido durante la validación:

| Indicador | Resultado |
|---|---:|
| Pruebas ejecutadas | 2 |
| Pruebas aprobadas | 2 |
| Pruebas fallidas | 0 |
| Tiempo de ejecución | 1,18 segundos |

Las funcionalidades verificadas fueron:

- Creación de una reserva.
- Consulta del listado de reservas.

Durante la ejecución se generaron dos advertencias de deprecación provenientes de dependencias utilizadas por FastAPI/Starlette. Estas advertencias no provocaron fallos en las pruebas.

## 8. Prueba de carga

Se realizó una prueba básica de carga contra el endpoint:

`GET /health`

del Reservation Service ejecutado mediante Docker.

Para ejecutar la prueba:

```bash
python tests/load/load_test.py
```

Resultado obtenido:

| Indicador | Resultado |
|---|---:|
| Solicitudes realizadas | 100 |
| Solicitudes exitosas | 100 |
| Errores | 0 |
| Tiempo total | 3,82 segundos |
| Solicitudes por segundo | 26,16 |

La prueba obtuvo una tasa de éxito del 100 % en el entorno local utilizado.

Los resultados pueden variar dependiendo del hardware y las condiciones de ejecución.

## 9. Seguridad

La arquitectura separa la autenticación de la gestión de reservas mediante un microservicio independiente denominado Auth Service.

Para efectos del prototipo académico se implementó una autenticación básica.

Esta implementación permite demostrar la separación de responsabilidades, pero no debe considerarse un mecanismo de autenticación preparado para producción.

En un entorno productivo se recomienda incorporar:

- Tokens seguros mediante JWT u OAuth2.
- Gestión segura de credenciales.
- HTTPS/TLS para cifrar las comunicaciones.
- Gestión centralizada de secretos.
- Un proveedor de identidad especializado.

## 10. Escalabilidad

Los servicios se ejecutan en contenedores independientes, permitiendo separar sus responsabilidades y ciclos de ejecución.

Esta separación facilita que cada microservicio pueda evolucionar y escalar de forma independiente.

En una arquitectura cloud productiva se podrían incorporar:

- múltiples instancias de cada microservicio;
- balanceadores de carga;
- autoescalado;
- servicios administrados de persistencia;
- monitoreo y observabilidad.

## 11. Limitaciones del prototipo

El proyecto corresponde a un prototipo académico orientado a demostrar los principales conceptos arquitectónicos solicitados.

Actualmente las reservas se almacenan en memoria dentro del Reservation Service.

Esto significa que:

- Las reservas se pierden al reiniciar el servicio.
- Diferentes instancias del servicio no compartirían el mismo estado.
- La solución actual no proporciona persistencia de datos.

En una implementación productiva se debería utilizar una capa de persistencia externa, como una base de datos administrada, permitiendo desacoplar el estado de las instancias de aplicación.

La autenticación implementada también corresponde a una versión simplificada para fines demostrativos.

## 12. Evidencias

Las evidencias de las pruebas realizadas se encuentran almacenadas en:

```text
docs/evidencias/
```

Incluyen:

- `evidencia-pruebas-unitarias.png`
- `evidencia-prueba-carga.png`

## 13. Mejoras futuras

Como evolución del prototipo se propone:

- Incorporar persistencia mediante una base de datos.
- Implementar autenticación mediante JWT, OAuth2 o un proveedor de identidad.
- Implementar HTTPS/TLS.
- Incorporar un API Gateway.
- Implementar balanceo de carga.
- Configurar escalamiento automático.
- Aumentar la cobertura de pruebas unitarias.
- Implementar pruebas concurrentes y de estrés.
- Incorporar monitoreo, métricas y observabilidad.
- Desplegar la solución en una plataforma cloud.

## 14. Conclusión

El prototipo demuestra una arquitectura básica de microservicios para un sistema de reservas.

La solución permite crear, consultar y cancelar reservas, incorpora un servicio independiente de autenticación y utiliza Docker Compose para ejecutar ambos microservicios de forma separada.

Las pruebas realizadas permitieron validar las funcionalidades principales y comprobar el comportamiento básico del Reservation Service bajo una carga controlada.

La arquitectura constituye una base sobre la cual se pueden incorporar posteriormente mecanismos de persistencia, seguridad, escalamiento y observabilidad propios de un entorno cloud productivo.