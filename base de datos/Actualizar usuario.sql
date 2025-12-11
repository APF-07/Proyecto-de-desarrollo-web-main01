USE INVENTARIO;
GO

CREATE OR ALTER PROCEDURE sp_ActualizarUsuario
    @id_usuario INT,
    @nombre NVARCHAR(100),
    @correo NVARCHAR(100),
    @password NVARCHAR(255)
AS
BEGIN
    -- Validar que el correo no esté duplicado (excepto si es el mismo usuario)
    IF EXISTS (SELECT 1 FROM Usuarios WHERE correo = @correo AND id_usuario != @id_usuario)
    BEGIN
        RAISERROR('El correo ya está en uso por otro usuario.', 16, 1);
        RETURN;
    END

    UPDATE Usuarios
    SET nombre = @nombre, correo = @correo, contraseña = @password
    WHERE id_usuario = @id_usuario;
END
GO