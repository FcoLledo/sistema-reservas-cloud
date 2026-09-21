# Informe de Pruebas
## Sistema de Reservas Cloud

## 1. Objetivo

El objetivo de las pruebas es validar el funcionamiento básico del sistema de reservas y realizar una comprobación inicial de su comportamiento bajo carga.

Se realizaron dos tipos de pruebas:

- Pruebas unitarias y funcionales sobre el Reservation Service.
- Prueba básica de carga sobre el Reservation Service ejecutado mediante Docker.

---

## 2. Entorno de pruebas

El sistema fue ejecutado localmente utilizando Docker Compose.

La arquitectura utilizada durante las pruebas estuvo compuesta por dos contenedores independientes:

| Servicio | Puerto | Estado |
|---|---:|---|
| Reservation Service | 8001 | Operativo |
| Auth Service | 8002 | Operativo |

La ejecución fue verificada mediante:

```bash
docker compose ps
```

Ambos contenedores se encontraban en estado `Up` durante la validación.

---

## 3. Pruebas unitarias

Las pruebas fueron implementadas utilizando Pytest y FastAPI TestClient.

Archivo utilizado:

```text
tests/test_reservation.py
```

### 3.1 Funcionalidades verificadas

Se implementaron dos pruebas:

1. Creación de una reserva mediante `POST /reservations`.
2. Consulta del listado de reservas mediante `GET /reservations`.

### 3.2 Ejecución

Comando utilizado:

```bash
python -m pytest tests/test_reservation.py -v
```

### 3.3 Resultados

| Indicador | Resultado |
|---|---:|
| Pruebas ejecutadas | 2 |
| Pruebas aprobadas | 2 |
| Pruebas fallidas | 0 |
| Tiempo de ejecución | 1,18 segundos |

Resultado:

```text
test_create_reservation PASSED
test_list_reservations PASSED

2 passed
```

Las dos pruebas finalizaron correctamente.

Durante la ejecución se generaron dos advertencias de deprecación relacionadas con dependencias utilizadas por FastAPI/Starlette. Estas advertencias no provocaron fallos en las pruebas ni afectaron el resultado de la validación.

---

## 4. Prueba de carga

Se realizó una prueba básica de carga utilizando un script desarrollado en Python con HTTPX.

Archivo utilizado:

```text
tests/load/load_test.py
```

La prueba realizó 100 solicitudes HTTP contra:

```text
GET /health
```

del Reservation Service:

```text
http://127.0.0.1:8001/health
```

### 4.1 Ejecución

Comando utilizado:

```bash
python tests/load/load_test.py
```

### 4.2 Resultados

| Indicador | Resultado |
|---|---:|
| Solicitudes realizadas | 100 |
| Solicitudes exitosas | 100 |
| Errores | 0 |
| Tiempo total | 3,82 segundos |
| Solicitudes por segundo | 26,16 |
| Tasa de éxito | 100 % |

Durante esta ejecución no se registraron errores HTTP.

---

## 5. Análisis de resultados

Las pruebas unitarias permitieron verificar correctamente las operaciones básicas de creación y consulta de reservas implementadas en el Reservation Service.

La prueba de carga ejecutó 100 solicitudes contra el endpoint de salud del servicio y obtuvo una tasa de éxito del 100 %, sin errores durante la ejecución.

El resultado corresponde exclusivamente al entorno local utilizado y a una carga limitada de 100 solicitudes secuenciales. Por lo tanto, no debe interpretarse como una medición de capacidad máxima ni como evidencia de rendimiento en un entorno productivo.

---

## 6. Problema identificado y solución aplicada

Durante la implementación inicial de la prueba de carga se detectó un error en el cálculo del tiempo transcurrido.

Inicialmente se utilizaba:

```python
elapsed = time.perf_counter()
```

Esto entregaba un valor acumulado del contador de rendimiento del sistema en lugar del tiempo real utilizado por la prueba.

El cálculo fue corregido utilizando:

```python
elapsed = time.perf_counter() - start
```

Después de la corrección se volvió a ejecutar la prueba, obteniendo un tiempo válido de 3,82 segundos para las 100 solicitudes.

---

## 7. Limitaciones

Las pruebas realizadas corresponden al alcance de un prototipo académico.

Entre sus principales limitaciones se encuentran:

- La prueba de carga utiliza solicitudes secuenciales y no usuarios concurrentes.
- Solo se utilizaron 100 solicitudes.
- La prueba fue realizada en un entorno local.
- No se realizaron pruebas de estrés ni de capacidad máxima.
- La cobertura de pruebas unitarias se limita a las funcionalidades principales seleccionadas.
- Las reservas utilizan almacenamiento temporal en memoria.

Para una implementación productiva sería necesario ampliar la cobertura y realizar pruebas concurrentes en infraestructura representativa del entorno de producción.

---

## 8. Evidencias

Las capturas correspondientes a las ejecuciones se encuentran en:

```text
docs/evidencias/
```

Archivos:

```text
evidencia-pruebas-unitarias.png
evidencia-prueba-carga.png
```

---

## 9. Conclusión

Las pruebas ejecutadas permitieron comprobar el funcionamiento básico del Reservation Service dentro del alcance definido para el prototipo.

Las dos pruebas automatizadas finalizaron correctamente y la prueba básica de carga completó 100 solicitudes sin errores.

Los resultados permiten validar el comportamiento inicial de la solución, reconociendo que para un escenario productivo sería necesario realizar pruebas de mayor cobertura, concurrencia y volumen.