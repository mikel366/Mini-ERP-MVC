# app/vistas/pedidos_vistas.py
import tkinter as tk
from tkinter import ttk, messagebox
from controladores import PedidoControlador, ClientesControlador, ProductoControlador, DetallePedidoControlador
from datetime import datetime

class PedidosTab(ttk.Frame):
    def __init__(self, master, refresh_purchases_cb=None):
        super().__init__(master)
        self.refresh_purchases_cb = refresh_purchases_cb
        self.selected_pedido_id = None
        self.current_pedido_id = None  # Para el pedido abierto actual
        self.build_ui()
        self.refresh()

    def build_ui(self):
        # Frame principal con dos secciones
        main_frame = ttk.PanedWindow(self, orient="horizontal")
        main_frame.pack(fill="both", expand=True, padx=6, pady=6)
        
        # Panel izquierdo - Gestión de pedidos
        left_panel = ttk.Frame(main_frame)
        main_frame.add(left_panel, weight=1)
        
        # Panel derecho - Detalles del pedido
        right_panel = ttk.Frame(main_frame)
        main_frame.add(right_panel, weight=1)
        
        self.build_pedidos_panel(left_panel)
        self.build_detalles_panel(right_panel)

    def build_pedidos_panel(self, parent):
        # Frame de búsqueda
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill="x", padx=6, pady=6)
        
        ttk.Label(search_frame, text="Buscar:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=6)
        search_entry.bind('<KeyRelease>', lambda e: self.refresh())
        
        ttk.Button(search_frame, text="Limpiar", command=self.clear_search).pack(side="left", padx=4)

        # Frame para abrir pedido
        open_frame = ttk.LabelFrame(parent, text="1. Abrir Nuevo Pedido")
        open_frame.pack(fill="x", padx=6, pady=6)
        
        ttk.Label(open_frame, text="Cliente:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.cliente_var = tk.StringVar()
        self.cliente_combo = ttk.Combobox(open_frame, textvariable=self.cliente_var, width=25, state="readonly")
        self.cliente_combo.grid(row=0, column=1, padx=6, pady=6)
        
        ttk.Button(open_frame, text="Abrir Pedido", command=self.abrir_pedido).grid(row=0, column=2, padx=6, pady=6)
        
        # Estado del pedido actual
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(open_frame, textvariable=self.status_var, foreground="blue")
        self.status_label.grid(row=1, column=0, columnspan=3, padx=6, pady=6)

        # Frame de gestión de pedidos
        manage_frame = ttk.LabelFrame(parent, text="3. Gestión de Pedidos")
        manage_frame.pack(fill="x", padx=6, pady=6)
        
        button_frame = ttk.Frame(manage_frame)
        button_frame.pack(fill="x", padx=6, pady=6)
        
        ttk.Button(button_frame, text="Crear Pedido", command=self.crear_pedido).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Ver Detalles", command=self.view_pedido_details).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Actualizar Estado", command=self.update_estado).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Eliminar", command=self.delete_selected).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Cancelar Pedido Actual", command=self.cancel_current_pedido).pack(side="left", padx=2)
        ttk.Button(button_frame, text="🗑️ Eliminar Todos", command=self.delete_all_pedidos, 
                  style="Accent.TButton").pack(side="right", padx=2)

        # Treeview para listar pedidos
        cols = ("id", "cliente", "monto_final", "estado", "ganancia_total", "fecha")
        self.tree = ttk.Treeview(parent, columns=cols, show="headings", height=12)
        
        # Configurar columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("monto_final", text="Monto Final")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("ganancia_total", text="Ganancia")
        self.tree.heading("fecha", text="Fecha")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("cliente", width=120, anchor="w")
        self.tree.column("monto_final", width=80, anchor="e")
        self.tree.column("estado", width=80, anchor="center")
        self.tree.column("ganancia_total", width=80, anchor="e")
        self.tree.column("fecha", width=120, anchor="center")
        
        # Scrollbar para el treeview
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        scrollbar.pack(side="right", fill="y", padx=(0, 6), pady=6)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select_pedido)
        
        # Cargar clientes en el combobox
        self.cargar_clientes()

    def build_detalles_panel(self, parent):
        # Frame para agregar detalles
        detail_frame = ttk.LabelFrame(parent, text="2. Agregar Productos al Pedido")
        detail_frame.pack(fill="x", padx=6, pady=6)
        
        # Producto
        ttk.Label(detail_frame, text="Producto:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.producto_var = tk.StringVar()
        self.producto_combo = ttk.Combobox(detail_frame, textvariable=self.producto_var, width=25, state="readonly")
        self.producto_combo.grid(row=0, column=1, padx=6, pady=6)
        
        # Cantidad
        ttk.Label(detail_frame, text="Cantidad:").grid(row=0, column=2, padx=6, pady=6, sticky="e")
        self.cantidad_var = tk.StringVar()
        cantidad_entry = ttk.Entry(detail_frame, textvariable=self.cantidad_var, width=10)
        cantidad_entry.grid(row=0, column=3, padx=6, pady=6)
        
        ttk.Button(detail_frame, text="Agregar Producto", command=self.agregar_detalle).grid(row=0, column=4, padx=6, pady=6)
        
        # Información del pedido actual
        info_frame = ttk.Frame(detail_frame)
        info_frame.grid(row=1, column=0, columnspan=5, padx=6, pady=6, sticky="ew")
        
        ttk.Label(info_frame, text="Subtotal:").grid(row=0, column=0, padx=6, pady=3, sticky="e")
        self.subtotal_var = tk.StringVar(value="0.00")
        ttk.Label(info_frame, textvariable=self.subtotal_var).grid(row=0, column=1, padx=6, pady=3, sticky="w")
        
        ttk.Label(info_frame, text="Ganancia:").grid(row=0, column=2, padx=6, pady=3, sticky="e")
        self.ganancia_var = tk.StringVar(value="0.00")
        ttk.Label(info_frame, textvariable=self.ganancia_var).grid(row=0, column=3, padx=6, pady=3, sticky="w")

        # Treeview para detalles del pedido
        detail_cols = ("id", "producto", "cantidad", "precio_unitario", "subtotal")
        self.detail_tree = ttk.Treeview(parent, columns=detail_cols, show="headings", height=10)
        
        # Configurar columnas de detalles
        self.detail_tree.heading("id", text="ID")
        self.detail_tree.heading("producto", text="Producto")
        self.detail_tree.heading("cantidad", text="Cantidad")
        self.detail_tree.heading("precio_unitario", text="Precio Unit.")
        self.detail_tree.heading("subtotal", text="Subtotal")
        
        self.detail_tree.column("id", width=50, anchor="center")
        self.detail_tree.column("producto", width=150, anchor="w")
        self.detail_tree.column("cantidad", width=80, anchor="center")
        self.detail_tree.column("precio_unitario", width=80, anchor="e")
        self.detail_tree.column("subtotal", width=80, anchor="e")
        
        # Scrollbar para detalles
        detail_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.detail_tree.yview)
        self.detail_tree.configure(yscrollcommand=detail_scrollbar.set)
        
        self.detail_tree.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        detail_scrollbar.pack(side="right", fill="y", padx=(0, 6), pady=6)
        
        self.detail_tree.bind('<Double-1>', self.delete_detalle)
        
        # Cargar productos en el combobox
        self.cargar_productos()

    def cargar_clientes(self):
        """Carga la lista de clientes en el combobox"""
        try:
            clientes = ClientesControlador.listar_clientes()
            if clientes:
                cliente_list = [f"{cliente[0]} - {cliente[1]}" for cliente in clientes]
                self.cliente_combo['values'] = cliente_list
            else:
                self.cliente_combo['values'] = []
                print("No hay clientes disponibles")
        except Exception as e:
            print(f"Error al cargar clientes: {e}")
            messagebox.showerror("Error", f"Error al cargar clientes: {e}")

    def cargar_productos(self):
        """Carga la lista de productos en el combobox"""
        try:
            productos = ProductoControlador.listar_productos()
            if productos:
                producto_list = [f"{producto[0]} - {producto[2]} (${producto[4]:.2f})" for producto in productos]
                self.producto_combo['values'] = producto_list
            else:
                self.producto_combo['values'] = []
                print("No hay productos disponibles")
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            messagebox.showerror("Error", f"Error al cargar productos: {e}")

    def refresh_dropdowns(self):
        """Actualiza los dropdowns de clientes y productos"""
        self.cargar_clientes()
        self.cargar_productos()

    def abrir_pedido(self):
        """Abre un nuevo pedido seleccionando un cliente"""
        if not self.cliente_var.get():
            messagebox.showwarning("Validación", "Por favor seleccione un cliente")
            return
        
        try:
            # Extraer ID del cliente del combobox
            cliente_text = self.cliente_var.get()
            cliente_id = int(cliente_text.split(" - ")[0])
            
            # Abrir nuevo pedido
            pedido = PedidoControlador.abrir_pedido(cliente_id)
            
            if pedido:
                self.current_pedido_id = pedido.id
                cliente_name = cliente_text.split(" - ")[1]
                self.status_var.set(f"Pedido #{pedido.id} abierto para {cliente_name}")
                messagebox.showinfo("Éxito", f"Pedido #{pedido.id} abierto exitosamente")
                self.refresh_detalles()
                self.refresh()
            else:
                messagebox.showerror("Error", "No se pudo abrir el pedido")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir pedido: {str(e)}")

    def agregar_detalle(self):
        """Agrega un producto al pedido actual"""
        if not self.current_pedido_id:
            messagebox.showwarning("Validación", "Primero debe abrir un pedido")
            return
        
        if not self.producto_var.get() or not self.cantidad_var.get():
            messagebox.showwarning("Validación", "Seleccione un producto y especifique la cantidad")
            return
        
        try:
            # Extraer ID del producto
            producto_text = self.producto_var.get()
            producto_id = int(producto_text.split(" - ")[0])
            cantidad = int(self.cantidad_var.get())
            
            if cantidad <= 0:
                messagebox.showwarning("Validación", "La cantidad debe ser mayor a 0")
                return
            
            # Crear detalle del pedido
            detalle = PedidoControlador.crear_detalle_pedido(self.current_pedido_id, producto_id, cantidad)
            
            if detalle:
                messagebox.showinfo("Éxito", "Producto agregado al pedido")
                self.cantidad_var.set("")
                self.refresh_detalles()
            else:
                messagebox.showerror("Error", "No se pudo agregar el producto")
                
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")

    def crear_pedido(self):
        """Finaliza y crea el pedido con todos sus detalles"""
        if not self.current_pedido_id:
            messagebox.showwarning("Validación", "No hay un pedido abierto")
            return
        
        try:
            # Obtener todos los detalles del pedido
            detalles = DetallePedidoControlador.obtener_detalle_completo_pedido(self.current_pedido_id)
            
            if not detalles or len(detalles) == 0:
                messagebox.showwarning("Validación", "Debe agregar al menos un producto al pedido")
                return
            
            # Crear el pedido final
            pedido = PedidoControlador.crear_pedido(self.current_pedido_id, list(detalles))
            
            if pedido:
                messagebox.showinfo("Éxito", f"Pedido #{pedido.id} creado exitosamente\nMonto total: ${float(pedido.monto_final):.2f}")
                self.current_pedido_id = None
                self.status_var.set("No hay pedido abierto")
                self.refresh_detalles()
                self.refresh()
            else:
                messagebox.showerror("Error", "No se pudo crear el pedido")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear pedido: {str(e)}")

    def refresh_detalles(self):
        """Actualiza la vista de detalles del pedido actual"""
        # Limpiar el treeview de detalles
        for item in self.detail_tree.get_children():
            self.detail_tree.delete(item)
        
        if not self.current_pedido_id:
            self.subtotal_var.set("0.00")
            self.ganancia_var.set("0.00")
            return
        
        try:
            # Obtener detalles del pedido actual
            detalles = DetallePedidoControlador.obtener_detalle_completo_pedido(self.current_pedido_id)
            
            total_subtotal = 0
            total_ganancia = 0
            
            if detalles:
                for detalle in detalles:
                    # Obtener información del producto
                    producto = ProductoControlador.obtener_producto(detalle.producto_id)
                    producto_nombre = producto.codigo if producto else "Producto no encontrado"
                    
                    values = (
                        detalle.id,
                        producto_nombre,
                        detalle.cantidad,
                        f"{float(producto.precio_venta):.2f}" if producto else "0.00",
                        f"{float(detalle.subtotal):.2f}"
                    )
                    self.detail_tree.insert("", "end", values=values)
                    
                    total_subtotal += float(detalle.subtotal)
                    total_ganancia += float(detalle.ganancia_per_detalle)
            
            self.subtotal_var.set(f"{total_subtotal:.2f}")
            self.ganancia_var.set(f"{total_ganancia:.2f}")
            
        except Exception as e:
            print(f"Error al actualizar detalles: {e}")

    def delete_detalle(self, event):
        """Elimina un detalle del pedido con doble clic"""
        selected = self.detail_tree.focus()
        if not selected:
            return
        
        values = self.detail_tree.item(selected, 'values')
        detalle_id = values[0]
        producto_name = values[1]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar {producto_name} del pedido?"):
            success = DetallePedidoControlador.eliminar_detalle(int(detalle_id))
            if success:
                self.refresh_detalles()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto")

    def cancel_current_pedido(self):
        """Cancela el pedido actual"""
        if not self.current_pedido_id:
            messagebox.showwarning("Validación", "No hay un pedido abierto")
            return
        
        if messagebox.askyesno("Confirmar", "¿Cancelar el pedido actual? Se perderán todos los productos agregados."):
            success = PedidoControlador.eliminar_pedido(self.current_pedido_id)
            if success:
                self.current_pedido_id = None
                self.status_var.set("Pedido cancelado")
                self.refresh_detalles()
                self.refresh()
            else:
                messagebox.showerror("Error", "No se pudo cancelar el pedido")

    def on_select_pedido(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.selected_pedido_id = values[0]

    def update_estado(self):
        """Actualiza el estado del pedido seleccionado"""
        if not self.selected_pedido_id:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un pedido")
            return
        
        try:
            selected_item = self.tree.focus()
            if not selected_item:
                messagebox.showwarning("Selección requerida", "Por favor seleccione un pedido")
                return
                
            values = self.tree.item(selected_item, 'values')
            if not values or len(values) < 2:
                messagebox.showerror("Error", "No se pudo obtener la información del pedido")
                return
                
            pedido_id = values[0]
            cliente_name = values[1]
            
            confirm_msg = f"¿Completar pedido y migrar a ventas?\n\n"
            confirm_msg += f"Pedido ID: {pedido_id}\n"
            confirm_msg += f"Cliente: {cliente_name}\n\n"
            confirm_msg += "Esta acción moverá el pedido a la sección de ventas."
            
            if messagebox.askyesno("Confirmar completar pedido", confirm_msg):
                venta = PedidoControlador.actualizar_estado(int(self.selected_pedido_id))
                if venta:
                    messagebox.showinfo("Éxito", f"Pedido #{pedido_id} completado y migrado a ventas como venta #{venta.id}")
                    self.refresh()
                    # Refrescar también la vista de ventas si existe el callback
                    if self.refresh_purchases_cb:
                        self.refresh_purchases_cb()
                    # Forzar actualización de la interfaz
                    self.update_idletasks()
                else:
                    messagebox.showerror("Error", "No se pudo completar el pedido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al completar pedido: {str(e)}")

    def delete_selected(self):
        """Elimina el pedido seleccionado"""
        if not self.selected_pedido_id:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un pedido para eliminar")
            return
        
        try:
            selected_item = self.tree.focus()
            if not selected_item:
                messagebox.showwarning("Selección requerida", "Por favor seleccione un pedido para eliminar")
                return
                
            values = self.tree.item(selected_item, 'values')
            if not values or len(values) < 2:
                messagebox.showerror("Error", "No se pudo obtener la información del pedido seleccionado")
                return
                
            pedido_id = values[0]
            cliente_name = values[1]
            
            if messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar el pedido #{pedido_id} del cliente '{cliente_name}'?"):
                success = PedidoControlador.eliminar_pedido(int(self.selected_pedido_id))
                
                if success:
                    messagebox.showinfo("Éxito", "Pedido eliminado exitosamente")
                    self.refresh()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el pedido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar pedido: {str(e)}")

    def refresh(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            search_term = self.search_var.get().strip()
            pedidos = PedidoControlador.listar_pedidos(search_term)
            
            if pedidos:
                for pedido in pedidos:
                    try:
                        # Obtener nombre del cliente
                        cliente = ClientesControlador.obtener_cliente(pedido.cliente.id)
                        cliente_nombre = cliente.nombre if cliente else "Cliente no encontrado"
                        
                        # Formatear fecha
                        fecha_str = pedido.fecha.strftime("%Y-%m-%d %H:%M") if pedido.fecha else ""
                        
                        # Obtener estado
                        estados = {1: "Pendiente", 2: "En Proceso", 3: "Completado", 4: "Cancelado"}
                        estado_nombre = estados.get(pedido.estado.id, "Desconocido")
                        
                        values = (
                            pedido.id,
                            cliente_nombre,
                            f"{float(pedido.monto_final):.2f}",
                            estado_nombre,
                            f"{float(pedido.ganancia_total):.2f}",
                            fecha_str
                        )
                        self.tree.insert("", "end", values=values)
                    except Exception as e:
                        print(f"Error al procesar pedido {pedido.id}: {e}")
            else:
                print("No se encontraron pedidos")
        except Exception as e:
            print(f"Error en refresh de pedidos: {e}")
            messagebox.showerror("Error", f"Error al cargar pedidos: {str(e)}")

    def clear_search(self):
        self.search_var.set("")
        self.refresh()

    def view_pedido_details(self):
        """Muestra los detalles completos del pedido seleccionado"""
        if not self.selected_pedido_id:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un pedido")
            return
        
        try:
            # Obtener información del pedido
            pedido = PedidoControlador.obtener_pedido(int(self.selected_pedido_id))
            if not pedido:
                messagebox.showerror("Error", "No se pudo obtener la información del pedido")
                return
            
            # Obtener cliente
            cliente = ClientesControlador.obtener_cliente(pedido.cliente.id)
            cliente_nombre = cliente.nombre if cliente else "Cliente no encontrado"
            
            # Obtener detalles del pedido
            detalles = DetallePedidoControlador.obtener_detalle_completo_pedido(int(self.selected_pedido_id))
            
            # Crear ventana de detalles
            detail_window = tk.Toplevel(self)
            detail_window.title(f"Detalles del Pedido #{pedido.id}")
            detail_window.geometry("700x500")
            detail_window.resizable(True, True)
            
            # Frame principal con scroll
            main_frame = ttk.Frame(detail_window)
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Información del pedido
            info_frame = ttk.LabelFrame(main_frame, text="Información del Pedido")
            info_frame.pack(fill="x", pady=(0, 10))
            
            info_grid = ttk.Frame(info_frame)
            info_grid.pack(fill="x", padx=10, pady=10)
            
            ttk.Label(info_grid, text="ID Pedido:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="e", padx=5, pady=2)
            ttk.Label(info_grid, text=str(pedido.id)).grid(row=0, column=1, sticky="w", padx=5, pady=2)
            
            ttk.Label(info_grid, text="Cliente:", font=("Arial", 9, "bold")).grid(row=0, column=2, sticky="e", padx=5, pady=2)
            ttk.Label(info_grid, text=cliente_nombre).grid(row=0, column=3, sticky="w", padx=5, pady=2)
            
            ttk.Label(info_grid, text="Monto Final:", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky="e", padx=5, pady=2)
            ttk.Label(info_grid, text=f"${float(pedido.monto_final):.2f}", foreground="green").grid(row=1, column=1, sticky="w", padx=5, pady=2)
            
            ttk.Label(info_grid, text="Ganancia:", font=("Arial", 9, "bold")).grid(row=1, column=2, sticky="e", padx=5, pady=2)
            ttk.Label(info_grid, text=f"${float(pedido.ganancia_total):.2f}", foreground="blue").grid(row=1, column=3, sticky="w", padx=5, pady=2)
            
            ttk.Label(info_grid, text="Fecha:", font=("Arial", 9, "bold")).grid(row=2, column=0, sticky="e", padx=5, pady=2)
            fecha_str = pedido.fecha.strftime("%Y-%m-%d %H:%M:%S") if pedido.fecha else "N/A"
            ttk.Label(info_grid, text=fecha_str).grid(row=2, column=1, sticky="w", padx=5, pady=2)
            
            estados = {1: "Pendiente", 2: "En Proceso", 3: "Completado", 4: "Cancelado"}
            estado_nombre = estados.get(pedido.estado.id, "Desconocido")
            ttk.Label(info_grid, text="Estado:", font=("Arial", 9, "bold")).grid(row=2, column=2, sticky="e", padx=5, pady=2)
            ttk.Label(info_grid, text=estado_nombre).grid(row=2, column=3, sticky="w", padx=5, pady=2)
            
            # Productos del pedido
            products_frame = ttk.LabelFrame(main_frame, text="Productos en el Pedido")
            products_frame.pack(fill="both", expand=True, pady=(0, 10))
            
            # Treeview para productos
            cols = ("producto", "codigo", "cantidad", "precio_unitario", "subtotal", "ganancia")
            products_tree = ttk.Treeview(products_frame, columns=cols, show="headings", height=10)
            
            products_tree.heading("producto", text="Producto")
            products_tree.heading("codigo", text="Código")
            products_tree.heading("cantidad", text="Cantidad")
            products_tree.heading("precio_unitario", text="Precio Unit.")
            products_tree.heading("subtotal", text="Subtotal")
            products_tree.heading("ganancia", text="Ganancia")
            
            products_tree.column("producto", width=150, anchor="w")
            products_tree.column("codigo", width=100, anchor="w")
            products_tree.column("cantidad", width=80, anchor="center")
            products_tree.column("precio_unitario", width=100, anchor="e")
            products_tree.column("subtotal", width=100, anchor="e")
            products_tree.column("ganancia", width=100, anchor="e")
            
            # Scrollbar para productos
            products_scrollbar = ttk.Scrollbar(products_frame, orient="vertical", command=products_tree.yview)
            products_tree.configure(yscrollcommand=products_scrollbar.set)
            
            products_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            products_scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
            
            # Llenar datos de productos
            if detalles:
                for detalle in detalles:
                    producto = ProductoControlador.obtener_producto(detalle.producto_id)
                    if producto:
                        values = (
                            f"ID: {producto.id}",
                            producto.codigo,
                            detalle.cantidad,
                            f"${float(producto.precio_venta):.2f}",
                            f"${float(detalle.subtotal):.2f}",
                            f"${float(detalle.ganancia_per_detalle):.2f}"
                        )
                        products_tree.insert("", "end", values=values)
            
            # Botones
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill="x", pady=(10, 0))
            
            ttk.Button(button_frame, text="Cerrar", command=detail_window.destroy).pack(side="right", padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar detalles: {str(e)}")

    def delete_all_pedidos(self):
        """Elimina todos los pedidos de la base de datos"""
        confirm_msg = "⚠️ ADVERTENCIA ⚠️\n\n"
        confirm_msg += "Esta acción eliminará TODOS los pedidos y sus detalles.\n"
        confirm_msg += "También se eliminarán todas las ventas relacionadas.\n\n"
        confirm_msg += "Esta acción NO se puede deshacer.\n\n"
        confirm_msg += "¿Está seguro de que desea continuar?"
        
        if messagebox.askyesno("Confirmar eliminación masiva", confirm_msg):
            # Doble confirmación
            if messagebox.askyesno("Confirmación final", "¿Realmente desea eliminar TODOS los pedidos?\n\nEsta es su última oportunidad para cancelar."):
                try:
                    success = PedidoControlador.eliminar_todos()
                    if success:
                        messagebox.showinfo("Éxito", "Todos los pedidos han sido eliminados exitosamente")
                        self.current_pedido_id = None
                        self.status_var.set("No hay pedido abierto")
                        self.refresh_detalles()
                        self.refresh()
                        # Refrescar también la vista de ventas si existe el callback
                        if self.refresh_purchases_cb:
                            self.refresh_purchases_cb()
                    else:
                        messagebox.showerror("Error", "No se pudieron eliminar todos los pedidos")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar pedidos: {str(e)}")