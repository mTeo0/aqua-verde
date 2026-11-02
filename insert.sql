USE piscineria_jardineria;

INSERT INTO servicios (nombre, categoria, descripcion, precio_base, activo)
SELECT
    'Paquete Piscina',
    'Piscineria',
    'Cepillado de paredes y fondo, aspirado, retiro de hojas, control de pH y cloro, y ajuste de productos para mantener el agua en buenas condiciones.',
    50000,
    TRUE
WHERE NOT EXISTS (
    SELECT 1
    FROM servicios
    WHERE nombre = 'Paquete Piscina'
);

INSERT INTO servicios (nombre, categoria, descripcion, precio_base, activo)
SELECT
    'Paquete Jardín',
    'Jardineria',
    'Corte de pasto, poda de plantas, limpieza de canteros y retiro de residuos para mantener el jardín limpio y ordenado.',
    50000,
    TRUE
WHERE NOT EXISTS (
    SELECT 1
    FROM servicios
    WHERE nombre = 'Paquete Jardín'
);

INSERT INTO servicios (nombre, categoria, descripcion, precio_base, activo)
SELECT
    'Paquete Piscina + Jardín',
    'Combinado',
    'Incluye todas las tareas del paquete Piscina y del paquete Jardín en una sola visita, con un precio especial.',
    0,
    TRUE
WHERE NOT EXISTS (
    SELECT 1
    FROM servicios
    WHERE nombre = 'Paquete Piscina + Jardín'
);

SELECT id_servicio, nombre, categoria, descripcion, precio_base, activo
FROM servicios
WHERE nombre IN (
    'Paquete Piscina',
    'Paquete Jardín',
    'Paquete Piscina + Jardín'
)
ORDER BY id_servicio;
