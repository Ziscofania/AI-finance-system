# Pruebas del Backend - Sistema de Finanzas con IA

Esta carpeta contiene las pruebas automatizadas del backend del sistema de finanzas con inteligencia artificial.

## Tipos de Pruebas

- **Unitarias (unit tests):**
  - Prueban funciones específicas, independientes del sistema completo.
  - Ubicadas en `core/` y `ai/`.

- **Funcionales/Integración:**
  - Prueban la interacción entre varias funciones o servicios (por ejemplo, carga de datos y procesamiento por IA).
  - Pueden extenderse o agruparse en archivos separados si el proyecto crece.

- **Datos de prueba:**
  - Creados en `test/data/` para simular entradas y salidas esperadas.

---

## Cómo ejecutar las pruebas

### 1. Activar el entorno virtual (si no está activo)

```bash
source venv/bin/activate