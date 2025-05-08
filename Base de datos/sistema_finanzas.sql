-- Tabla de usuarios actualizada para soportar autenticación con redes sociales
CREATE TABLE usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE,
    contraseña_hash VARCHAR(255),
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    fecha_nacimiento DATE,
    telefono VARCHAR(20),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_login DATETIME,
    esta_activo BOOLEAN DEFAULT TRUE,
    token_verificacion VARCHAR(255),
    fecha_verificacion DATETIME,
    proveedor_auth ENUM('email', 'google', 'facebook', 'instagram') DEFAULT 'email',
    id_proveedor VARCHAR(255) COMMENT 'ID único del usuario en el proveedor de autenticación',
    avatar_url VARCHAR(255),
    es_administrador BOOLEAN DEFAULT FALSE,
    UNIQUE KEY (proveedor_auth, id_proveedor) COMMENT 'Para evitar duplicados con el mismo proveedor'
);

-- Insertar usuario administrador con credenciales quemadas
-- Contraseña: 1234 (hasheada con bcrypt)
INSERT INTO usuarios (email, contraseña_hash, nombre, apellido, esta_activo, es_administrador)
VALUES (
    'admin@finanzas-ia.com',
    '$2a$10$N9qo8uLOickgx2ZMRZoMy.Mrqsf3dC7lE6CNAa1ERmRKx4EJNDpW2',
    'Administrador',
    'Sistema',
    TRUE,
    TRUE
);

-- Resto de las tablas permanecen igual...
-- Tabla de tokens de sesión
CREATE TABLE sesiones (
    sesion_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    token_sesion VARCHAR(255) NOT NULL,
    dispositivo VARCHAR(255),
    ip VARCHAR(45),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion DATETIME NOT NULL,
    es_valida BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Índice adicional para búsqueda por proveedor
CREATE INDEX idx_usuario_proveedor ON usuarios(proveedor_auth, id_proveedor);

-- Tabla de perfiles de usuario
CREATE TABLE perfiles_usuario (
    perfil_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT UNIQUE NOT NULL,
    profesion VARCHAR(100),
    industria VARCHAR(100),
    ingresos_anuales DECIMAL(15,2),
    nivel_educacion ENUM('secundaria', 'pregrado', 'posgrado', 'doctorado', 'otro'),
    pais_residencia VARCHAR(100),
    ciudad VARCHAR(100),
    avatar_url VARCHAR(255),
    biografia TEXT,
    preferencias_moneda VARCHAR(3) DEFAULT 'USD',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Tabla de metas financieras
CREATE TABLE metas_financieras (
    meta_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    tipo_meta ENUM('ahorro', 'inversion', 'deuda', 'ingreso', 'gasto', 'otros') NOT NULL,
    monto_objetivo DECIMAL(15,2) NOT NULL,
    monto_actual DECIMAL(15,2) DEFAULT 0,
    fecha_inicio DATE NOT NULL,
    fecha_objetivo DATE NOT NULL,
    prioridad ENUM('baja', 'media', 'alta', 'critica') DEFAULT 'media',
    esta_completada BOOLEAN DEFAULT FALSE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Tabla de ingresos (ganancias)
CREATE TABLE ingresos (
    ingreso_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    fuente VARCHAR(255) NOT NULL,
    monto DECIMAL(15,2) NOT NULL,
    frecuencia ENUM('diario', 'semanal', 'quincenal', 'mensual', 'bimestral', 'trimestral', 'semestral', 'anual', 'ocasional') NOT NULL,
    fecha_ingreso DATE NOT NULL,
    es_recurrente BOOLEAN DEFAULT FALSE,
    categoria VARCHAR(100),
    notas TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Tabla de gastos
CREATE TABLE gastos (
    gasto_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    monto DECIMAL(15,2) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    fecha_gasto DATE NOT NULL,
    es_recurrente BOOLEAN DEFAULT FALSE,
    frecuencia ENUM('diario', 'semanal', 'quincenal', 'mensual', 'bimestral', 'trimestral', 'semestral', 'anual', 'ocasional'),
    notas TEXT,
    etiquetas VARCHAR(255),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Tabla de ahorros e inversiones
CREATE TABLE ahorros_inversiones (
    ahorro_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    tipo ENUM('cuenta_ahorros', 'cdt', 'acciones', 'fondos', 'cripto', 'bienes_raices', 'otros') NOT NULL,
    monto_actual DECIMAL(15,2) NOT NULL,
    tasa_retorno DECIMAL(5,2),
    fecha_inicio DATE NOT NULL,
    fecha_vencimiento DATE,
    riesgo ENUM('bajo', 'medio', 'alto') DEFAULT 'medio',
    notas TEXT,
    meta_asociada INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (meta_asociada) REFERENCES metas_financieras(meta_id) ON DELETE SET NULL
);

-- Tabla de deudas
CREATE TABLE deudas (
    deuda_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    acreedor VARCHAR(255) NOT NULL,
    monto_total DECIMAL(15,2) NOT NULL,
    monto_pendiente DECIMAL(15,2) NOT NULL,
    tasa_interes DECIMAL(5,2),
    tipo_interes ENUM('fijo', 'variable') DEFAULT 'fijo',
    fecha_inicio DATE NOT NULL,
    fecha_vencimiento DATE,
    pago_minimo DECIMAL(15,2),
    frecuencia_pago ENUM('diario', 'semanal', 'quincenal', 'mensual', 'bimestral', 'trimestral', 'semestral', 'anual'),
    notas TEXT,
    meta_asociada INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (meta_asociada) REFERENCES metas_financieras(meta_id) ON DELETE SET NULL
);

-- Tabla de recomendaciones de IA
CREATE TABLE recomendaciones_ia (
    recomendacion_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    tipo_recomendacion ENUM('ahorro', 'inversion', 'gasto', 'deuda', 'ingreso', 'meta') NOT NULL,
    contenido TEXT NOT NULL,
    fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    es_aceptada BOOLEAN DEFAULT NULL,
    fecha_aceptacion DATETIME,
    contexto TEXT COMMENT 'Datos contextuales usados para generar la recomendación',
    puntuacion_relevancia INT COMMENT 'Puntuación de relevancia asignada por la IA (1-100)',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Tabla de preferencias de usuario para IA
CREATE TABLE preferencias_ia (
    preferencia_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT UNIQUE NOT NULL,
    tolerancia_riesgo ENUM('conservador', 'moderado', 'agresivo') DEFAULT 'moderado',
    horizonte_temporal ENUM('corto_plazo', 'medio_plazo', 'largo_plazo') DEFAULT 'medio_plazo',
    enfoque_principal ENUM('ahorro', 'inversion', 'reduccion_deuda', 'ingresos', 'balance') DEFAULT 'balance',
    intereses_especificos SET('tecnologia', 'bienes_raices', 'mercados', 'cripto', 'fondos', 'emprendimiento', 'otros'),
    actualizaciones_frecuentes BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Tabla de historial financiero (para análisis de IA)
CREATE TABLE historial_financiero (
    historial_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    fecha_registro DATE NOT NULL,
    patrimonio_neto DECIMAL(15,2) NOT NULL,
    total_activos DECIMAL(15,2) NOT NULL,
    total_pasivos DECIMAL(15,2) NOT NULL,
    ingresos_mes DECIMAL(15,2),
    gastos_mes DECIMAL(15,2),
    ahorros_mes DECIMAL(15,2),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);