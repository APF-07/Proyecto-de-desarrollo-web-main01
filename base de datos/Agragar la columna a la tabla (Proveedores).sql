USE INVENTARIO;
GO

-- 1. Agregamos la columna a la tabla
ALTER TABLE Proveedores ADD tipo_producto NVARCHAR(255);
GO

-- 2. Ponemos un valor por defecto a los actuales para que no se vea vacío
UPDATE Proveedores SET tipo_producto = 'Granos y Cereales' WHERE tipo_producto IS NULL;
GO

-- 3. Actualizamos el procedimiento de LISTAR
CREATE OR ALTER PROCEDURE sp_ObtenerProveedores
AS
BEGIN
    SELECT id_proveedor, nombre, telefono, direccion, correo, tipo_producto
    FROM Proveedores
    ORDER BY id_proveedor DESC
END
GO

-- 4. Actualizamos el procedimiento de BUSCAR POR ID
CREATE OR ALTER PROCEDURE sp_ObtenerProveedorPorId
    @id_proveedor INT
AS
BEGIN
    SELECT id_proveedor, nombre, telefono, direccion, correo, tipo_producto
    FROM Proveedores
    WHERE id_proveedor = @id_proveedor
END
GO

-- 5. Actualizamos el procedimiento de AGREGAR
CREATE OR ALTER PROCEDURE sp_AgregarProveedor
    @nombre NVARCHAR(100),
    @telefono NVARCHAR(20),
    @direccion NVARCHAR(255),
    @correo NVARCHAR(100),
    @tipo_producto NVARCHAR(255) -- Nuevo parámetro
AS
BEGIN
    INSERT INTO Proveedores (nombre, telefono, direccion, correo, tipo_producto)
    VALUES (@nombre, @telefono, @direccion, @correo, @tipo_producto)
END
GO

-- 6. Actualizamos el procedimiento de ACTUALIZAR
CREATE OR ALTER PROCEDURE sp_ActualizarProveedor
    @id_proveedor INT,
    @nombre NVARCHAR(100),
    @telefono NVARCHAR(20),
    @direccion NVARCHAR(255),
    @correo NVARCHAR(100),
    @tipo_producto NVARCHAR(255) -- Nuevo parámetro
AS
BEGIN
    UPDATE Proveedores
    SET nombre = @nombre, 
        telefono = @telefono, 
        direccion = @direccion, 
        correo = @correo,
        tipo_producto = @tipo_producto
    WHERE id_proveedor = @id_proveedor
END
GO