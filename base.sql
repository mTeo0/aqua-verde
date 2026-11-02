CREATE DATABASE IF NOT EXISTS aquaverde
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE aquaverde;

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(100),
    direccion VARCHAR(200)
);

CREATE TABLE servicios (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(30) NOT NULL,
    descripcion TEXT,
    precio_base DECIMAL(10,2) DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(100),
    especialidad VARCHAR(30) NOT NULL,
    fecha_contratacion DATE,
    estado VARCHAR(20) DEFAULT 'Activo'
);

CREATE TABLE solicitudes (
    id_solicitud INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_empleado INT NULL,
    fecha_solicitud DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_servicio DATETIME NULL,
    servicios JSON NOT NULL,
    estado VARCHAR(30) DEFAULT 'Pendiente',
    precio_total DECIMAL(10,2) DEFAULT 0,
    observaciones TEXT,
    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_empleado)
        REFERENCES empleados(id_empleado)
);