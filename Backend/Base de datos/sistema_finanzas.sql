-- Insertar usuario Juan Pérez con autenticación por email
-- Contraseña: JuanPerez2024 (hasheada con bcrypt)
INSERT INTO usuarios (
    email, 
    contraseña_hash, 
    nombre, 
    apellido, 
    fecha_nacimiento, 
    telefono, 
    fecha_registro, 
    esta_activo, 
    avatar_url
) VALUES (
    'juan.perez@example.com', 
    '$2a$10$8vZP5uVz7J3tYd4q9XrB0e.9mZ1lLk2Nf3pDo7sQhGvY6W1cXyHjK', 
    'Juan', 
    'Pérez', 
    '1985-07-15', 
    '+5491145678901', 
    '2023-01-15 09:30:00', 
    TRUE, 
    'https://ejemplo.com/avatars/juanperez.jpg'
);
-- Perfil profesional y personal de Juan Pérez
INSERT INTO perfiles_usuario (
    usuario_id,
    profesion,
    industria,
    ingresos_anuales,
    nivel_educacion,
    pais_residencia,
    ciudad,
    biografia,
    preferencias_moneda
) VALUES (
    LAST_INSERT_ID(), -- Asume que se ejecuta justo después de crear el usuario
    'Ingeniero de Software',
    'Tecnología',
    75000.00,
    'posgrado',
    'Argentina',
    'Buenos Aires',
    'Ingeniero de software con 10 años de experiencia, interesado en inversiones tecnológicas y planificación financiera a largo plazo.',
    'ARS'
);
-- Preferencias para las recomendaciones de IA
INSERT INTO preferencias_ia (
    usuario_id,
    tolerancia_riesgo,
    horizonte_temporal,
    enfoque_principal,
    intereses_especificos,
    actualizaciones_frecuentes
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'moderado',
    'largo_plazo',
    'balance',
    'tecnologia,cripto,emprendimiento',
    TRUE
);
-- Meta 1: Fondo de emergencia
INSERT INTO metas_financieras (
    usuario_id,
    titulo,
    descripcion,
    tipo_meta,
    monto_objetivo,
    monto_actual,
    fecha_inicio,
    fecha_objetivo,
    prioridad
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Fondo de emergencia',
    'Ahorrar 6 meses de gastos básicos para imprevistos',
    'ahorro',
    180000.00,
    75000.00,
    '2023-01-15',
    '2024-01-15',
    'alta'
);

-- Meta 2: Renovar computadora
INSERT INTO metas_financieras (
    usuario_id,
    titulo,
    descripcion,
    tipo_meta,
    monto_objetivo,
    fecha_inicio,
    fecha_objetivo,
    prioridad
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Computadora nueva',
    'Equipo para trabajo y desarrollo personal',
    'ahorro',
    2000.00,
    '2023-01-15',
    '2023-12-31',
    'media'
);
-- Meta 3: Entrada para apartamento
INSERT INTO metas_financieras (
    usuario_id,
    titulo,
    descripcion,
    tipo_meta,
    monto_objetivo,
    fecha_inicio,
    fecha_objetivo,
    prioridad
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Entrada para apartamento',
    '20% para compra de apartamento en zona norte',
    'ahorro',
    50000.00,
    '2023-01-15',
    '2026-01-15',
    'alta'
);

-- Meta 4: MBA
INSERT INTO metas_financieras (
    usuario_id,
    titulo,
    descripcion,
    tipo_meta,
    monto_objetivo,
    fecha_inicio,
    fecha_objetivo,
    prioridad
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Programa MBA',
    'Maestría en administración de empresas en universidad local',
    'ahorro',
    15000.00,
    '2023-01-15',
    '2025-06-01',
    'media'
);
-- Meta 5: Jubilación anticipada
INSERT INTO metas_financieras (
    usuario_id,
    titulo,
    descripcion,
    tipo_meta,
    monto_objetivo,
    fecha_inicio,
    fecha_objetivo,
    prioridad
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Jubilación anticipada',
    'Fondo para retirarse a los 55 años',
    'inversion',
    1000000.00,
    '2023-01-15',
    '2040-07-15',
    'alta'
);

-- Meta 6: Inversión en startup
INSERT INTO metas_financieras (
    usuario_id,
    titulo,
    descripcion,
    tipo_meta,
    monto_objetivo,
    fecha_inicio,
    fecha_objetivo,
    prioridad
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Inversión en startup',
    'Capital para invertir en emprendimiento tecnológico',
    'inversion',
    50000.00,
    '2023-01-15',
    '2028-01-15',
    'media'
);
-- Salario principal
INSERT INTO ingresos (
    usuario_id,
    fuente,
    monto,
    frecuencia,
    fecha_ingreso,
    es_recurrente,
    categoria
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Salario Acme Corp',
    6250.00,
    'mensual',
    '2023-01-01',
    TRUE,
    'salario'
);

-- Freelance
INSERT INTO ingresos (
    usuario_id,
    fuente,
    monto,
    frecuencia,
    fecha_ingreso,
    es_recurrente,
    categoria
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Desarrollo freelance',
    1000.00,
    'mensual',
    '2023-01-01',
    TRUE,
    'ingreso_extra'
);
-- Alquiler
INSERT INTO gastos (
    usuario_id,
    descripcion,
    monto,
    categoria,
    fecha_gasto,
    es_recurrente,
    frecuencia
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Alquiler departamento',
    800.00,
    'vivienda',
    '2023-01-01',
    TRUE,
    'mensual'
);

-- Comida
INSERT INTO gastos (
    usuario_id,
    descripcion,
    monto,
    categoria,
    fecha_gasto,
    es_recurrente,
    frecuencia
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Supermercado y comida',
    400.00,
    'alimentos',
    '2023-01-01',
    TRUE,
    'mensual'
);

-- Transporte
INSERT INTO gastos (
    usuario_id,
    descripcion,
    monto,
    categoria,
    fecha_gasto,
    es_recurrente,
    frecuencia
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Transporte público y taxi',
    150.00,
    'transporte',
    '2023-01-01',
    TRUE,
    'mensual'
);

-- Entretenimiento
INSERT INTO gastos (
    usuario_id,
    descripcion,
    monto,
    categoria,
    fecha_gasto,
    es_recurrente,
    frecuencia
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Cine, salidas, streaming',
    200.00,
    'entretenimiento',
    '2023-01-01',
    TRUE,
    'mensual'
);
-- Cuenta de ahorros
INSERT INTO ahorros_inversiones (
    usuario_id,
    nombre,
    tipo,
    monto_actual,
    tasa_retorno,
    fecha_inicio,
    riesgo,
    meta_asociada
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Cuenta de ahorros emergencia',
    'cuenta_ahorros',
    75000.00,
    2.5,
    '2022-06-01',
    'bajo',
    (SELECT meta_id FROM metas_financieras WHERE titulo = 'Fondo de emergencia' AND usuario_id = (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'))
);

-- Inversión en cripto
INSERT INTO ahorros_inversiones (
    usuario_id,
    nombre,
    tipo,
    monto_actual,
    tasa_retorno,
    fecha_inicio,
    riesgo,
    meta_asociada
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Portafolio cripto',
    'cripto',
    15000.00,
    NULL,
    '2021-03-15',
    'alto',
    (SELECT meta_id FROM metas_financieras WHERE titulo = 'Jubilación anticipada' AND usuario_id = (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'))
);
-- Tarjeta de crédito
INSERT INTO deudas (
    usuario_id,
    acreedor,
    monto_total,
    monto_pendiente,
    tasa_interes,
    fecha_inicio,
    fecha_vencimiento,
    pago_minimo,
    frecuencia_pago
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'Visa Gold',
    5000.00,
    3000.00,
    45.0,
    '2022-11-15',
    NULL,
    300.00,
    'mensual'
);
-- Recomendación 1: Consolidar deuda
INSERT INTO recomendaciones_ia (
    usuario_id,
    tipo_recomendacion,
    contenido,
    fecha_generacion,
    puntuacion_relevancia,
    contexto
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'deuda',
    'Considera consolidar tu deuda de tarjeta de crédito con un préstamo personal a menor tasa de interés. Podrías ahorrar aproximadamente $15,000 pesos en intereses este año.',
    '2023-01-20 14:30:00',
    85,
    'Deuda de tarjeta con alto interés vs. posibles opciones de consolidación'
);

-- Recomendación 2: Aumentar aportes a jubilación
INSERT INTO recomendaciones_ia (
    usuario_id,
    tipo_recomendacion,
    contenido,
    fecha_generacion,
    puntuacion_relevancia,
    contexto
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    'inversion',
    'Basado en tu meta de jubilación anticipada, sugerimos aumentar tus aportes mensuales a instrumentos de largo plazo. Una cartera 70% acciones tech, 20% ETFs globales y 10% bonos sería adecuada para tu perfil.',
    '2023-01-20 14:32:00',
    92,
    'Meta de jubilación anticipada con horizonte de 17 años y tolerancia moderada al riesgo'
);
-- Snapshot financiero inicial
INSERT INTO historial_financiero (
    usuario_id,
    fecha_registro,
    patrimonio_neto,
    total_activos,
    total_pasivos,
    ingresos_mes,
    gastos_mes,
    ahorros_mes
) VALUES (
    (SELECT usuario_id FROM usuarios WHERE email = 'juan.perez@example.com'),
    '2023-01-31',
    225000.00,
    265000.00,
    40000.00,
    7250.00,
    1550.00,
    1500.00
);