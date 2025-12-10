from app.db import get_connection

# =====================================================
#   PRODUCTOS
# =====================================================

def obtener_productos():
    """Obtiene todos los productos usando sp_ObtenerProductos"""
    conn = get_connection()
    productos = []
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerProductos")
        
        for row in cursor.fetchall():
            productos.append({
                "id": row.id_producto,
                "nombre": row.nombre,
                "categoria": row.categoria,
                "proveedor": row.proveedor,
                "unidad": row.unidad_medida,
                "stock": float(row.stock_actual),
                "stock_minimo": float(row.stock_minimo),
                "precio": float(row.precio_unitario),
                "estado": row.estado,
                "imagen": row.imagen
            })
    finally:
        conn.close()
    return productos


def obtener_categorias():
    """Lista simple para dropdowns usando sp_ObtenerCategorias"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM Categorias ORDER BY nombre")
        return [{"id": r.id_categoria, "nombre": r.nombre} for r in cursor.fetchall()]
    finally:
        conn.close()


def obtener_proveedores():
    """Lista simple para dropdowns usando sp_ObtenerProveedores"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_proveedor, nombre FROM Proveedores ORDER BY nombre")
        return [{"id": r.id_proveedor, "nombre": r.nombre} for r in cursor.fetchall()]
    finally:
        conn.close()


def agregar_producto(nombre, id_categoria, id_proveedor, unidad, stock_inicial, stock_minimo, precio_unitario, imagen=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            EXEC sp_AgregarProducto 
                @nombre=?, @id_categoria=?, @id_proveedor=?, 
                @unidad_medida=?, @stock_inicial=?, @stock_minimo=?, @precio_unitario=?, @imagen=?
        """, (nombre, id_categoria, id_proveedor, unidad, stock_inicial, stock_minimo, precio_unitario, imagen))
        conn.commit()
        return True
    except Exception as e:
        print("Error al agregar producto:", e)
        return False
    finally:
        conn.close()


def obtener_producto_por_id(id_producto):
    """Obtiene un producto por ID usando sp_ObtenerProductoPorId"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerProductoPorId @id_producto=?", (id_producto,))
        
        row = cursor.fetchone()
        if not row:
            return None

        return {
            "id": row.id_producto,
            "nombre": row.nombre,
            "id_categoria": row.id_categoria,
            "id_proveedor": row.id_proveedor,
            "unidad": row.unidad_medida,
            "stock": float(row.stock_actual),
            "stock_minimo": float(row.stock_minimo),
            "precio": float(row.precio_unitario),
            "estado": row.estado
        }
    except Exception as e:
        print("Error en obtener_producto_por_id:", e)
        return None
    finally:
        conn.close()


def actualizar_producto(id_producto, nombre, id_categoria, id_proveedor, unidad, stock_minimo, precio, imagen=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            EXEC sp_ActualizarProducto
                @id_producto=?, @nombre=?, @id_categoria=?, @id_proveedor=?,
                @unidad_medida=?, @stock_minimo=?, @precio_unitario=?, @imagen=?
        """, (id_producto, nombre, id_categoria, id_proveedor, unidad, stock_minimo, precio, imagen))
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar producto:", e)
        return False
    finally:
        conn.close()


def eliminar_producto(id_producto):
    """Elimina (inactiva) producto usando sp_CambiarEstadoProducto"""
    return cambiar_estado_producto(id_producto, 'Inactivo')


def cambiar_estado_producto(id_producto, nuevo_estado):
    """Cambia estado usando sp_CambiarEstadoProducto"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_CambiarEstadoProducto @id_producto=?, @nuevo_estado=?", 
                      (id_producto, nuevo_estado))
        conn.commit()
        return True
    except Exception as e:
        print("Error al cambiar estado:", e)
        return False
    finally:
        conn.close()


# =====================================================
#   CATEGORÍAS
# =====================================================

def obtener_categorias_todas():
    """Obtiene todas las categorías con detalles usando sp_ObtenerCategorias"""
    conn = get_connection()
    categorias = []
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerCategorias")
        
        for row in cursor.fetchall():
            categorias.append({
                "id": row.id_categoria,
                "nombre": row.nombre,
                "descripcion": row.descripcion
            })
    finally:
        conn.close()
    return categorias


def agregar_categoria(nombre, descripcion):
    """Agrega categoría usando sp_AgregarCategoria"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_AgregarCategoria @nombre=?, @descripcion=?", 
                      (nombre, descripcion))
        conn.commit()
        return True
    except Exception as e:
        print("Error al agregar categoría:", e)
        return False
    finally:
        conn.close()


def obtener_categoria_por_id(id_categoria):
    """Obtiene una categoría por ID usando sp_ObtenerCategoriaPorId"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerCategoriaPorId @id_categoria=?", (id_categoria,))
        
        row = cursor.fetchone()
        if not row:
            return None
            
        return {
            "id": row.id_categoria,
            "nombre": row.nombre,
            "descripcion": row.descripcion
        }
    finally:
        conn.close()


def actualizar_categoria(id_categoria, nombre, descripcion):
    """Actualiza categoría usando sp_ActualizarCategoria"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ActualizarCategoria @id_categoria=?, @nombre=?, @descripcion=?",
                      (id_categoria, nombre, descripcion))
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar categoría:", e)
        return False
    finally:
        conn.close()


def eliminar_categoria(id_categoria):
    """Elimina categoría usando sp_EliminarCategoria"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_EliminarCategoria @id_categoria=?", (id_categoria,))
        conn.commit()
        return True
    except Exception as e:
        print("Error al eliminar categoría:", e)
        return False
    finally:
        conn.close()


# =====================================================
#   PROVEEDORES (ACTUALIZADO)
# =====================================================

def obtener_proveedores_todos():
    """Obtiene todos los proveedores incluyendo el tipo de producto"""
    conn = get_connection()
    proveedores = []
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerProveedores")
        
        for r in cursor.fetchall():
            proveedores.append({
                "id": r.id_proveedor,
                "nombre": r.nombre,
                "telefono": r.telefono,
                "direccion": r.direccion,
                "correo": r.correo,
                "tipo_producto": r.tipo_producto # <--- Nuevo campo
            })
    finally:
        conn.close()
    return proveedores


def agregar_proveedor(nombre, telefono, direccion, correo, tipo_producto): # <--- Nuevo argumento
    """Agrega proveedor con tipo de producto"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Agregamos el parámetro @tipo_producto=?
        cursor.execute("EXEC sp_AgregarProveedor @nombre=?, @telefono=?, @direccion=?, @correo=?, @tipo_producto=?",
                      (nombre, telefono, direccion, correo, tipo_producto))
        conn.commit()
        return True
    except Exception as e:
        print("Error al agregar proveedor:", e)
        return False
    finally:
        conn.close()


def obtener_proveedor_por_id(id_proveedor):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerProveedorPorId @id_proveedor=?", (id_proveedor,))
        
        r = cursor.fetchone()
        if not r:
            return None
            
        return {
            "id": r.id_proveedor,
            "nombre": r.nombre,
            "telefono": r.telefono,
            "direccion": r.direccion,
            "correo": r.correo,
            "tipo_producto": r.tipo_producto # <--- Nuevo campo
        }
    finally:
        conn.close()


def actualizar_proveedor(id_proveedor, nombre, telefono, direccion, correo, tipo_producto): # <--- Nuevo argumento
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Agregamos el parámetro @tipo_producto=?
        cursor.execute("""
            EXEC sp_ActualizarProveedor 
                @id_proveedor=?, @nombre=?, @telefono=?, @direccion=?, @correo=?, @tipo_producto=?
        """, (id_proveedor, nombre, telefono, direccion, correo, tipo_producto))
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar proveedor:", e)
        return False
    finally:
        conn.close()

def eliminar_proveedor(id_proveedor):
    """Elimina proveedor usando sp_EliminarProveedor"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_EliminarProveedor @id_proveedor=?", (id_proveedor,))
        conn.commit()
        return True
    except Exception as e:
        print("Error al eliminar proveedor:", e)
        return False
    finally:
        conn.close()


# =====================================================
#   CLIENTES
# =====================================================

def obtener_clientes():
    """Obtiene todos los clientes usando sp_ObtenerClientes"""
    conn = get_connection()
    clientes = []
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerClientes")
        
        for r in cursor.fetchall():
            clientes.append({
                "id": r.id_cliente,
                "nombre": r.nombre,
                "telefono": r.telefono,
                "direccion": r.direccion,
                "correo": r.correo
            })
    finally:
        conn.close()
    return clientes


def obtener_cliente_por_id(id_cliente):
    """Obtiene cliente por ID usando sp_ObtenerClientePorId"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerClientePorId @id_cliente=?", (id_cliente,))
        
        row = cursor.fetchone()
        if not row:
            return None
            
        return {
            "id": row.id_cliente,
            "nombre": row.nombre,
            "telefono": row.telefono,
            "direccion": row.direccion,
            "correo": row.correo
        }
    finally:
        conn.close()


def agregar_cliente(nombre, telefono, direccion, correo):
    """Agrega cliente usando sp_AgregarCliente"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_AgregarCliente @nombre=?, @telefono=?, @direccion=?, @correo=?",
                      (nombre, telefono, direccion, correo))
        conn.commit()
        return True
    except Exception as e:
        print("Error al agregar cliente:", e)
        return False
    finally:
        conn.close()


def actualizar_cliente(id_cliente, nombre, telefono, direccion, correo):
    """Actualiza cliente usando sp_ActualizarCliente"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            EXEC sp_ActualizarCliente 
                @id_cliente=?, @nombre=?, @telefono=?, @direccion=?, @correo=?
        """, (id_cliente, nombre, telefono, direccion, correo))
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar cliente:", e)
        return False
    finally:
        conn.close()


def eliminar_cliente(id_cliente):
    """Elimina cliente usando sp_EliminarCliente"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_EliminarCliente @id_cliente=?", (id_cliente,))
        conn.commit()
        return True
    except Exception as e:
        print("Error al eliminar cliente:", e)
        return False
    finally:
        conn.close()


# =====================================================
#   VENTAS
# =====================================================

def obtener_ventas():
    """Obtiene todas las ventas usando sp_ObtenerVentasLista"""
    conn = get_connection()
    ventas = []
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerVentasLista")
        
        for row in cursor.fetchall():
            # Manejar valores NULL en total
            total = row.total if row.total is not None else 0.0
            
            # Formatear fecha como string para el template
            fecha_str = row.fecha_venta.strftime("%d/%m/%Y %H:%M") if row.fecha_venta else "Fecha no disponible"
            
            ventas.append({
                "id": row.id_venta,
                "cliente": row.cliente,
                "fecha": fecha_str,
                "total": float(total),
                "tipo": row.tipo_venta if row.tipo_venta is not None else 'Venta',
                "observaciones": row.observaciones or ''
            })
    except Exception as e:
        print("Error en obtener_ventas:", e)
    finally:
        conn.close()
    return ventas


def registrar_venta(id_cliente, detalle_json):
    """Registra una venta completa usando sp_RegistrarVenta"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_RegistrarVenta @id_cliente=?, @detalle=?", 
                      (id_cliente, detalle_json))
        conn.commit()
        return True, "Venta registrada correctamente"
    except Exception as e:
        print("Error al registrar venta:", e)
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


def obtener_venta_por_id(id_venta):
    """Obtiene venta por ID usando sp_ObtenerVentaPorId"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerVentaPorId @id_venta=?", (id_venta,))
        
        # Primera consulta: encabezado
        row = cursor.fetchone()
        if not row:
            return None, []
            
        # Formatear fecha
        fecha_str = row.fecha_venta.strftime("%d/%m/%Y %H:%M") if row.fecha_venta else "Fecha no disponible"
        
        venta = {
            "id": row.id_venta,
            "cliente": row.cliente,
            "fecha": fecha_str,
            "total": float(row.total) if row.total is not None else 0.0,
            "tipo": row.tipo_venta or 'Venta',
            "observaciones": row.observaciones or ''
        }
        
        # Segunda consulta: detalles
        cursor.nextset()
        detalles = []
        for r in cursor.fetchall():
            detalles.append({
                "producto": r.producto,
                "cantidad": float(r.cantidad),
                "precio_unitario": float(r.precio_unitario),
                "subtotal": float(r.subtotal)
            })
        
        return venta, detalles
        
    except Exception as e:
        print("Error en obtener_venta_por_id:", e)
        return None, []
    finally:
        conn.close()


def obtener_detalles_venta(id_venta):
    """Obtiene detalles de venta usando sp_ObtenerDetallesVenta"""
    conn = get_connection()
    detalles = []
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerDetallesVenta @id_venta=?", (id_venta,))
        
        for r in cursor.fetchall():
            detalles.append({
                "producto": r.producto,
                "cantidad": float(r.cantidad),
                "precio_unitario": float(r.precio_unitario),
                "subtotal": float(r.subtotal)
            })
    finally:
        conn.close()
    return detalles


# =====================================================
#   REPORTES / VENTAS FILTRADAS
# =====================================================

def obtener_ventas_filtradas(fecha_inicio=None, fecha_fin=None, id_cliente=None):
    """Obtiene ventas con filtros usando sp_ObtenerVentasFiltradas"""
    conn = get_connection()
    ventas = []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            EXEC sp_ObtenerVentasFiltradas 
                @fecha_inicio=?, 
                @fecha_fin=?, 
                @id_cliente=?
        """, (fecha_inicio, fecha_fin, id_cliente))
        
        for row in cursor.fetchall():
            ventas.append({
                "id": row.id_venta,
                "cliente": row.cliente,
                "fecha": row.fecha_venta.strftime("%d/%m/%Y %H:%M"),
                "total": float(row.total),
                "observaciones": row.observaciones
            })
    finally:
        conn.close()
    return ventas


def obtener_reporte_ventas_por_periodo(fecha_inicio, fecha_fin):
    """Obtiene reporte de ventas por período usando sp_ReporteVentasPorPeriodo"""
    conn = get_connection()
    ventas = []
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ReporteVentasPorPeriodo @fecha_inicio=?, @fecha_fin=?", 
                      (fecha_inicio, fecha_fin))
        
        for row in cursor.fetchall():
            ventas.append({
                "id": row.id_venta,
                "cliente": row.cliente,
                "fecha": row.fecha_venta.strftime("%d/%m/%Y"),
                "total": float(row.total),
                "cantidad_productos": row.cantidad_productos
            })
    finally:
        conn.close()
    return ventas


# =====================================================
#   MOVIMIENTOS DE INVENTARIO
# =====================================================

def agregar_movimiento(id_producto, tipo_movimiento, cantidad, observaciones):
    """Registra movimiento de inventario usando sp_RegistrarMovimientoSimple"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Ejecutar procedimiento simple
        cursor.execute("EXEC sp_RegistrarMovimientoSimple @id_producto=?, @tipo_movimiento=?, @cantidad=?, @observaciones=?", 
                      (id_producto, tipo_movimiento, cantidad, observaciones))
        conn.commit()
        
        # Obtener el nuevo stock para el mensaje
        cursor.execute("SELECT stock_actual FROM Productos WHERE id_producto = ?", (id_producto,))
        nuevo_stock = cursor.fetchone()[0]
        
        mensaje = f"✅ Movimiento registrado correctamente. Stock actual: {nuevo_stock}"
        return True, mensaje
        
    except Exception as e:
        error_msg = str(e)
        print("Error al registrar movimiento:", error_msg)
        
        # Mensajes específicos
        if "Stock insuficiente" in error_msg:
            # Obtener stock actual para el mensaje
            cursor.execute("SELECT stock_actual FROM Productos WHERE id_producto = ?", (id_producto,))
            stock_actual = cursor.fetchone()[0]
            return False, f"Stock insuficiente. Disponible: {stock_actual}"
        elif "Tipo de movimiento inválido" in error_msg:
            return False, "Tipo de movimiento debe ser 'Entrada' o 'Salida'"
        elif "Producto no encontrado" in error_msg:
            return False, "Producto no encontrado"
        else:
            return False, f"Error al registrar el movimiento: {error_msg}"
    finally:
        conn.close()


def obtener_movimientos(fecha_inicio=None, fecha_fin=None, tipo_movimiento=None):
    """Obtiene movimientos con filtros usando sp_ObtenerMovimientos"""
    conn = get_connection()
    movimientos = []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            EXEC sp_ObtenerMovimientos 
                @fecha_inicio=?, 
                @fecha_fin=?, 
                @tipo_movimiento=?
        """, (fecha_inicio, fecha_fin, tipo_movimiento))
        
        for row in cursor.fetchall():
            movimientos.append({
                "id": row.id_movimiento,
                "producto": row.producto,
                "tipo": row.tipo_movimiento,
                "cantidad": float(row.cantidad),
                "fecha": row.fecha_movimiento.strftime("%d/%m/%Y %H:%M"),
                "observaciones": row.observaciones
            })
    finally:
        conn.close()
    return movimientos


# =====================================================
#   FUNCIONES AUXILIARES
# =====================================================

def obtener_usuarios():
    """Obtiene usuarios para dropdowns usando sp_ObtenerUsuariosActivos"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerUsuariosActivos")
        return [{"id": r.id_usuario, "nombre": r.nombre} for r in cursor.fetchall()]
    finally:
        conn.close()


def obtener_productos_para_venta():
    """Obtiene productos activos para ventas usando sp_ObtenerProductosParaVenta"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerProductosParaVenta")
        return [
            {
                "id": r.id_producto,
                "nombre": r.nombre,
                "stock": float(r.stock_actual),
                "precio": float(r.precio_unitario),
                "imagen": r.imagen if r.imagen else None # <--- NUEVO: Capturamos la imagen
            }
            for r in cursor.fetchall()
        ]
    finally:
        conn.close()


# =====================================================
#   FUNCIONES PARA DASHBOARD (COMPLETO)
# =====================================================

def obtener_total_productos():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerTotalProductos")
        row = cursor.fetchone()
        return row[0] if row else 0
    finally:
        conn.close()

def obtener_total_ventas(fecha_inicio=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerTotalVentas @fecha_inicio=?", (fecha_inicio,))
        row = cursor.fetchone()
        return row[0] if row else 0
    finally:
        conn.close()

def obtener_total_ingresos(fecha_inicio=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerTotalIngresos @fecha_inicio=?", (fecha_inicio,))
        row = cursor.fetchone()
        val = row[0] if row else 0
        return float(val) if val else 0.0
    finally:
        conn.close()

def obtener_total_clientes():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerTotalClientes")
        row = cursor.fetchone()
        return row[0] if row else 0
    finally:
        conn.close()

def obtener_ventas_ultimos_meses(meses=6):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerVentasUltimosMeses @meses=?", (meses,))
        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                "mes": row.mes,
                "cantidad_ventas": row.cantidad_ventas,
                "total_ventas": float(row.total_ventas)
            })
        return resultados
    finally:
        conn.close()

def obtener_productos_mas_vendidos(limite=5, fecha_inicio=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerProductosMasVendidos @limite=?, @fecha_inicio=?", (limite, fecha_inicio))
        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                "producto": row.nombre,
                "total_vendido": float(row.total_vendido),
                "total_ingresos": float(row.total_ingresos)
            })
        return resultados
    finally:
        conn.close()

# ESTA ES LA FUNCIÓN QUE FALTABA Y CAUSABA EL ERROR:
def obtener_productos_stock_bajo():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ObtenerProductosStockBajo")
        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                "producto": row.nombre,
                "stock_actual": float(row.stock_actual),
                "stock_minimo": float(row.stock_minimo),
                "diferencia": float(row.stock_minimo - row.stock_actual)
            })
        return resultados
    except Exception as e:
        print("Error en obtener_productos_stock_bajo:", e)
        return []
    finally:
        conn.close()



# =====================================================
#   SEGURIDAD Y USUARIOS (LOGIN)
# =====================================================
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, nombre, correo, rol, password_hash):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.rol = rol
        self.password_hash = password_hash

def obtener_usuario_por_correo(correo):
    """Busca usuario por correo para el login"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Nota: En un sistema real, la contraseña debería estar encriptada.
        # Aquí leemos la contraseña tal cual está en tu SQL (texto plano).
        cursor.execute("SELECT id_usuario, nombre, correo, rol, contraseña FROM Usuarios WHERE correo = ? AND activo = 1", (correo,))
        row = cursor.fetchone()
        if row:
            return User(row.id_usuario, row.nombre, row.correo, row.rol, row.contraseña)
        return None
    finally:
        conn.close()

def obtener_usuario_por_id(id_usuario):
    """Recarga el usuario desde la sesión"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, correo, rol, contraseña FROM Usuarios WHERE id_usuario = ?", (id_usuario,))
        row = cursor.fetchone()
        if row:
            return User(row.id_usuario, row.nombre, row.correo, row.rol, row.contraseña)
        return None
    finally:
        conn.close()
        
def actualizar_perfil_usuario(id_usuario, nombre, correo, password):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ActualizarUsuario @id_usuario=?, @nombre=?, @correo=?, @password=?", 
                      (id_usuario, nombre, correo, password))
        conn.commit()
        return True, "Perfil actualizado correctamente."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()