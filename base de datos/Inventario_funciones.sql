use INVENTARIO
go

-- =========================================================
--                      PROCEDIMIENTOS
-- ===========================================================

-- 1. Agregar producto (sin usar id_usuario)
CREATE OR ALTER PROCEDURE sp_AgregarProducto
    @nombre NVARCHAR(100),
    @id_categoria INT,
    @id_proveedor INT,
    @unidad_medida NVARCHAR(50),
    @stock_inicial DECIMAL(10,2),
    @stock_minimo DECIMAL(10,2),
    @precio_unitario DECIMAL(10,2)
AS
BEGIN
    INSERT INTO Productos (nombre, id_categoria, id_proveedor, unidad_medida, stock_actual, stock_minimo, precio_unitario)
    VALUES (@nombre, @id_categoria, @id_proveedor, @unidad_medida, @stock_inicial, @stock_minimo, @precio_unitario);

    DECLARE @id_producto INT = SCOPE_IDENTITY();
    
    -- Movimiento con NULL en id_usuario
    INSERT INTO Cambios_Inventario (id_producto, tipo_movimiento, cantidad, id_usuario, observaciones)
    VALUES (@id_producto, 'Entrada', @stock_inicial, NULL, 'Stock inicial del producto');

    PRINT '✅ Producto agregado y movimiento registrado correctamente.';
END;
GO

-- 2. Obtener todos los productos con detalles
CREATE OR ALTER PROCEDURE sp_ObtenerProductos
AS
BEGIN
    SELECT 
        p.id_producto,
        p.nombre,
        c.nombre AS categoria,
        pr.nombre AS proveedor,
        p.unidad_medida,
        p.stock_actual,
        p.stock_minimo,
        p.precio_unitario,
        p.estado
    FROM Productos p
    INNER JOIN Categorias c ON p.id_categoria = c.id_categoria
    INNER JOIN Proveedores pr ON p.id_proveedor = pr.id_proveedor
    ORDER BY p.id_producto DESC
END
GO

-- 3. Obtener un producto por ID
CREATE OR ALTER PROCEDURE sp_ObtenerProductoPorId
    @id_producto INT
AS
BEGIN
    SELECT 
        id_producto,
        nombre,
        id_categoria,
        id_proveedor,
        unidad_medida,
        stock_actual,
        stock_minimo,
        precio_unitario,
        estado
    FROM Productos
    WHERE id_producto = @id_producto
END
GO

-- 4. Actualizar producto (sin modificar stock)
CREATE OR ALTER PROCEDURE sp_ActualizarProducto
    @id_producto INT,
    @nombre NVARCHAR(100),
    @id_categoria INT,
    @id_proveedor INT,
    @unidad_medida NVARCHAR(50),
    @stock_minimo DECIMAL(10,2),
    @precio_unitario DECIMAL(10,2)
AS
BEGIN
    UPDATE Productos
    SET 
        nombre = @nombre,
        id_categoria = @id_categoria,
        id_proveedor = @id_proveedor,
        unidad_medida = @unidad_medida,
        stock_minimo = @stock_minimo,
        precio_unitario = @precio_unitario
    WHERE id_producto = @id_producto
    
    IF @@ROWCOUNT > 0
        PRINT '✅ Producto actualizado correctamente'
    ELSE
        RAISERROR('❌ Producto no encontrado', 16, 1)
END
GO

-- 5. Cambiar estado del producto
CREATE OR ALTER PROCEDURE sp_CambiarEstadoProducto
    @id_producto INT,
    @nuevo_estado NVARCHAR(20)
AS
BEGIN
    IF @nuevo_estado NOT IN ('Activo', 'Inactivo')
    BEGIN
        RAISERROR('❌ Estado inválido. Use "Activo" o "Inactivo"', 16, 1)
        RETURN
    END

    UPDATE Productos
    SET estado = @nuevo_estado
    WHERE id_producto = @id_producto
    
    IF @@ROWCOUNT > 0
        PRINT '✅ Estado cambiado correctamente'
    ELSE
        RAISERROR('❌ Producto no encontrado', 16, 1)
END
GO

-- ============================================================
--  PROCEDIMIENTOS PARA CATEGORÍAS
-- ============================================================

CREATE OR ALTER PROCEDURE sp_ObtenerCategorias
AS
BEGIN
    SELECT id_categoria, nombre, descripcion
    FROM Categorias
    ORDER BY id_categoria DESC
END
GO

CREATE OR ALTER PROCEDURE sp_ObtenerCategoriaPorId
    @id_categoria INT
AS
BEGIN
    SELECT id_categoria, nombre, descripcion
    FROM Categorias
    WHERE id_categoria = @id_categoria
END
GO

CREATE OR ALTER PROCEDURE sp_AgregarCategoria
    @nombre NVARCHAR(100),
    @descripcion NVARCHAR(255)
AS
BEGIN
    INSERT INTO Categorias (nombre, descripcion)
    VALUES (@nombre, @descripcion)
    
    PRINT '✅ Categoría agregada correctamente'
END
GO

CREATE OR ALTER PROCEDURE sp_ActualizarCategoria
    @id_categoria INT,
    @nombre NVARCHAR(100),
    @descripcion NVARCHAR(255)
AS
BEGIN
    UPDATE Categorias
    SET nombre = @nombre, descripcion = @descripcion
    WHERE id_categoria = @id_categoria
    
    IF @@ROWCOUNT > 0
        PRINT '✅ Categoría actualizada correctamente'
    ELSE
        RAISERROR('❌ Categoría no encontrada', 16, 1)
END
GO

CREATE OR ALTER PROCEDURE sp_EliminarCategoria
    @id_categoria INT
AS
BEGIN
    -- Validar que no tenga productos asociados
    IF EXISTS (SELECT 1 FROM Productos WHERE id_categoria = @id_categoria)
    BEGIN
        RAISERROR('❌ No se puede eliminar. Existen productos con esta categoría', 16, 1)
        RETURN
    END

    DELETE FROM Categorias WHERE id_categoria = @id_categoria
    
    IF @@ROWCOUNT > 0
        PRINT '✅ Categoría eliminada correctamente'
    ELSE
        RAISERROR('❌ Categoría no encontrada', 16, 1)
END
GO

-- ============================================================
--  PROCEDIMIENTOS PARA PROVEEDORES
-- ============================================================

CREATE OR ALTER PROCEDURE sp_ObtenerProveedores
AS
BEGIN
    SELECT id_proveedor, nombre, telefono, direccion, correo
    FROM Proveedores
    ORDER BY id_proveedor DESC
END
GO

CREATE OR ALTER PROCEDURE sp_ObtenerProveedorPorId
    @id_proveedor INT
AS
BEGIN
    SELECT id_proveedor, nombre, telefono, direccion, correo
    FROM Proveedores
    WHERE id_proveedor = @id_proveedor
END
GO

CREATE OR ALTER PROCEDURE sp_AgregarProveedor
    @nombre NVARCHAR(100),
    @telefono NVARCHAR(20),
    @direccion NVARCHAR(255),
    @correo NVARCHAR(100)
AS
BEGIN
    INSERT INTO Proveedores (nombre, telefono, direccion, correo)
    VALUES (@nombre, @telefono, @direccion, @correo)
    
    PRINT '✅ Proveedor agregado correctamente'
END
GO

CREATE OR ALTER PROCEDURE sp_ActualizarProveedor
    @id_proveedor INT,
    @nombre NVARCHAR(100),
    @telefono NVARCHAR(20),
    @direccion NVARCHAR(255),
    @correo NVARCHAR(100)
AS
BEGIN
    UPDATE Proveedores
    SET nombre = @nombre, telefono = @telefono, 
        direccion = @direccion, correo = @correo
    WHERE id_proveedor = @id_proveedor
    
    IF @@ROWCOUNT > 0
        PRINT '✅ Proveedor actualizado correctamente'
    ELSE
        RAISERROR('❌ Proveedor no encontrado', 16, 1)
END
GO

CREATE OR ALTER PROCEDURE sp_EliminarProveedor
    @id_proveedor INT
AS
BEGIN
    -- Validar que no tenga productos asociados
    IF EXISTS (SELECT 1 FROM Productos WHERE id_proveedor = @id_proveedor)
    BEGIN
        RAISERROR('❌ No se puede eliminar. Existen productos de este proveedor', 16, 1)
        RETURN
    END

    DELETE FROM Proveedores WHERE id_proveedor = @id_proveedor
    
    IF @@ROWCOUNT > 0
        PRINT '✅ Proveedor eliminado correctamente'
    ELSE
        RAISERROR('❌ Proveedor no encontrado', 16, 1)
END
GO

-- ============================================================
--  PROCEDIMIENTOS PARA CLIENTES
-- ============================================================

CREATE OR ALTER PROCEDURE sp_ObtenerClientes
AS
BEGIN
    SELECT id_cliente, nombre, telefono, direccion, correo
    FROM Clientes
    ORDER BY id_cliente DESC
END
GO

CREATE OR ALTER PROCEDURE sp_ObtenerClientePorId
    @id_cliente INT
AS
BEGIN
    SELECT id_cliente, nombre, telefono, direccion, correo
    FROM Clientes
    WHERE id_cliente = @id_cliente
END
GO

CREATE OR ALTER PROCEDURE sp_AgregarCliente
    @nombre NVARCHAR(100),
    @telefono NVARCHAR(20),
    @direccion NVARCHAR(255),
    @correo NVARCHAR(100)
AS
BEGIN
    INSERT INTO Clientes (nombre, telefono, direccion, correo)
    VALUES (@nombre, @telefono, @direccion, @correo)
    
    PRINT '✅ Cliente agregado correctamente'
END
GO

CREATE OR ALTER PROCEDURE sp_ActualizarCliente
    @id_cliente INT,
    @nombre NVARCHAR(100),
    @telefono NVARCHAR(20),
    @direccion NVARCHAR(255),
    @correo NVARCHAR(100)
AS
BEGIN
    UPDATE Clientes
    SET nombre = @nombre, telefono = @telefono,
        direccion = @direccion, correo = @correo
    WHERE id_cliente = @id_cliente
    
    IF @@ROWCOUNT > 0
        PRINT '✅ Cliente actualizado correctamente'
    ELSE
        RAISERROR('❌ Cliente no encontrado', 16, 1)
END
GO

CREATE OR ALTER PROCEDURE sp_EliminarCliente
    @id_cliente INT
AS
BEGIN
    -- Validar que no tenga ventas asociadas
    IF EXISTS (SELECT 1 FROM Ventas WHERE id_cliente = @id_cliente)
    BEGIN
        RAISERROR('❌ No se puede eliminar. El cliente tiene ventas registradas', 16, 1)
        RETURN
    END

    DELETE FROM Clientes WHERE id_cliente = @id_cliente
    
    IF @@ROWCOUNT > 0
        PRINT '✅ Cliente eliminado correctamente'
    ELSE
        RAISERROR('❌ Cliente no encontrado', 16, 1)
END
GO

-- ============================================================
--  PROCEDIMIENTOS PARA MOVIMIENTOS DE INVENTARIO
-- ============================================================

CREATE OR ALTER PROCEDURE sp_RegistrarMovimientoSimple
    @id_producto INT,
    @tipo_movimiento NVARCHAR(20),
    @cantidad DECIMAL(10,2),
    @observaciones NVARCHAR(255) = NULL
AS
BEGIN
    SET NOCOUNT ON
    
    BEGIN TRY
        -- Validar tipo de movimiento
        IF @tipo_movimiento NOT IN ('Entrada', 'Salida')
            RAISERROR('Tipo de movimiento inválido', 16, 1)

        -- Validar que el producto existe
        IF NOT EXISTS (SELECT 1 FROM Productos WHERE id_producto = @id_producto)
            RAISERROR('Producto no encontrado', 16, 1)

        DECLARE @stock_actual DECIMAL(10,2)
        SELECT @stock_actual = stock_actual FROM Productos WHERE id_producto = @id_producto

        -- Validar stock para salidas
        IF @tipo_movimiento = 'Salida' AND @cantidad > @stock_actual
            RAISERROR('Stock insuficiente', 16, 1)

        BEGIN TRANSACTION

        -- Registrar movimiento
        INSERT INTO Cambios_Inventario (id_producto, tipo_movimiento, cantidad, observaciones)
        VALUES (@id_producto, @tipo_movimiento, @cantidad, @observaciones)

        -- Actualizar stock
        IF @tipo_movimiento = 'Entrada'
            UPDATE Productos SET stock_actual = stock_actual + @cantidad WHERE id_producto = @id_producto
        ELSE
            UPDATE Productos SET stock_actual = stock_actual - @cantidad WHERE id_producto = @id_producto

        COMMIT TRANSACTION

    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION
        ;THROW
    END CATCH
END
GO

-- Obtener movimientos con filtros opcionales
CREATE OR ALTER PROCEDURE sp_ObtenerMovimientos
    @fecha_inicio DATETIME = NULL,
    @fecha_fin DATETIME = NULL,
    @tipo_movimiento NVARCHAR(20) = NULL
AS
BEGIN
    SELECT 
        m.id_movimiento,
        p.nombre AS producto,
        m.tipo_movimiento,
        m.cantidad,
        m.fecha_movimiento,
        m.observaciones
    FROM Cambios_Inventario m
    INNER JOIN Productos p ON m.id_producto = p.id_producto
    WHERE 
        (@fecha_inicio IS NULL OR m.fecha_movimiento >= @fecha_inicio)
        AND (@fecha_fin IS NULL OR m.fecha_movimiento <= @fecha_fin)
        AND (@tipo_movimiento IS NULL OR m.tipo_movimiento = @tipo_movimiento)
    ORDER BY m.fecha_movimiento DESC
END
GO

-- ============================================================
--  PROCEDIMIENTOS PARA VENTAS
-- ============================================================

CREATE OR ALTER PROCEDURE sp_RegistrarVenta
    @id_cliente INT,
    @detalle NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;

        DECLARE @id_venta INT;
        DECLARE @total DECIMAL(10,2) = 0;

        -- Calcular el total directamente desde el JSON
        SELECT @total = SUM(d.cantidad * p.precio_unitario)
        FROM OPENJSON(@detalle)
        WITH (
            id_producto INT,
            cantidad DECIMAL(10,2)
        ) d
        INNER JOIN Productos p ON d.id_producto = p.id_producto;

        -- Insertar la venta (sin usuario)
        INSERT INTO Ventas (id_cliente, id_usuario, total, tipo_venta)
        VALUES (@id_cliente, NULL, @total, 'Venta');

        SET @id_venta = SCOPE_IDENTITY();

        -- Insertar detalles
        INSERT INTO Detalle_venta (id_venta, id_producto, cantidad, precio_unitario)
        SELECT 
            @id_venta,
            d.id_producto,
            d.cantidad,
            p.precio_unitario
        FROM OPENJSON(@detalle)
        WITH (
            id_producto INT,
            cantidad DECIMAL(10,2)
        ) d
        INNER JOIN Productos p ON d.id_producto = p.id_producto;

        -- Actualizar stock y registrar movimientos
        INSERT INTO Cambios_Inventario (id_producto, tipo_movimiento, cantidad, observaciones)
        SELECT 
            d.id_producto,
            'Salida',
            d.cantidad,
            'Venta #' + CAST(@id_venta AS NVARCHAR(10))
        FROM OPENJSON(@detalle)
        WITH (
            id_producto INT,
            cantidad DECIMAL(10,2)
        ) d;

        UPDATE p
        SET p.stock_actual = p.stock_actual - d.cantidad
        FROM Productos p
        INNER JOIN (
            SELECT id_producto, cantidad
            FROM OPENJSON(@detalle)
            WITH (id_producto INT, cantidad DECIMAL(10,2))
        ) d ON p.id_producto = d.id_producto;

        COMMIT TRANSACTION;
        PRINT '✅ Venta registrada correctamente. ID: ' + CAST(@id_venta AS NVARCHAR(10));
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();
        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END;
GO

CREATE OR ALTER PROCEDURE sp_ObtenerVentaPorId
    @id_venta INT
AS
BEGIN
    -- Encabezado de la venta
    SELECT 
        v.id_venta,
        c.nombre AS cliente,
        v.fecha_venta,
        v.total,
        v.tipo_venta,
        v.observaciones
    FROM Ventas v
    INNER JOIN Clientes c ON v.id_cliente = c.id_cliente
    WHERE v.id_venta = @id_venta;

    -- Detalles de la venta
    SELECT 
        p.nombre AS producto,
        d.cantidad,
        d.precio_unitario,
        d.subtotal
    FROM Detalle_venta d
    INNER JOIN Productos p ON d.id_producto = p.id_producto
    WHERE d.id_venta = @id_venta;
END;
GO

-- Obtener ventas con filtros
CREATE OR ALTER PROCEDURE sp_ObtenerVentasFiltradas
    @fecha_inicio DATETIME = NULL,
    @fecha_fin DATETIME = NULL,
    @id_cliente INT = NULL
AS
BEGIN
    SELECT 
        v.id_venta,
        c.nombre AS cliente,
        v.fecha_venta,
        v.total,
        v.observaciones
    FROM Ventas v
    INNER JOIN Clientes c ON v.id_cliente = c.id_cliente
    WHERE v.tipo_venta = 'Venta'
        AND (@fecha_inicio IS NULL OR v.fecha_venta >= @fecha_inicio)
        AND (@fecha_fin IS NULL OR v.fecha_venta <= @fecha_fin)
        AND (@id_cliente IS NULL OR v.id_cliente = @id_cliente)
    ORDER BY v.fecha_venta DESC
END
GO

-- Procedimiento para obtener reporte de ventas por período
CREATE OR ALTER PROCEDURE sp_ReporteVentasPorPeriodo
    @fecha_inicio DATETIME,
    @fecha_fin DATETIME
AS
BEGIN
    SELECT 
        v.id_venta,
        c.nombre AS cliente,
        v.fecha_venta,
        v.total,
        COUNT(d.id_detalle) AS cantidad_productos
    FROM Ventas v
    INNER JOIN Clientes c ON v.id_cliente = c.id_cliente
    INNER JOIN Detalle_venta d ON v.id_venta = d.id_venta
    WHERE v.fecha_venta BETWEEN @fecha_inicio AND @fecha_fin
    GROUP BY v.id_venta, c.nombre, v.fecha_venta, v.total
    ORDER BY v.fecha_venta DESC
END
GO

-- ============================================================
--  NUEVOS PROCEDIMIENTOS PARA CONSULTAS DIRECTAS
-- ============================================================

-- Para obtener lista de ventas (reemplaza consulta directa)
CREATE OR ALTER PROCEDURE sp_ObtenerVentasLista
AS
BEGIN
    SELECT 
        v.id_venta,
        c.nombre AS cliente,
        v.fecha_venta,
        v.total,
        v.tipo_venta,
        v.observaciones
    FROM Ventas v
    INNER JOIN Clientes c ON v.id_cliente = c.id_cliente
    ORDER BY v.fecha_venta DESC
END
GO

-- Para obtener usuarios activos (sin usuario específico)
CREATE OR ALTER PROCEDURE sp_ObtenerUsuariosActivos
AS
BEGIN
    SELECT id_usuario, nombre 
    FROM Usuarios 
    WHERE activo = 1 
    ORDER BY nombre
END
GO

-- Para obtener productos disponibles para venta
CREATE OR ALTER PROCEDURE sp_ObtenerProductosParaVenta
AS
BEGIN
    SELECT id_producto, nombre, stock_actual, precio_unitario 
    FROM Productos 
    WHERE estado = 'Activo' AND stock_actual > 0
    ORDER BY nombre
END
GO

-- Para obtener detalles de una venta específica
CREATE OR ALTER PROCEDURE sp_ObtenerDetallesVenta
    @id_venta INT
AS
BEGIN
    SELECT 
        p.nombre AS producto,
        d.cantidad,
        d.precio_unitario,
        d.subtotal
    FROM Detalle_venta d
    INNER JOIN Productos p ON d.id_producto = p.id_producto
    WHERE d.id_venta = @id_venta
END
GO

-- ============================================================
--  PROCEDIMIENTOS PARA DASHBOARD/REPORTES
-- ============================================================

CREATE OR ALTER PROCEDURE sp_ObtenerTotalProductos
AS
BEGIN
    SELECT COUNT(*) as total FROM Productos WHERE estado = 'Activo'
END
GO

CREATE OR ALTER PROCEDURE sp_ObtenerTotalVentas
AS
BEGIN
    SELECT COUNT(*) as total FROM Ventas
END
GO

CREATE OR ALTER PROCEDURE sp_ObtenerTotalClientes
AS
BEGIN
    SELECT COUNT(*) as total FROM Clientes
END
GO

CREATE OR ALTER PROCEDURE sp_ObtenerVentasUltimosMeses
    @meses INT
AS
BEGIN
    SELECT 
        FORMAT(fecha_venta, 'yyyy-MM') as mes,
        COUNT(*) as cantidad_ventas,
        ISNULL(SUM(total), 0) as total_ventas
    FROM Ventas 
    WHERE fecha_venta >= DATEADD(MONTH, -@meses, GETDATE())
    GROUP BY FORMAT(fecha_venta, 'yyyy-MM')
    ORDER BY mes
END
GO

CREATE OR ALTER PROCEDURE sp_ObtenerProductosMasVendidos
    @limite INT
AS
BEGIN
    SELECT TOP (@limite)
        p.nombre,
        ISNULL(SUM(d.cantidad), 0) as total_vendido,
        ISNULL(SUM(d.subtotal), 0) as total_ingresos
    FROM Detalle_venta d
    INNER JOIN Productos p ON d.id_producto = p.id_producto
    GROUP BY p.nombre
    ORDER BY total_vendido DESC
END
GO

CREATE OR ALTER PROCEDURE sp_ObtenerProductosStockBajo
AS
BEGIN
    SELECT nombre, stock_actual, stock_minimo
    FROM Productos 
    WHERE estado = 'Activo' AND stock_actual <= stock_minimo
    ORDER BY (stock_minimo - stock_actual) DESC
END
GO

-- ===============================================
--                  VISTAS
-- ===============================================

-- 4. Vista de productos bajo mínimo
CREATE OR ALTER VIEW vw_ProductosBajoMinimo AS
SELECT 
    p.id_producto,
    p.nombre,
    p.stock_actual,
    p.stock_minimo,
    c.nombre AS categoria,
    pr.nombre AS proveedor
FROM Productos p
JOIN Categorias c ON p.id_categoria = c.id_categoria
JOIN Proveedores pr ON p.id_proveedor = pr.id_proveedor
WHERE p.stock_actual < p.stock_minimo;
GO

-- 5. Resumen inventario
CREATE OR ALTER VIEW vw_ResumenInventario AS
SELECT 
    p.id_producto,
    p.nombre AS producto,
    c.nombre AS categoria,
    pr.nombre AS proveedor,
    p.stock_actual,
    p.stock_minimo,
    p.unidad_medida,
    p.precio_unitario,
    (p.stock_actual * p.precio_unitario) AS valor_total
FROM Productos p
JOIN Categorias c ON p.id_categoria = c.id_categoria
JOIN Proveedores pr ON p.id_proveedor = pr.id_proveedor;
GO

-- ===============================================
--                  TRIGGERS
-- ===============================================

CREATE OR ALTER TRIGGER tr_ValidarStock_Venta
ON Detalle_venta
FOR INSERT
AS
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM inserted i 
        JOIN Productos p ON i.id_producto = p.id_producto 
        WHERE i.cantidad > p.stock_actual
    )
    BEGIN
        RAISERROR('❌ Stock insuficiente para completar la venta', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
GO

PRINT '✅ Todos los procedimientos almacenados han sido actualizados correctamente'
PRINT '📊 Total: 36 procedimientos almacenados, 2 vistas y 1 trigger'
GO