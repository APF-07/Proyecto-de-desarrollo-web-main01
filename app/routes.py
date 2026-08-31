from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import models
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import uuid
import json




# Definir el blueprint principal
main_bp = Blueprint('main', __name__)

# ==========================
# LOGIN Y LOGOUT
# ==========================
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya entró, lo mandamos al inicio para que no se loguee doble
    if current_user.is_authenticated:
        return redirect(url_for('main.inicio'))
    
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        
        # Buscamos si existe el usuario
        user = models.obtener_usuario_por_correo(correo)
        
        # Verificamos la contraseña (texto plano según tu DB actual)
        if user and user.password_hash == password:
            login_user(user)
            flash(f'¡Bienvenido, {user.nombre}!', 'success')
            return redirect(url_for('main.inicio'))
        else:
            flash('Correo o contraseña incorrectos.', 'error')
    
    return render_template('login.html', page_title="Iniciar Sesión")

@main_bp.route('/logout')
def logout():
    logout_user() # Cierra la sesión
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main.login'))

# ==========================
# Página de inicio
# ==========================
@main_bp.route('/')
@login_required
def inicio():
    return render_template('inicio.html', page_title="Inicio")

# ==========================
# Listado de productos
# ==========================
# ==========================
# Listado de productos
# ==========================
@main_bp.route('/productos', strict_slashes=False)
@login_required
def listar_productos():
    # Obtenemos productos Y categorías
    productos = models.obtener_productos()
    categorias = models.obtener_categorias()
    
    return render_template('productos.html', 
                         productos=productos, 
                         categorias=categorias,
                         page_title="Productos")

# ==========================
# Eliminar producto
# ==========================
@main_bp.route('/productos/toggle_estado/<int:id>/<string:estado_actual>')
@login_required
def toggle_estado_producto(id, estado_actual):
    nuevo_estado = 'Inactivo' if estado_actual == 'Activo' else 'Activo'
    ok = models.cambiar_estado_producto(id, nuevo_estado)

    if ok:
        mensaje = f"✅ Producto {'desactivado' if nuevo_estado == 'Inactivo' else 'activado'} correctamente."
        flash(mensaje)
    else:
        flash("❌ No se pudo actualizar el estado del producto.")

    return redirect(url_for('main.listar_productos'))

# =====================================================
#   CATEGORÍAS
# =====================================================

@main_bp.route('/categorias')
@login_required
def listar_categorias():
    categorias = models.obtener_categorias_todas()
    return render_template('categorias.html', categorias=categorias, page_title="Categorías")

@main_bp.route('/categorias/nueva', methods=['GET', 'POST'])
@login_required
def nueva_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        if models.agregar_categoria(nombre, descripcion):
            flash("✅ Categoría agregada correctamente.")
        else:
            flash("❌ Error al agregar categoría.")
        return redirect(url_for('main.listar_categorias'))
    return render_template('categoria_form.html', categoria=None, page_title="Nueva categoría")

@main_bp.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    categoria = models.obtener_categoria_por_id(id)
    if not categoria:
        flash("❌ Categoría no encontrada.")
        return redirect(url_for('main.listar_categorias'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        if models.actualizar_categoria(id, nombre, descripcion):
            flash("✅ Categoría actualizada correctamente.")
        else:
            flash("❌ Error al actualizar categoría.")
        return redirect(url_for('main.listar_categorias'))

    return render_template('categoria_form.html', categoria=categoria, page_title="Editar categoría")

@main_bp.route('/categorias/eliminar/<int:id>')
@login_required
def eliminar_categoria(id):
    if models.eliminar_categoria(id):
        flash("🗑️ Categoría eliminada.")
    else:
        flash("❌ No se pudo eliminar la categoría.")
    return redirect(url_for('main.listar_categorias'))

# =====================================================
#   PROVEEDORES
# =====================================================

@main_bp.route('/proveedores')
@login_required
def listar_proveedores():
    proveedores = models.obtener_proveedores_todos()
    return render_template('proveedores.html', proveedores=proveedores, page_title="Proveedores")

@main_bp.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_proveedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        correo = request.form['correo']
        tipo_producto = request.form['tipo_producto'] # <--- Capturar nuevo dato
        
        if models.agregar_proveedor(nombre, telefono, direccion, correo, tipo_producto):
            flash("✅ Proveedor agregado correctamente.")
        else:
            flash("❌ Error al agregar proveedor.")
        return redirect(url_for('main.listar_proveedores'))
    return render_template('proveedor_form.html', proveedor=None, page_title="Nuevo proveedor")

@main_bp.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(id):
    proveedor = models.obtener_proveedor_por_id(id)
    if not proveedor:
        flash("❌ Proveedor no encontrado.")
        return redirect(url_for('main.listar_proveedores'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        correo = request.form['correo']
        tipo_producto = request.form['tipo_producto'] # <--- Capturar nuevo dato
        
        if models.actualizar_proveedor(id, nombre, telefono, direccion, correo, tipo_producto):
            flash("✅ Proveedor actualizado correctamente.")
        else:
            flash("❌ Error al actualizar proveedor.")
        return redirect(url_for('main.listar_proveedores'))

    return render_template('proveedor_form.html', proveedor=proveedor, page_title="Editar proveedor")

@main_bp.route('/proveedores/eliminar/<int:id>')
@login_required
def eliminar_proveedor(id):
    if models.eliminar_proveedor(id):
        flash("🗑️ Proveedor eliminado.")
    else:
        flash("❌ No se pudo eliminar el proveedor.")
    return redirect(url_for('main.listar_proveedores'))

# =====================================================
#   VENTAS
# =====================================================

@main_bp.route("/ventas", strict_slashes=False)
@login_required
def listar_ventas():
    """Página principal de gestión de ventas y clientes"""
    clientes = models.obtener_clientes()
    ventas = models.obtener_ventas()
    return render_template("ventas.html", 
                           clientes=clientes, 
                           ventas=ventas, 
                           page_title="Gestión de Ventas y Clientes")

@main_bp.route("/ventas/nueva", methods=["GET", "POST"])
@login_required
def nueva_venta():
    """Registra una nueva venta usando sp_RegistrarVenta (sin usuario)"""
    if request.method == "POST":
        try:
            cliente_id = int(request.form["cliente_id"])
            detalles_json = request.form["detalles"]
            
            print("=== DEBUG VENTA ===")
            print("Cliente ID:", cliente_id)
            print("Detalles JSON:", detalles_json)
            
            # Registrar la venta
            success, mensaje = models.registrar_venta(cliente_id, detalles_json)
            
            print("Resultado:", success, mensaje)
            print("=== FIN DEBUG ===")
            
            if success:
                flash("✅ Venta registrada correctamente.", "success")
                return redirect(url_for("main.listar_ventas"))
            else:
                flash(f"❌ Error al registrar venta: {mensaje}", "error")
                
        except Exception as e:
            print("Error en nueva_venta:", e)
            flash(f"❌ Error en el formulario: {str(e)}", "error")

    return redirect(url_for('main.listar_ventas'))

@main_bp.route("/ventas/<int:id>")
@login_required
def ver_venta(id):
    """Muestra el detalle de una venta usando sp_ObtenerVentaPorId"""
    venta, detalles = models.obtener_venta_por_id(id)
    if not venta:
        flash("❌ Venta no encontrada.", "error")
        return redirect(url_for('main.listar_ventas'))

    # Pasamos la venta específica y sus detalles al template ventas.html
    clientes = models.obtener_clientes()
    ventas = models.obtener_ventas()  # Para mantener el historial
    
    return render_template(
        "ventas.html", 
        clientes=clientes,
        ventas=ventas,
        venta_especifica=venta,
        detalles_venta=detalles,
        page_title=f"Detalle de Venta #{venta['id']}"
    )

@main_bp.route("/api/ventas/calcular-total", methods=["POST"])
@login_required
def calcular_total_venta():
    """API para calcular el total de una venta en tiempo real"""
    try:
        data = request.get_json()
        detalles = data.get('detalles', [])
        
        total = 0
        for detalle in detalles:
            cantidad = float(detalle['cantidad'])
            precio = float(detalle['precio'])
            total += cantidad * precio
            
        return jsonify({"success": True, "total": round(total, 2)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@main_bp.route("/api/productos_venta")
@login_required
def api_productos_venta():
    """API para obtener productos disponibles para venta"""
    try:
        productos = models.obtener_productos_para_venta()
        return jsonify(productos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================================================
#   CLIENTES
# =====================================================

@main_bp.route("/nuevo_cliente", methods=["GET", "POST"])
@login_required
def nuevo_cliente():
    """Crea un nuevo cliente usando sp_AgregarCliente"""
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        correo = request.form["correo"]
        
        if models.agregar_cliente(nombre, telefono, direccion, correo):
            flash("✅ Cliente agregado correctamente.", "success")
        else:
            flash("❌ Error al agregar cliente.", "error")
        return redirect(url_for('main.listar_ventas'))
    
    return render_template("cliente_form.html", cliente=None, page_title="Nuevo Cliente")

@main_bp.route("/editar_cliente/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):
    """Edita un cliente usando sp_ActualizarCliente"""
    cliente = models.obtener_cliente_por_id(id)
    if not cliente:
        flash("❌ Cliente no encontrado.", "error")
        return redirect(url_for('main.listar_ventas'))

    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        correo = request.form["correo"]
        
        if models.actualizar_cliente(id, nombre, telefono, direccion, correo):
            flash("✅ Cliente actualizado correctamente.", "success")
        else:
            flash("❌ Error al actualizar cliente.", "error")
        return redirect(url_for('main.listar_ventas'))

    return render_template("cliente_form.html", cliente=cliente, page_title="Editar Cliente")

@main_bp.route("/eliminar_cliente/<int:id>")
@login_required
def eliminar_cliente(id):
    """Elimina un cliente usando sp_EliminarCliente"""
    if models.eliminar_cliente(id):
        flash("🗑️ Cliente eliminado correctamente.", "success")
    else:
        flash("❌ No se pudo eliminar el cliente.", "error")
    return redirect(url_for('main.listar_ventas'))

# =====================================================
#   DASHBOARD
# =====================================================

# Importa timedelta para calcular fechas
from datetime import datetime, timedelta 

@main_bp.route("/dashboard")
@login_required
def dashboard():
    """Dashboard con filtros de tiempo"""
    
    # 1. Obtener el filtro de la URL (por defecto 'historico')
    periodo = request.args.get('periodo', 'historico')
    fecha_inicio = None
    titulo_periodo = "Histórico Total"

    # 2. Calcular la fecha de inicio según el filtro
    now = datetime.now()
    
    if periodo == 'hoy':
        # Desde hoy a las 00:00:00
        fecha_inicio = now.replace(hour=0, minute=0, second=0, microsecond=0)
        titulo_periodo = "Ventas de Hoy"
        
    elif periodo == 'semana':
        # Últimos 7 días
        fecha_inicio = now - timedelta(days=7)
        titulo_periodo = "Últimos 7 Días"
        
    elif periodo == 'mes':
        # Primer día de este mes
        fecha_inicio = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        titulo_periodo = "Este Mes"

    # 3. Consultar datos con el filtro aplicado
    datos = {
        "periodo_actual": periodo,
        "titulo_periodo": titulo_periodo,
        "total_productos": models.obtener_total_productos(), # Inventario no cambia por fechas
        "total_ventas": models.obtener_total_ventas(fecha_inicio),
        "total_ingresos": models.obtener_total_ingresos(fecha_inicio), # ¡Nuevo dato!
        "total_clientes": models.obtener_total_clientes(),
        "ventas_por_mes": models.obtener_ventas_ultimos_meses(6), # Tendencia se mantiene fija
        "productos_mas_vendidos": models.obtener_productos_mas_vendidos(5, fecha_inicio), # Top cambia según fecha
        "stock_bajo": models.obtener_productos_stock_bajo()
    }
    
    return render_template("dashboard.html", datos=datos, page_title="Dashboard")

# =====================================================
#   REABASTECIMIENTO DE INVENTARIO
# =====================================================

@main_bp.route("/inventario/reabastecer", methods=["GET", "POST"])
@login_required
def reabastecer_inventario():
    """Reabastece el inventario de productos"""
    productos = models.obtener_productos()
    productos_bajos = models.obtener_productos_stock_bajo()  # <- NUEVA LÍNEA
    producto_seleccionado = request.args.get('producto_id')
    
    if request.method == "POST":
        try:
            producto_id = int(request.form["producto_id"])
            cantidad = float(request.form["cantidad"])
            observaciones = request.form.get("observaciones", "Reabastecimiento de inventario")
            
            # Registrar el movimiento de entrada
            success, mensaje = models.agregar_movimiento(
                producto_id, 'Entrada', cantidad, observaciones
            )
            
            if success:
                flash(f"✅ {mensaje}", "success")
            else:
                flash(f"❌ {mensaje}", "error")
                
            return redirect(url_for('main.reabastecer_inventario'))
            
        except Exception as e:
            flash(f"❌ Error en el formulario: {str(e)}", "error")
    
    return render_template("reabastecer.html", 
                         productos=productos, 
                         productos_bajos=productos_bajos,  # <- NUEVO PARÁMETRO
                         producto_seleccionado=producto_seleccionado,
                         page_title="Reabastecer Inventario")


# =====================================================
#   GENERACIÓN DE BOLETA PDF
# =====================================================

from flask import send_file
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os

@main_bp.route("/api/ventas/<int:id>/pdf/boleta")
@login_required
def generar_pdf_boleta(id):
    """Genera PDF con formato profesional de boleta de venta"""
    try:
        venta, detalles = models.obtener_venta_por_id(id)
        if not venta:
            return jsonify({'error': 'Venta no encontrada'}), 404

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        pdf.setTitle(f"Boleta Electronica {venta['id']}")
        
        # --- ENCABEZADO ---
        
        # 1. LOGO (Lado Izquierdo)
        try:
            # Buscamos logo.jpg en la carpeta static/img
            logo_path = os.path.join(os.path.dirname(__file__), 'static', 'img', 'logo.jpg')
            
            if os.path.exists(logo_path):
                # Dibuja el logo: (x, y, ancho, alto)
                # Ajustamos un poco el tamaño para que se vea bien
                pdf.drawImage(logo_path, 40, height - 110, width=100, height=60, mask='auto', preserveAspectRatio=True)
            else:
                print("Nota: No se encontró el archivo logo.jpg en static/img")
        except Exception as e:
            print(f"Error cargando logo: {e}")

        # 2. DATOS DE LA EMPRESA (Debajo/Al lado del logo)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(150, height - 60, "CEREAL SIERRA") 
        
        pdf.setFont("Helvetica-Oblique", 10)
        pdf.drawString(150, height - 72, "Alimentos de Altura") # Slogan del logo
        
        pdf.setFont("Helvetica", 9)
        pdf.drawString(40, height - 125, "Av. Los Andes 123, Pasco - Perú")
        pdf.drawString(40, height - 137, "Telf: (063) 421-500 | contacto@cerealsierra.com")
        
        # 3. CUADRO RUC (Lado Derecho - Estilo SUNAT)
        # Marco del cuadro
        pdf.setStrokeColorRGB(0.5, 0.5, 0.5)
        pdf.setLineWidth(1)
        pdf.rect(width - 210, height - 115, 170, 75, fill=0)
        
        # Título del documento (Fondo gris)
        pdf.setFillColorRGB(0.9, 0.9, 0.9)
        pdf.rect(width - 210, height - 90, 170, 25, fill=1, stroke=1)
        
        # Textos del cuadro
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(width - 125, height - 60, "R.U.C. 20601234567") # RUC Ficticio
        
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(width - 125, height - 83, "BOLETA DE VENTA")
        
        pdf.setFont("Helvetica", 12)
        # Número formateado (ej: 000123)
        pdf.drawCentredString(width - 125, height - 105, f"N° 001 - {str(venta['id']).zfill(6)}")

        # --- DATOS DEL CLIENTE ---
        y_info = height - 170
        
        # Fecha
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(40, y_info, "Fecha de Emisión:")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(140, y_info, venta['fecha'])
        
        # Cliente
        y_info -= 15
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(40, y_info, "Señor(es):")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(140, y_info, venta['cliente'])
        
        # Moneda
        y_info -= 15
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(40, y_info, "Moneda:")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(140, y_info, "SOLES")

        # --- TABLA DE PRODUCTOS ---
        y_header = y_info - 30
        
        # Encabezado Negro
        pdf.setFillColorRGB(0.2, 0.2, 0.2)
        pdf.rect(40, y_header - 5, width - 80, 20, fill=1, stroke=0)
        
        # Textos Blancos
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(50, y_header + 2, "CANT.")
        pdf.drawString(100, y_header + 2, "DESCRIPCIÓN")
        pdf.drawRightString(450, y_header + 2, "P. UNIT")
        pdf.drawRightString(530, y_header + 2, "IMPORTE")
        
        pdf.setFillColorRGB(0, 0, 0) # Volver a negro
        
        y_rows = y_header - 25
        total_venta = 0
        
        pdf.setFont("Helvetica", 9)
        
        for detalle in detalles:
            # Control de salto de página
            if y_rows < 100:
                pdf.showPage()
                y_rows = height - 50
            
            nombre = detalle['producto']
            if len(nombre) > 50: nombre = nombre[:47] + "..."
            
            pdf.drawString(50, y_rows, str(detalle['cantidad']))
            pdf.drawString(100, y_rows, nombre)
            
            # Precios alineados a la DERECHA
            pdf.drawRightString(450, y_rows, f"{detalle['precio_unitario']:.2f}")
            pdf.drawRightString(530, y_rows, f"{detalle['subtotal']:.2f}")
            
            # Línea separadora gris suave
            pdf.setStrokeColorRGB(0.9, 0.9, 0.9)
            pdf.line(40, y_rows - 5, width - 40, y_rows - 5)
            
            total_venta += detalle['subtotal']
            y_rows -= 20

        # --- TOTAL FINAL ---
        y_total = y_rows - 10
        
        # Cuadro de Total
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(350, y_total - 20, 200, 25, fill=0)
        
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(360, y_total - 13, "TOTAL A PAGAR:")
        pdf.drawRightString(540, y_total - 13, f"S/ {total_venta:.2f}")

        # --- PIE DE PÁGINA ---
        if venta['observaciones']:
            pdf.setFont("Helvetica-Oblique", 8)
            pdf.drawString(40, y_total - 40, f"Observaciones: {venta['observaciones']}")

        pdf.setFont("Helvetica", 8)
        pdf.drawCentredString(width/2, 50, "¡Gracias por su compra!")
        pdf.drawCentredString(width/2, 40, "Cereal Sierra - Calidad garantizada")

        pdf.save()
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"boleta_{str(venta['id']).zfill(6)}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Error al generar boleta: {e}")
        # En caso de error, devolvemos un JSON para saber qué pasó
        return jsonify({'error': f'Ocurrió un error: {str(e)}'}), 500
    
# 2. Configura la carpeta (justo debajo de los imports)
# Usamos 'app/static/img' como pediste
UPLOAD_FOLDER = 'app/static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 3. Modifica la ruta nuevo_producto
@main_bp.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        id_categoria = request.form['categoria']
        id_proveedor = request.form['proveedor']
        unidad = request.form['unidad']
        stock_inicial = request.form['stock_inicial']
        stock_minimo = request.form['stock_minimo']
        precio = request.form['precio']

        # --- LOGICA DE IMAGEN ---
        imagen_nombre = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Creamos un nombre único para no borrar fotos con el mismo nombre
                nombre_unico = f"{uuid.uuid4().hex}_{filename}"
                # Guardamos en app/static/img/
                file.save(os.path.join(UPLOAD_FOLDER, nombre_unico))
                imagen_nombre = nombre_unico
        # ------------------------

        ok = models.agregar_producto(
            nombre, id_categoria, id_proveedor, unidad,
            stock_inicial, stock_minimo, precio, imagen_nombre # Pasamos la imagen
        )
        if ok:
            flash("✅ Producto agregado correctamente.", "success")
        else:
            flash("❌ Error al agregar producto.", "error")
        return redirect(url_for('main.listar_productos'))

    categorias = models.obtener_categorias()
    proveedores = models.obtener_proveedores()
    return render_template('producto_form.html', categorias=categorias, proveedores=proveedores)

# 4. Modifica la ruta editar_producto (similar)
@main_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        id_categoria = request.form['categoria']
        id_proveedor = request.form['proveedor']
        unidad = request.form['unidad']
        stock_minimo = request.form['stock_minimo']
        precio = request.form['precio']

        # --- LOGICA DE IMAGEN ---
        imagen_nombre = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                nombre_unico = f"{uuid.uuid4().hex}_{filename}"
                file.save(os.path.join(UPLOAD_FOLDER, nombre_unico))
                imagen_nombre = nombre_unico
        # ------------------------

        ok = models.actualizar_producto(
            id, nombre, id_categoria, id_proveedor, unidad, stock_minimo, precio, imagen_nombre
        )
        if ok:
            flash("✅ Producto actualizado correctamente.", "success")
        else:
            flash("❌ Error al actualizar producto.", "error")
        return redirect(url_for('main.listar_productos'))

    producto = models.obtener_producto_por_id(id)
    categorias = models.obtener_categorias()
    proveedores = models.obtener_proveedores()
    return render_template('producto_form.html', producto=producto, categorias=categorias, proveedores=proveedores)

@main_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['password']
        
        # Actualizamos en BD
        success, mensaje = models.actualizar_perfil_usuario(current_user.id, nombre, correo, password)
        
        if success:
            flash("✅ " + mensaje, "success")
            # Actualizamos la sesión actual para que se vea el cambio de nombre al instante
            current_user.nombre = nombre
            current_user.correo = correo
        else:
            flash("❌ Error: " + mensaje, "error")
            
        return redirect(url_for('main.perfil'))

    return render_template('perfil.html', page_title="Mi Perfil")
# =====================================================
#   ASISTENTE INTELIGENTE CON GEMINI API
# =====================================================
from google import genai

def preguntar_a_gemini(pregunta):
    try:
        # Lee la clave de forma segura desde Google Cloud
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"Eres un asistente experto en inventarios y ventas para 'Cereal Sierra'. Responde de forma útil y breve: {pregunta}"
        )
        return response.text
    except Exception as e:
        return f"Error al conectar con la IA: {str(e)}"

@main_bp.route('/asistente-ia', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def asistente_ia():
    respuesta = None
    if request.method == 'POST':
        pregunta_usuario = request.form.get('pregunta')
        if pregunta_usuario:
            try:
                # 1. Recopilamos absolutamente todo de la base de datos en tiempo real
                total_productos = models.obtener_total_productos()
                stock_bajos = models.obtener_productos_stock_bajo()
                mas_vendidos = models.obtener_productos_mas_vendidos(10, None)
                todos_los_productos = models.obtener_productos()
                lista_clientes = models.obtener_clientes()
                lista_proveedores = models.obtener_proveedores_todos()
                lista_categorias = models.obtener_categorias_todas() # <--- ¡Nuevo! Obtenemos las categorías
                
                # 2. Construimos el contexto completo y actualizado
                contexto_negocio = "--- RESUMEN ACTUAL Y COMPLETO DEL SISTEMA 'CEREAL SIERRA' ---\n"
                contexto_negocio += f"- Total de productos en catálogo: {total_productos}\n"
                
                # Categorías registradas (¡NUEVO!)
                contexto_negocio += "- Categorías de productos disponibles:\n"
                if lista_categorias:
                    for cat in lista_categorias:
                        if isinstance(cat, dict):
                            c_nombre = cat.get('nombre') or 'Sin nombre'
                            c_desc = cat.get('descripcion', 'Sin descripción')
                        else:
                            c_nombre = getattr(cat, 'nombre', None) or 'Sin nombre'
                            c_desc = getattr(cat, 'descripcion', 'Sin descripción')
                        contexto_negocio += f"  * Categoría: {c_nombre} | Descripción: {c_desc}\n"
                else:
                    contexto_negocio += "  * No hay categorías registradas.\n"

                # Alertas de stock bajo
                contexto_negocio += "- Alertas de stock bajo:\n"
                if stock_bajos:
                    for p in stock_bajos:
                        if isinstance(p, dict):
                            nombre = p.get('nombre') or p.get('producto') or p.get('nombre_producto') or 'Desconocido'
                            stock = p.get('stock', 0)
                            minimo = p.get('stock_minimo', 0)
                        else:
                            nombre = getattr(p, 'nombre', None) or getattr(p, 'producto', None) or 'Desconocido'
                            stock = getattr(p, 'stock', 0)
                            minimo = getattr(p, 'stock_minimo', 0)
                        contexto_negocio += f"  * Producto: {nombre} | Stock actual: {stock} | Stock mínimo requerido: {minimo}\n"
                else:
                    contexto_negocio += "  * No hay productos con stock bajo.\n"

                # Productos más vendidos
                contexto_negocio += "- Productos más vendidos (Histórico de ventas):\n"
                if mas_vendidos:
                    for p in mas_vendidos:
                        if isinstance(p, dict):
                            nombre = p.get('nombre') or p.get('producto') or p.get('nombre_producto') or 'Desconocido'
                            total = p.get('total_vendido') or p.get('cantidad') or p.get('total') or '0'
                        else:
                            nombre = getattr(p, 'nombre', None) or getattr(p, 'producto', None) or 'Desconocido'
                            total = getattr(p, 'total_vendido', None) or getattr(p, 'cantidad', None) or getattr(p, 'total', None) or '0'
                        contexto_negocio += f"  * Producto: {nombre} -> Cantidad vendida: {total}\n"
                else:
                    contexto_negocio += "  * No hay registros de ventas detalladas aún.\n"

                # Catálogo general de productos
                contexto_negocio += "- Catálogo general de productos y precios:\n"
                if todos_los_productos:
                    for p in todos_los_productos:
                        if isinstance(p, dict):
                            nombre = p.get('nombre') or p.get('producto') or 'Desconocido'
                            precio = p.get('precio', 0)
                            stock = p.get('stock', 0)
                            cat = p.get('categoria', 'General')
                        else:
                            nombre = getattr(p, 'nombre', None) or getattr(p, 'producto', None) or 'Desconocido'
                            precio = getattr(p, 'precio', 0)
                            stock = getattr(p, 'stock', 0)
                            cat = getattr(p, 'categoria', 'General')
                        contexto_negocio += f"  * [{cat}] {nombre} - Precio: S/. {precio} - Stock: {stock}\n"

                # Listado de clientes
                contexto_negocio += "- Clientes y empresas registradas:\n"
                if lista_clientes:
                    for c in lista_clientes:
                        if isinstance(c, dict):
                            nombre_cliente = c.get('nombre') or c.get('nombre_cliente') or 'Cliente sin nombre'
                            telefono = c.get('telefono', 'Sin teléfono')
                            correo = c.get('correo', 'Sin correo')
                        else:
                            nombre_cliente = getattr(c, 'nombre', None) or 'Cliente sin nombre'
                            telefono = getattr(c, 'telefono', 'Sin teléfono')
                            correo = getattr(c, 'correo', 'Sin correo')
                        contexto_negocio += f"  * Cliente/Empresa: {nombre_cliente} | Teléfono: {telefono} | Correo: {correo}\n"
                else:
                    contexto_negocio += "  * No hay clientes registrados todavía.\n"

                # Listado de proveedores
                contexto_negocio += "- Proveedores registrados en el sistema:\n"
                if lista_proveedores:
                    for prov in lista_proveedores:
                        if isinstance(prov, dict):
                            p_nombre = prov.get('nombre') or 'Proveedor sin nombre'
                            p_tipo = prov.get('tipo_producto', 'General')
                            p_tel = prov.get('telefono', 'Sin teléfono')
                            p_correo = prov.get('correo', 'Sin correo')
                        else:
                            p_nombre = getattr(prov, 'nombre', None) or 'Proveedor sin nombre'
                            p_tipo = getattr(prov, 'tipo_producto', 'General')
                            p_tel = getattr(prov, 'telefono', 'Sin teléfono')
                            p_correo = getattr(prov, 'correo', 'Sin correo')
                        contexto_negocio += f"  * Proveedor: {p_nombre} | Suministra/Tipo: {p_tipo} | Teléfono: {p_tel} | Correo: {p_correo}\n"
                else:
                    contexto_negocio += "  * No hay proveedores registrados todavía.\n"
                
                contexto_negocio += "------------------------------------------------------------------\n"

            except Exception as db_error:
                contexto_negocio = f"(Aviso al sistema: Hubo una incidencia menor al cargar los datos: {db_error})\n"

            # 3. Prompt hacia la IA con todo el conocimiento del negocio
            prompt_completo = f"""
            {contexto_negocio}
            
            Instrucción: Eres el Gerente de Operaciones de 'Cereal Sierra'. Responde de forma clara y detallada a la pregunta del usuario utilizando la información completa de categorías, productos, ventas, clientes y proveedores provista arriba.
            
            Pregunta del usuario: {pregunta_usuario}
            """
            
            respuesta = preguntar_a_gemini(prompt_completo)
            
    return render_template('asistente_ia.html', respuesta=respuesta, page_title="Asistente IA")