# Documentación de Pruebas - Datos

## Archivos de prueba

- Ubicación: `test/data/sample.json`

## Objetivos

- Verificar que los datos de prueba estén bien formateados.
- Asegurar que las funciones procesen correctamente datos de ejemplo.
- Probar casos límite con datos corruptos o faltantes.

# Pruebas de Carga con Locust

## Configuración
1. Instalar dependencia:
   ```bash
   pip install locust

2. Ejecutar pruebas:
    locust -f test/load_test/locustfile.py

# Pruebas de Carga - Escenarios Probados

## Tabla de Endpoints

| Endpoint               | Método | Carga Relativa | Autenticación Requerida |
|------------------------|--------|----------------|-------------------------|
| `/api/auth/login`      | POST   | 50%            | No                      |
| `/api/auth/register`   | POST   | 10%            | No                      |
| `/api/finance/data`    | GET    | 30%            | Sí                      |
| `/api/ia/process`      | POST   | 20%            | Opcional                |

## Parámetros Recomendados

### Prueba Inicial
- **Usuarios concurrentes:** 100
- **Tasa de crecimiento:** 10 usuarios/segundo
- **Duración:** 5-10 minutos

### Prueba de Estrés
- **Usuarios concurrentes:** 500-1000
- **Tasa de crecimiento:** 20-50 usuarios/segundo  
- **Duración:** 15-30 minutos

### Comando de Ejemplo
```bash
locust -f test/load_test/locustfile.py \
--headless \
--users 100 \
--spawn-rate 10 \
--run-time 5m \
--host http://tu-backend:5000