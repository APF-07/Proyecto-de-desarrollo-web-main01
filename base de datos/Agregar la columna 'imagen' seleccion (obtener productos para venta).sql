USE INVENTARIO;
GO

CREATE OR ALTER PROCEDURE sp_ObtenerProductosParaVenta
AS
BEGIN
    -- Agregamos la columna 'imagen' a la selección
    SELECT id_producto, nombre, stock_actual, precio_unitario, imagen 
    FROM Productos 
    WHERE estado = 'Activo' AND stock_actual > 0
    ORDER BY nombre
END
GO