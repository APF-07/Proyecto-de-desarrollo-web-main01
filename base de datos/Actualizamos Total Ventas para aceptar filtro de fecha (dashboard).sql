USE INVENTARIO;
GO

-- 1. Actualizamos Total Ventas para aceptar filtro de fecha
CREATE OR ALTER PROCEDURE sp_ObtenerTotalVentas
    @fecha_inicio DATETIME = NULL
AS
BEGIN
    SELECT COUNT(*) as total 
    FROM Ventas
    WHERE (@fecha_inicio IS NULL OR fecha_venta >= @fecha_inicio)
END
GO

-- 2. Nuevo Procedimiento: Total Ganancias (Suma de dinero)
-- Esto es vital para el dashboard financiero
CREATE OR ALTER PROCEDURE sp_ObtenerTotalIngresos
    @fecha_inicio DATETIME = NULL
AS
BEGIN
    SELECT ISNULL(SUM(total), 0) as total
    FROM Ventas
    WHERE (@fecha_inicio IS NULL OR fecha_venta >= @fecha_inicio)
END
GO

-- 3. Actualizamos Productos Más Vendidos para aceptar fecha
CREATE OR ALTER PROCEDURE sp_ObtenerProductosMasVendidos
    @limite INT,
    @fecha_inicio DATETIME = NULL
AS
BEGIN
    SELECT TOP (@limite)
        p.nombre,
        ISNULL(SUM(d.cantidad), 0) as total_vendido,
        ISNULL(SUM(d.subtotal), 0) as total_ingresos
    FROM Detalle_venta d
    INNER JOIN Productos p ON d.id_producto = p.id_producto
    INNER JOIN Ventas v ON d.id_venta = v.id_venta -- Unimos con Ventas para ver la fecha
    WHERE (@fecha_inicio IS NULL OR v.fecha_venta >= @fecha_inicio)
    GROUP BY p.nombre
    ORDER BY total_vendido DESC
END
GO