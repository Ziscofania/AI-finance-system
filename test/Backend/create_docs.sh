mkdir -p docs

cat > docs/workflow.md << EOF
# Flujo de Trabajo para Pruebas - Backend

Este documento explica el flujo de trabajo para realizar pruebas en el backend del sistema de finanzas con IA.

## Objetivo

Garantizar que cada módulo del backend sea probado y documentado correctamente para asegurar la calidad del software.

## Pasos para el flujo de trabajo

1. **Asignación de tareas:** Cada integrante del equipo se asigna una sección o módulo a probar (IA, core, datos, etc.)
2. **Diseño de pruebas:** Crear pruebas unitarias y funcionales para cada módulo.
3. **Ejecución de pruebas:** Correr las pruebas localmente y en CI/CD.
4. **Documentación:** Registrar en este docs los resultados, problemas y observaciones.
5. **Revisión:** Revisión cruzada por otro integrante del equipo.
6. **Cierre:** Marcar la prueba como aprobada o con observaciones para corregir.

---

## Herramientas recomendadas

- Python + pytest para pruebas
- Git para control de versiones
- Documentación en Markdown en esta carpeta \`docs/\`
EOF

cat > docs/ai_tests.md << EOF
# Documentación de Pruebas - IA

## Módulo de pruebas

- Archivo principal de pruebas: \`test/ai/test_model.py\`

## Objetivos

- Validar el correcto funcionamiento de los modelos de IA.
- Asegurar que los resultados estén dentro de los rangos esperados.
- Probar la carga y predicción con datos de ejemplo.

## Registro de pruebas

| Fecha       | Responsable | Descripción                         | Resultado    | Observaciones          |
|-------------|-------------|-----------------------------------|--------------|-----------------------|
| 2025-05-26  | Juan Pérez  | Prueba carga modelo y predicción  | Aprobado     | Resultado correcto     |
|             |             |                                   |              |                       |
EOF

cat > docs/core_tests.md << EOF
# Documentación de Pruebas - Lógica Core

## Módulo de pruebas

- Archivo principal: \`test/core/test_main.py\`

## Objetivos

- Validar funciones y endpoints principales.
- Verificar manejo correcto de errores.
- Comprobar integridad de datos.

## Registro de pruebas

| Fecha       | Responsable | Descripción                        | Resultado    | Observaciones          |
|-------------|-------------|----------------------------------|--------------|-----------------------|
| 2025-05-26  | Ana Gómez   | Prueba función cálculo de saldo  | Aprobado     | Correcto en todos casos|
|             |             |                                  |              |                       |
EOF

cat > docs/data_tests.md << EOF
# Documentación de Pruebas - Datos

## Archivos de prueba

- Ubicación: \`test/data/sample.json\`

## Objetivos

- Verificar que los datos de prueba estén bien formateados.
- Asegurar que las funciones procesen correctamente datos de ejemplo.
- Probar casos límite con datos corruptos o faltantes.

## Registro de pruebas

| Fecha       | Responsable  | Descripción                        | Resultado    | Observaciones          |
|-------------|--------------|----------------------------------|--------------|-----------------------|
| 2025-05-26  | Luis Martínez| Validación de formato JSON       | Aprobado     | Sin errores            |
|             |              |                                  |              |                       |
EOF

cat > docs/issues.md << EOF
# Registro de Problemas en Pruebas

| Fecha       | Módulo       | Responsable | Descripción del problema               | Estado       | Resolución / Comentarios       |
|-------------|--------------|-------------|--------------------------------------|--------------|-------------------------------|
| 2025-05-26  | IA           | Juan Pérez  | Error en carga de modelo con datos X | En progreso  | Se investigará en próxima reunión |
|             |              |             |                                      |              |                               |
EOF

cat > docs/meeting_notes.md << EOF
# Notas de Reuniones - Pruebas Backend

| Fecha       | Asistentes          | Temas tratados                      | Acuerdos / Tareas                          |
|-------------|---------------------|-----------------------------------|--------------------------------------------|
| 2025-05-26  | Juan, Ana, Luis     | Revisión inicial de pruebas IA    | Ana hará pruebas adicionales en core       |
|             |                     |                                   | Luis actualizará datos de prueba            |
EOF

