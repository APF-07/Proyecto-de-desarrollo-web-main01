use master
go

drop database if exists INVENTARIO
go

create database INVENTARIO
go

use INVENTARIO
go

-- Tabla Usuarios
CREATE TABLE Usuarios (
    id_usuario INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    correo NVARCHAR(100) UNIQUE NOT NULL,
    contraseña NVARCHAR(255) NOT NULL,
    rol NVARCHAR(50) DEFAULT 'Usuario',
    fecha_registro DATETIME DEFAULT GETDATE(),
    activo BIT DEFAULT 1
);

INSERT INTO Usuarios (nombre, correo, contraseña, rol)
VALUES 
('Administrador', 'admin@sistema.com', 'admin123', 'Administrador'),
('Vendedor 1', 'vendedor1@sistema.com', 'vendedor123', 'Vendedor'),
('Almacenero', 'almacen@sistema.com', 'almacen123', 'Almacen');

CREATE TABLE Categorias (
    id_categoria INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    descripcion NVARCHAR(255)
);

INSERT INTO Categorias (nombre, descripcion) VALUES
('Cereales andinos', 'Productos como quinua, kiwicha, cañihua, maíz serrano.'),
('Legumbres secas', 'Frijol, lenteja, arveja, habas en estado seco.'),
('Semillas para siembra', 'Semillas seleccionadas para cultivo agrícola.'),
('Productos frescos', 'Legumbres y cereales en estado fresco o recién cosechados.'),
('Derivados procesados', 'Harinas, hojuelas, tostados, mezclas listas para consumo.'),
('Insumos agrícolas', 'Fertilizantes orgánicos, abonos, herramientas menores.'),
('Empaques y envases', 'Sacos, bolsas, frascos utilizados para comercialización.');

CREATE TABLE Proveedores (
    id_proveedor INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    telefono NVARCHAR(20),
    direccion NVARCHAR(255),
    correo NVARCHAR(100)
);

INSERT INTO Proveedores (nombre, telefono, direccion, correo) VALUES
('AgroAndes SAC', '+51 987 654 321', 'Jr. Los Incas 123, Huancayo, Junín', 'contacto@agroandes.pe'),
('Semillas del Sur', '+51 956 321 789', 'Av. Libertad 456, Ayacucho', 'ventas@semillasdelsur.com'),
('BioFert Perú', '+51 945 678 123', 'Calle Pachamama 89, Cusco', 'info@biofertperu.org'),
('Empaques Sierra Verde', '+51 923 456 789', 'Jr. Comercio 77, Huancavelica', 'servicio@sierraverde.pe'),
('Legumbres Selectas EIRL', '+51 912 345 678', 'Av. Central 101, Abancay', 'legumbres@selectas.com'),
('CerealCo Andino', '+51 999 888 777', 'Calle Quinoa 22, Cerro de Pasco', 'cereales@cerealco.pe');

CREATE TABLE Productos (
    id_producto INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    id_categoria INT FOREIGN KEY REFERENCES Categorias(id_categoria),
    id_proveedor INT FOREIGN KEY REFERENCES Proveedores(id_proveedor),
    unidad_medida NVARCHAR(50) NOT NULL,
    stock_actual DECIMAL(10,2) DEFAULT 0,
    stock_minimo DECIMAL(10,2) DEFAULT 0,
    precio_unitario DECIMAL(10,2) NOT NULL,
    fecha_registro DATETIME DEFAULT GETDATE(),
    estado NVARCHAR(20) DEFAULT 'Activo'
);

INSERT INTO Productos (nombre, id_categoria, id_proveedor, unidad_medida, stock_actual, stock_minimo, precio_unitario)
VALUES
-- Cereales andinos
('Quinua blanca', 1, 1, 'kg', 120.00, 30.00, 6.50),
('Kiwicha orgánica', 1, 2, 'kg', 80.00, 20.00, 7.20),
('Cañihua tostada', 1, 6, 'kg', 50.00, 15.00, 5.80),
('Maíz morado serrano', 1, 1, 'saco', 10.00, 3.00, 95.00),
('Maíz blanco tipo Cusco', 1, 3, 'qq', 5.00, 2.00, 120.00),
('Quinua roja', 1, 2, 'kg', 60.00, 10.00, 7.80),
('Cebada perlada', 1, 5, 'kg', 40.00, 10.00, 4.90),
-- Legumbres secas
('Frijol serrano', 2, 5, 'kg', 70.00, 20.00, 6.00),
('Haba seca', 2, 4, 'kg', 45.00, 10.00, 5.20);

CREATE TABLE Clientes (
    id_cliente INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    telefono NVARCHAR(20),
    direccion NVARCHAR(255),
    correo NVARCHAR(100)
);

-- Insertar clientes de ejemplo
INSERT INTO Clientes (nombre, telefono, direccion, correo) VALUES
('Cliente General', '+51 123 456 789', 'Dirección general', 'cliente@general.com'),
('Restaurante Andino', '+51 987 654 321', 'Av. Principal 123', 'pedidos@restauranteandino.com'),
('Tienda Natural', '+51 955 444 333', 'Jr. Salud 456', 'contacto@tiendanatural.pe'),
('Mercado Central', '+51 966 777 888', 'Mercado Central Puesto 45', 'mercado@central.com');

CREATE TABLE Ventas (
    id_venta INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NULL FOREIGN KEY REFERENCES Usuarios(id_usuario), -- Permitir NULL
    id_cliente INT FOREIGN KEY REFERENCES Clientes(id_cliente),
    fecha_venta DATETIME DEFAULT GETDATE(),
    total DECIMAL(10,2) DEFAULT 0,
    tipo_venta NVARCHAR(20) DEFAULT 'Venta',
    observaciones NVARCHAR(255)
);

CREATE TABLE Detalle_venta (
    id_detalle INT IDENTITY(1,1) PRIMARY KEY,
    id_venta INT FOREIGN KEY REFERENCES Ventas(id_venta),
    id_producto INT FOREIGN KEY REFERENCES Productos(id_producto),
    cantidad DECIMAL(10,2) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal AS (cantidad * precio_unitario) PERSISTED
);

CREATE TABLE Cambios_Inventario (
    id_movimiento INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NULL FOREIGN KEY REFERENCES Usuarios(id_usuario), -- Permitir NULL
    id_producto INT FOREIGN KEY REFERENCES Productos(id_producto),
    tipo_movimiento NVARCHAR(20) CHECK (tipo_movimiento IN ('Entrada','Salida')),
    cantidad DECIMAL(10,2) NOT NULL,
    fecha_movimiento DATETIME DEFAULT GETDATE(),
    observaciones NVARCHAR(255)
);

-- Insertar algunos movimientos de ejemplo
INSERT INTO Cambios_Inventario (id_producto, tipo_movimiento, cantidad, observaciones)
VALUES
(1, 'Entrada', 100, 'Compra inicial'),
(2, 'Entrada', 80, 'Compra inicial'),
(3, 'Entrada', 50, 'Compra inicial');

PRINT '✅ Base de datos INVENTARIO creada correctamente con datos de ejemplo';