USE INVENTARIO;
GO

-- 1. Agregar la columna 'imagen' a la tabla Productos
ALTER TABLE Productos ADD imagen NVARCHAR(255) DEFAULT NULL;
GO

-- 2. Actualizar el procedimiento de AGREGAR
CREATE OR ALTER PROCEDURE sp_AgregarProducto
    @nombre NVARCHAR(100),
    @id_categoria INT,
    @id_proveedor INT,
    @unidad_medida NVARCHAR(50),
    @stock_inicial DECIMAL(10,2),
    @stock_minimo DECIMAL(10,2),
    @precio_unitario DECIMAL(10,2),
    @imagen NVARCHAR(255) = NULL
AS
BEGIN
    INSERT INTO Productos (nombre, id_categoria, id_proveedor, unidad_medida, stock_actual, stock_minimo, precio_unitario, imagen)
    VALUES (@nombre, @id_categoria, @id_proveedor, @unidad_medida, @stock_inicial, @stock_minimo, @precio_unitario, @imagen);

    DECLARE @id_producto INT = SCOPE_IDENTITY();
    
    INSERT INTO Cambios_Inventario (id_producto, tipo_movimiento, cantidad, id_usuario, observaciones)
    VALUES (@id_producto, 'Entrada', @stock_inicial, NULL, 'Stock inicial del producto');
END;
GO

-- 3. Actualizar el procedimiento de ACTUALIZAR
CREATE OR ALTER PROCEDURE sp_ActualizarProducto
    @id_producto INT,
    @nombre NVARCHAR(100),
    @id_categoria INT,
    @id_proveedor INT,
    @unidad_medida NVARCHAR(50),
    @stock_minimo DECIMAL(10,2),
    @precio_unitario DECIMAL(10,2),
    @imagen NVARCHAR(255) = NULL
AS
BEGIN
    UPDATE Productos
    SET 
        nombre = @nombre,
        id_categoria = @id_categoria,
        id_proveedor = @id_proveedor,
        unidad_medida = @unidad_medida,
        stock_minimo = @stock_minimo,
        precio_unitario = @precio_unitario,
        imagen = ISNULL(@imagen, imagen) -- Mantiene la foto anterior si no suben una nueva
    WHERE id_producto = @id_producto
END
GO

-- 4. Actualizar el procedimiento de OBTENER (Listar)
CREATE OR ALTER PROCEDURE sp_ObtenerProductos
AS
BEGIN
    SELECT 
        p.id_producto, p.nombre, c.nombre AS categoria, pr.nombre AS proveedor,
        p.unidad_medida, p.stock_actual, p.stock_minimo, p.precio_unitario, p.estado,
        p.imagen -- Agregamos la columna imagen
    FROM Productos p
    INNER JOIN Categorias c ON p.id_categoria = c.id_categoria
    INNER JOIN Proveedores pr ON p.id_proveedor = pr.id_proveedor
    ORDER BY p.id_producto DESC
END
GO

-- 5. Actualizar el procedimiento de OBTENER POR ID
CREATE OR ALTER PROCEDURE sp_ObtenerProductoPorId
    @id_producto INT
AS
BEGIN
    SELECT id_producto, nombre, id_categoria, id_proveedor, unidad_medida, 
           stock_actual, stock_minimo, precio_unitario, estado, imagen
    FROM Productos WHERE id_producto = @id_producto
END
GO