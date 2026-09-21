# Documentación Técnica de Arquitectura
## Sistema de Reservas Cloud

## 1. Objetivo de la arquitectura

La solución tiene como objetivo implementar un prototipo de sistema de reservas utilizando una arquitectura basada en microservicios.

El sistema permite realizar las operaciones principales de creación, consulta y cancelación de reservas, separando la gestión de reservas de la autenticación de usuarios.

La arquitectura busca favorecer la modularidad, mantenibilidad y capacidad de evolución independiente de sus componentes.

---

## 2. Arquitectura implementada

La solución está compuesta por dos microservicios:

### Reservation Service

Responsable de la lógica asociada a la gestión de reservas.

Funciones principales:

- Crear reservas.
- Consultar todas las reservas.
- Consultar una reserva mediante su identificador.
- Cancelar reservas.
- Proporcionar un endpoint de health check.

El servicio utiliza FastAPI y se ejecuta en el puerto `8001`.

### Auth Service

Responsable de la autenticación básica de usuarios.

Funciones principales:

- Autenticar un usuario.
- Proporcionar un endpoint de health check.

El servicio utiliza FastAPI y se ejecuta en el puerto `8002`.

---

## 3. Comunicación

Los servicios exponen interfaces HTTP mediante APIs REST y utilizan JSON para el intercambio de información.

En el prototipo actual, el cliente accede directamente a cada microservicio.

```text
Usuario / Cliente
       |
    HTTP/REST
       |
       +---------------------+
       |                     |
       v                     v
 Auth Service        Reservation Service
    :8002                   :8001
```

En una evolución productiva se podría incorporar un API Gateway como punto único de entrada.

---

## 4. Contenerización

Cada microservicio se ejecuta en un contenedor independiente.

Docker Compose permite construir, iniciar y administrar ambos servicios de manera conjunta.

La separación mediante contenedores facilita:

- aislamiento entre servicios;
- reproducibilidad del entorno;
- despliegue independiente;
- evolución independiente de los componentes.

La ejecución se realiza mediante:

```bash
docker compose up --build -d
```

---

## 5. Modelo de reservas

El Reservation Service utiliza dos modelos principales definidos mediante Pydantic.

### ReservationCreate

Representa los datos necesarios para crear una reserva:

```text
customer_name: str
resource: str
reservation_date: datetime
```

### Reservation

Extiende el modelo `ReservationCreate` e incorpora:

```text
id: UUID
```

El identificador UUID permite asignar un identificador único a cada reserva.

---

## 6. Persistencia

Para el alcance del prototipo académico, las reservas se almacenan temporalmente en memoria mediante una estructura de datos del Reservation Service.

Esta decisión permite validar rápidamente las operaciones principales sin incorporar infraestructura adicional.

La principal limitación es que las reservas se pierden cuando el servicio se reinicia.

Además, múltiples instancias del Reservation Service no podrían compartir el mismo estado.

Para un entorno productivo se recomienda utilizar una base de datos externa administrada, desacoplando la persistencia de las instancias de aplicación.

---

## 7. Seguridad

La arquitectura separa la responsabilidad de autenticación mediante el Auth Service.

La autenticación implementada corresponde a una demostración básica para el prototipo y no constituye una solución de seguridad preparada para producción.

Una evolución productiva debería incorporar:

- autenticación mediante JWT, OAuth2 o proveedor de identidad;
- almacenamiento seguro de credenciales;
- gestión de secretos;
- HTTPS/TLS para cifrado de comunicaciones;
- autorización de acceso a los recursos protegidos.

---

## 8. Escalabilidad

La separación de responsabilidades permite que cada microservicio pueda evolucionar de manera independiente.

La contenerización también facilita la creación de múltiples instancias de un servicio.

Sin embargo, el prototipo actual utiliza almacenamiento en memoria, por lo que el Reservation Service no debe considerarse actualmente stateless.

Para permitir escalamiento horizontal real sería necesario externalizar el estado mediante una base de datos.

Una arquitectura productiva podría incorporar:

```text
Cliente
   |
API Gateway / Load Balancer
   |
   +------------------------+
   |                        |
Auth Service          Reservation Service
   |                        |
Múltiples             Múltiples
instancias             instancias
                            |
                      Base de datos
```

Esto permitiría distribuir solicitudes entre diferentes instancias según la demanda.

---

## 9. Adaptabilidad y mantenibilidad

La arquitectura divide las responsabilidades principales en servicios independientes.

Esto permite modificar la lógica de autenticación sin alterar directamente la lógica de reservas y viceversa.

FastAPI proporciona además documentación automática mediante OpenAPI/Swagger, facilitando la comprensión y prueba de las interfaces disponibles.

La separación de componentes reduce el acoplamiento y proporciona una base para futuras ampliaciones.

---

## 10. Pruebas

La solución incorpora pruebas automatizadas mediante Pytest para validar operaciones principales del Reservation Service.

También se implementó una prueba básica de carga mediante HTTPX.

Los resultados completos se encuentran documentados en:

```text
docs/test-report/informe-pruebas.md
```

Las evidencias se encuentran en:

```text
docs/evidencias/
```

---

## 11. Decisiones técnicas principales

| Decisión | Justificación |
|---|---|
| Arquitectura de microservicios | Separar responsabilidades y permitir evolución independiente |
| FastAPI | Desarrollo simple de APIs REST y documentación automática |
| Pydantic | Validación y definición estructurada de datos |
| UUID | Identificación única de reservas |
| Docker | Aislamiento y reproducibilidad |
| Docker Compose | Ejecución coordinada de los microservicios |
| Almacenamiento en memoria | Reducir complejidad del prototipo académico |
| Pytest | Automatización de pruebas |
| HTTPX | Ejecución de solicitudes HTTP para pruebas |

---

## 12. Limitaciones actuales

El prototipo presenta deliberadamente las siguientes limitaciones:

- No existe persistencia permanente.
- La autenticación es simplificada.
- No existe API Gateway.
- No existe balanceador de carga.
- No existe autoescalado.
- No existe infraestructura cloud desplegada.
- No existe monitoreo centralizado.
- Las pruebas de carga son básicas y locales.

Estas limitaciones corresponden al alcance definido para el prototipo y constituyen oportunidades de evolución hacia una arquitectura productiva.

---

## 13. Evolución propuesta

Una futura versión podría incorporar:

1. Base de datos administrada.
2. API Gateway.
3. Autenticación mediante un proveedor de identidad.
4. HTTPS/TLS.
5. Balanceo de carga.
6. Autoescalado horizontal.
7. Gestión centralizada de secretos.
8. Monitoreo y observabilidad.
9. Pruebas concurrentes y de estrés.
10. Despliegue en infraestructura cloud.

---

## 14. Conclusión

La arquitectura implementada permite demostrar los principios fundamentales de una solución basada en microservicios mediante dos servicios independientes contenerizados.

El prototipo cumple las operaciones principales de gestión de reservas y separa la responsabilidad de autenticación.

La implementación actual prioriza simplicidad y demostración técnica. Sus limitaciones están identificadas y permiten establecer una ruta clara de evolución hacia una solución cloud con persistencia, seguridad, escalamiento y observabilidad.