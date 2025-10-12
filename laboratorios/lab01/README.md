# Laboratorio 01 - Sistema de Comunicaciones Espaciales
- Profesor: Viktor Tapia
- Ayudante: Luciano Yevenes
- Alumno: Rodrigo Pereira
- Asignatura: Redes Computacionales, vespertino 2-2025
- Fecha: 12 de octubre de 2025

## 📡 Descripción del Proyecto

Este proyecto implementa un **sistema de comunicaciones espaciales** que simula la interacción entre una **Estación Espacial** y dos sistemas terrestres:
- **Centro de Control** (comunicación TCP)
- **Sistema de Alertas** (comunicación UDP)

El objetivo es demostrar el uso de **sockets TCP y UDP** en Python para establecer comunicaciones cliente-servidor, entendiendo las diferencias entre ambos protocolos de transporte.

---

## 🏗️ Arquitectura del Sistema

```
                 ┌─────────────────────┐
                 │  Estación Espacial  │
                 │     (Cliente)       │
                 └──────┬────────┬─────┘
                        │        │
                    TCP │        │ UDP
                       ↓↑        ↓↑
            ┌──────────────┐  ┌─────────────────┐
            │Centro Control│  │Sistema Alertas  │
            │  (Servidor)  │  │   (Servidor)    │
            │   TCP:8001   │  │   UDP:8002      │
            └──────────────┘  └─────────────────┘
```

### Componentes

1. **`estacion_espacial.py`** - Cliente que se conecta a los servidores
2. **`centro_control.py`** - Servidor TCP para reportes y consultas
3. **`sistema_alertas.py`** - Servidor UDP para alertas rápidas

### ¿Cómo funciona?

El sistema opera mediante un modelo **cliente-servidor** con dos canales de comunicación independientes:

#### Flujo de Comunicación TCP (Centro de Control)

1. **Inicio del servidor:** `centro_control.py` se ejecuta primero y queda escuchando en el puerto 8001
2. **Conexión del cliente:** La estación espacial establece una conexión TCP
3. **Intercambio de mensajes:**
   - El cliente envía comandos (`REPORTE:`, `CONSULTAR`, `MISION_COMPLETA`)
   - El servidor valida y procesa cada mensaje
   - El servidor responde confirmando la recepción
   - La conexión se mantiene hasta recibir `MISION_COMPLETA`
4. **Cierre ordenado:** Ambos extremos cierran la conexión de forma controlada

#### Flujo de Comunicación UDP (Sistema de Alertas)

1. **Inicio del servidor:** `sistema_alertas.py` se ejecuta y escucha en el puerto 8002
2. **Envío de datagramas:** La estación espacial envía mensajes sin establecer conexión previa
3. **Respuestas rápidas:**
   - Cada mensaje recibe una confirmación inmediata
   - No hay garantía de orden ni entrega
   - Ideal para alertas donde la velocidad es prioritaria
4. **Finalización:** El servidor se detiene al recibir `base_segura`

#### Validación de Mensajes

La estación espacial implementa validación mediante la función `verificar_mensaje_tcp()` que solo permite:
- Mensajes que comiencen con `REPORTE:` seguido de contenido
- El comando exacto `CONSULTAR` (sin caracteres adicionales)
- El comando exacto `MISION_COMPLETA` (sin caracteres adicionales)

Cualquier otro formato es rechazado y se solicita al usuario reintentar.

---

## 🚀 Cómo Ejecutar

### Prerrequisitos
- Python 3.x
- Sistema operativo: Linux/macOS/Windows

### Pasos de Ejecución

**1. Abrir tres terminales diferentes**

**Terminal 1 - Centro de Control (TCP):**
```bash
cd /path/to/lab01
python3 centro_control.py
```

**Terminal 2 - Sistema de Alertas (UDP):**
```bash
cd /path/to/lab01
python3 sistema_alertas.py
```

**Terminal 3 - Estación Espacial (Cliente):**
```bash
cd /path/to/lab01
python3 estacion_espacial.py
```

> ⚠️ **Importante:** Debes iniciar primero los servidores (Centro de Control y Sistema de Alertas) antes de ejecutar la Estación Espacial.

---

## 📋 Funcionalidades

### 🛰️ Estación Espacial (Cliente)

El cliente presenta un menú interactivo con tres opciones:

```
[ESTACION ESPACIAL] Iniciando sistema de comunicaciones...
1. Conectar con Centro de Control
2. Enviar alerta rapida
3. Abortar el envio de mensajes y salir
Seleccione una opcion (1-3):
```

#### Opción 1: Centro de Control (TCP)
Permite enviar comandos específicos:
- `REPORTE:<mensaje>` - Envía un reporte al centro de control
- `CONSULTAR` - Solicita el historial de reportes
- `MISION_COMPLETA` - Finaliza la comunicación

#### Opción 2: Sistema de Alertas (UDP)
Permite enviar alertas rápidas:
- Cualquier mensaje se considera una alerta
- `base_segura` - Finaliza el modo de emergencia

#### Opción 3: Salir
Cierra el sistema sin establecer conexión.

### 🎯 Centro de Control (Servidor TCP)

- **Puerto:** 8001
- **Protocolo:** TCP (confiable, orientado a conexión)
- **Funcionalidad:**
  - Recibe y almacena reportes
  - Mantiene un historial numerado
  - Responde consultas sobre el historial
  - Confirma recepción de cada mensaje

### 🚨 Sistema de Alertas (Servidor UDP)

- **Puerto:** 8002
- **Protocolo:** UDP (rápido, sin conexión)
- **Funcionalidad:**
  - Recibe alertas de emergencia
  - Confirma recepción inmediata
  - No mantiene historial

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Enviar Reportes al Centro de Control

**Terminal Estación Espacial:**
```
Seleccione una opcion (1-3): 1
[ESTACION ESPACIAL] Conectado con Centro de Control (TCP)
Astronauta> REPORTE: Nivel de oxigeno: 95%
Centro de control: Reporte almacenado. Todo bajo control, Estación.

Astronauta> REPORTE: Temperatura estable a 22°C
Centro de control: Reporte almacenado. Todo bajo control, Estación.

Astronauta> CONSULTAR
Centro de control: === HISTORIAL DE COMUNICACIONES ===
1. Nivel de oxigeno: 95%
2. Temperatura estable a 22°C

Astronauta> MISION_COMPLETA
Centro de control: Comunicación finalizada. Buen trabajo, astronautas.

[ESTACION ESPACIAL] Desconectado de Centro de Control
```

**Terminal Centro de Control:**
```
[CENTRO DE CONTROL] Esperando conexiones de la Estacion Espacial...
[CENTRO DE CONTROL] Conectado con ('127.0.0.1', 54321)
[CENTRO DE CONTROL] Desconectado de la Estacion Espacial
```

### Ejemplo 2: Enviar Alertas Rápidas

**Terminal Estación Espacial:**
```
Seleccione una opcion (1-3): 2
[ESTACION ESPACIAL] Conectado con Sistema de Alertas (UDP)
Emergencia> Fuga de aire detectada en modulo 3
Alerta: CONFIRMADO: Fuga de aire detectada en modulo 3

Emergencia> Iniciando procedimiento de sellado
Alerta: CONFIRMADO: Iniciando procedimiento de sellado

Emergencia> base_segura
Sistema: Modo emergencia desactivado. Mantente seguro alla arriba.

[ESTACION ESPACIAL] Desconectado de Sistemas de Alertas
```

**Terminal Sistema de Alertas:**
```
[SISTEMA DE ALERTAS] Esperando alertas rapidas...
[SISTEMA DE ALERTAS] Desconectado de la Estacion Espacial
```

### Ejemplo 3: Validación de Mensajes

**Mensajes inválidos en Centro de Control:**
```
Astronauta> Hola
Mensaje no permitido. Intente de nuevo con 'REPORTE:', 'CONSULTAR', 'MISION_COMPLETA'.

Astronauta> CONSULTAR:
Mensaje no permitido. Intente de nuevo con 'REPORTE:', 'CONSULTAR', 'MISION_COMPLETA'.

Astronauta> REPORTE:Todo OK
Centro de control: Reporte almacenado. Todo bajo control, Estación.
```

---

## 🔍 Detalles Técnicos

### TCP vs UDP

| Característica | TCP (Centro Control) | UDP (Sistema Alertas) |
|----------------|---------------------|----------------------|
| **Conexión** | Orientado a conexión | Sin conexión |
| **Confiabilidad** | Garantiza entrega | No garantiza entrega |
| **Orden** | Mantiene orden | No garantiza orden |
| **Velocidad** | Más lento | Más rápido |
| **Uso** | Reportes críticos | Alertas rápidas |

### Estructura de Mensajes

**TCP - Centro de Control:**
```python
"REPORTE:<contenido>"     # Envía un reporte
"CONSULTAR"               # Solicita historial
"MISION_COMPLETA"         # Finaliza conexión
```

**UDP - Sistema de Alertas:**
```python
"<cualquier_mensaje>"     # Alerta de emergencia
"base_segura"             # Finaliza modo emergencia
```

### Puertos Utilizados

- **Puerto 8001:** Centro de Control (TCP)
- **Puerto 8002:** Sistema de Alertas (UDP)
- **Host:** 127.0.0.1 (localhost)

---

## 📚 Conceptos Aprendidos

1. **Sockets en Python:** Uso de la librería `socket`
2. **Protocolo TCP:** Conexión confiable con `SOCK_STREAM`
3. **Protocolo UDP:** Comunicación rápida con `SOCK_DGRAM`
4. **Cliente-Servidor:** Arquitectura de comunicación en red
5. **Codificación:** Uso de `encode()` y `decode()` para UTF-8
6. **Manejo de conexiones:** Context managers con `with`

---
Código 👽 por rodrigo-alonso-pereira
