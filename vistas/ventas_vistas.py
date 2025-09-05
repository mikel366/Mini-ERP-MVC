# app/vistas/ventas_vistas.py
import tkinter as tk
from tkinter import ttk, messagebox
from controladores import VentaControlador, ClientesControlador
from datetime import datetime
import calendar

class VentasTab(ttk.Frame):
    def __init__(self, master, refresh_purchases_cb=None):
        super().__init__(master)
        self.refresh_purchases_cb = refresh_purchases_cb
        self.selected_venta_id = None
        self.build_ui()
        self.refresh()

    def build_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=6, pady=6)
        
        # Frame de búsqueda y filtros
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill="x", padx=6, pady=6)
        
        ttk.Label(search_frame, text="Buscar:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=6)
        search_entry.bind('<KeyRelease>', lambda e: self.refresh())
        
        ttk.Button(search_frame, text="Limpiar", command=self.clear_search).pack(side="left", padx=4)
        
        # Separador
        ttk.Separator(search_frame, orient="vertical").pack(side="left", fill="y", padx=10)
        
        # Filtros de fecha
        ttk.Label(search_frame, text="Filtrar por mes:").pack(side="left", padx=(10, 5))
        self.month_var = tk.StringVar()
        month_combo = ttk.Combobox(search_frame, textvariable=self.month_var, width=12, state="readonly")
        months = ["Todos"] + [f"{i:02d} - {calendar.month_name[i]}" for i in range(1, 13)]
        month_combo['values'] = months
        month_combo.set("Todos")
        month_combo.pack(side="left", padx=5)
        month_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh())
        
        ttk.Label(search_frame, text="Año:").pack(side="left", padx=(10, 5))
        self.year_var = tk.StringVar()
        year_combo = ttk.Combobox(search_frame, textvariable=self.year_var, width=8, state="readonly")
        current_year = datetime.now().year
        years = ["Todos"] + [str(year) for year in range(current_year - 5, current_year + 2)]
        year_combo['values'] = years
        year_combo.set("Todos")
        year_combo.pack(side="left", padx=5)
        year_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh())

        # Frame de estadísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estadísticas de Ventas")
        stats_frame.pack(fill="x", padx=6, pady=6)
        
        stats_inner = ttk.Frame(stats_frame)
        stats_inner.pack(fill="x", padx=6, pady=6)
        
        # Total ventas
        ttk.Label(stats_inner, text="Total Ventas:").grid(row=0, column=0, padx=6, pady=3, sticky="e")
        self.total_ventas_var = tk.StringVar(value="0")
        ttk.Label(stats_inner, textvariable=self.total_ventas_var, font=("Arial", 10, "bold")).grid(row=0, column=1, padx=6, pady=3, sticky="w")
        
        # Monto total
        ttk.Label(stats_inner, text="Monto Total:").grid(row=0, column=2, padx=6, pady=3, sticky="e")
        self.monto_total_var = tk.StringVar(value="$0.00")
        ttk.Label(stats_inner, textvariable=self.monto_total_var, font=("Arial", 10, "bold"), foreground="green").grid(row=0, column=3, padx=6, pady=3, sticky="w")
        
        # Ganancia total
        ttk.Label(stats_inner, text="Ganancia Total:").grid(row=0, column=4, padx=6, pady=3, sticky="e")
        self.ganancia_total_var = tk.StringVar(value="$0.00")
        ttk.Label(stats_inner, textvariable=self.ganancia_total_var, font=("Arial", 10, "bold"), foreground="blue").grid(row=0, column=5, padx=6, pady=3, sticky="w")
        
        # Promedio por venta
        ttk.Label(stats_inner, text="Promedio/Venta:").grid(row=1, column=0, padx=6, pady=3, sticky="e")
        self.promedio_var = tk.StringVar(value="$0.00")
        ttk.Label(stats_inner, textvariable=self.promedio_var, font=("Arial", 10, "bold")).grid(row=1, column=1, padx=6, pady=3, sticky="w")

        # Frame de gestión
        manage_frame = ttk.LabelFrame(main_frame, text="Gestión de Ventas")
        manage_frame.pack(fill="x", padx=6, pady=6)
        
        button_frame = ttk.Frame(manage_frame)
        button_frame.pack(fill="x", padx=6, pady=6)
        
        ttk.Button(button_frame, text="Revertir a Pedido", command=self.revert_to_pedido).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Eliminar Venta", command=self.delete_selected).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Ver Detalles", command=self.view_details).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Exportar", command=self.export_sales).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Actualizar", command=self.refresh).pack(side="left", padx=2)
        ttk.Button(button_frame, text="🗑️ Eliminar Todas", command=self.delete_all_ventas, 
                  style="Accent.TButton").pack(side="right", padx=2)

        # Treeview para listar ventas
        cols = ("id", "pedido_id", "cliente", "monto_final", "ganancia_total", "fecha", "estado")
        self.tree = ttk.Treeview(main_frame, columns=cols, show="headings", height=15)
        
        # Configurar columnas
        self.tree.heading("id", text="ID Venta")
        self.tree.heading("pedido_id", text="ID Pedido")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("monto_final", text="Monto Final")
        self.tree.heading("ganancia_total", text="Ganancia")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("estado", text="Estado")
        
        self.tree.column("id", width=70, anchor="center")
        self.tree.column("pedido_id", width=80, anchor="center")
        self.tree.column("cliente", width=150, anchor="w")
        self.tree.column("monto_final", width=100, anchor="e")
        self.tree.column("ganancia_total", width=100, anchor="e")
        self.tree.column("fecha", width=120, anchor="center")
        self.tree.column("estado", width=100, anchor="center")
        
        # Scrollbar para el treeview
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        scrollbar.pack(side="right", fill="y", padx=(0, 6), pady=6)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.bind('<Double-1>', self.view_details)

    def on_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.selected_venta_id = values[0]

    def refresh(self):
        # Limpiar el treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_term = self.search_var.get().strip()
        ventas = VentaControlador.listar_ventas(search_term)
        
        # Variables para estadísticas
        total_ventas = 0
        monto_total = 0.0
        ganancia_total = 0.0
        
        if ventas:
            for venta in ventas:
                try:
                    # Filtrar por mes y año si están seleccionados
                    if not self.filter_by_date(venta.fecha):
                        continue
                    
                    # Obtener nombre del cliente
                    cliente = ClientesControlador.obtener_cliente(venta.cliente.id)
                    cliente_nombre = cliente.nombre if cliente else "Cliente no encontrado"
                    
                    # Formatear fecha
                    fecha_str = venta.fecha.strftime("%Y-%m-%d %H:%M") if venta.fecha else ""
                    
                    # Obtener estado
                    estados = {1: "Pendiente", 2: "En Proceso", 3: "Completado", 4: "Cancelado"}
                    estado_nombre = estados.get(venta.estado_id, "Completado")
                    
                    values = (
                        venta.id,
                        venta.pedido_id,
                        cliente_nombre,
                        f"${float(venta.monto_final):.2f}",
                        f"${float(venta.ganancia_total):.2f}",
                        fecha_str,
                        estado_nombre
                    )
                    self.tree.insert("", "end", values=values)
                    
                    # Actualizar estadísticas
                    total_ventas += 1
                    monto_total += float(venta.monto_final)
                    ganancia_total += float(venta.ganancia_total)
                    
                except Exception as e:
                    print(f"Error al procesar venta {venta.id}: {e}")
        
        # Actualizar estadísticas
        self.update_statistics(total_ventas, monto_total, ganancia_total)

    def filter_by_date(self, fecha):
        """Filtra las ventas por mes y año seleccionados"""
        if not fecha:
            return True
        
        month_filter = self.month_var.get()
        year_filter = self.year_var.get()
        
        if month_filter != "Todos":
            selected_month = int(month_filter.split(" - ")[0])
            if fecha.month != selected_month:
                return False
        
        if year_filter != "Todos":
            selected_year = int(year_filter)
            if fecha.year != selected_year:
                return False
        
        return True

    def update_statistics(self, total_ventas, monto_total, ganancia_total):
        """Actualiza las estadísticas mostradas"""
        self.total_ventas_var.set(str(total_ventas))
        self.monto_total_var.set(f"${monto_total:.2f}")
        self.ganancia_total_var.set(f"${ganancia_total:.2f}")
        
        promedio = monto_total / total_ventas if total_ventas > 0 else 0
        self.promedio_var.set(f"${promedio:.2f}")

    def clear_search(self):
        self.search_var.set("")
        self.month_var.set("Todos")
        self.year_var.set("Todos")
        self.refresh()

    def revert_to_pedido(self):
        """Revierte una venta a pedido"""
        if not self.selected_venta_id:
            messagebox.showwarning("Selección requerida", "Por favor seleccione una venta")
            return
        
        try:
            selected_item = self.tree.focus()
            values = self.tree.item(selected_item, 'values')
            venta_id = values[0]
            cliente_name = values[2]
            monto = values[3]
            
            confirm_msg = f"¿Está seguro de que desea revertir la venta a pedido?\n\n"
            confirm_msg += f"Venta ID: {venta_id}\n"
            confirm_msg += f"Cliente: {cliente_name}\n"
            confirm_msg += f"Monto: {monto}\n\n"
            confirm_msg += "Esta acción convertirá la venta de vuelta a un pedido pendiente."
            
            if messagebox.askyesno("Confirmar reversión", confirm_msg):
                pedido = VentaControlador.cambiar_estado(int(self.selected_venta_id))
                
                if pedido:
                    messagebox.showinfo("Éxito", f"Venta #{venta_id} revertida a pedido #{pedido.id} exitosamente")
                    self.refresh()
                    # Refrescar también la vista de pedidos si existe el callback
                    if self.refresh_purchases_cb:
                        self.refresh_purchases_cb()
                    # Forzar actualización de la interfaz
                    self.update_idletasks()
                else:
                    messagebox.showerror("Error", "No se pudo revertir la venta. Verifique que la venta existe y no tenga dependencias.")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al revertir venta: {str(e)}")

    def delete_selected(self):
        """Elimina la venta seleccionada"""
        if not self.selected_venta_id:
            messagebox.showwarning("Selección requerida", "Por favor seleccione una venta para eliminar")
            return
        
        selected_item = self.tree.focus()
        values = self.tree.item(selected_item, 'values')
        venta_id = values[0]
        cliente_name = values[2]
        monto = values[3]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar la venta #{venta_id} del cliente '{cliente_name}' ({monto})?\n\nEsta acción no se puede deshacer."):
            success = VentaControlador.eliminar_venta(int(self.selected_venta_id))
            
            if success:
                messagebox.showinfo("Éxito", "Venta eliminada exitosamente")
                self.refresh()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la venta")

    def view_details(self, event=None):
        """Muestra los detalles completos de la venta seleccionada"""
        if not self.selected_venta_id:
            messagebox.showwarning("Selección requerida", "Por favor seleccione una venta")
            return
        
        try:
            venta = VentaControlador.obtener_venta(int(self.selected_venta_id))
            if not venta:
                messagebox.showerror("Error", "No se pudo obtener la información de la venta")
                return
            
            # Obtener información del cliente
            cliente = ClientesControlador.obtener_cliente(venta.cliente.id)
            cliente_nombre = cliente.nombre if cliente else "Cliente no encontrado"
            
            # Crear ventana de detalles
            detail_window = tk.Toplevel(self)
            detail_window.title(f"Detalles de Venta #{venta.id}")
            detail_window.geometry("700x500")
            detail_window.resizable(True, True)
            
            # Frame principal
            main_frame = ttk.Frame(detail_window)
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Información de la venta
            info_frame = ttk.LabelFrame(main_frame, text="Información de la Venta")
            info_frame.pack(fill="x", pady=(0, 10))
            
            info_grid = ttk.Frame(info_frame)
            info_grid.pack(fill="x", padx=10, pady=10)
            
            ttk.Label(info_grid, text="ID Venta:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="e", padx=5, pady=2)
            ttk.Label(info_grid, text=str(venta.id)).grid(row=0, column=1, sticky="w", padx=5, pady=2)
            
            ttk.Label(info_grid, text="ID Pedido Original:", font=("Arial", 9, "bold")).grid(row=0, column=2, sticky="e", padx=5, pady=2)
            ttk.Label(info_grid, text=str(venta.pedido_id)).grid(row=0, column=3, sticky="w", padx=5, pady=2)
            
            ttk.Label(info_grid, text="Cliente:", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky="e", padx=5, pady=2)
            ttk.Label(info_grid, text=cliente_nombre).grid(row=1, column=1, sticky="w", padx=5, pady=2)
            
            ttk.Label(info_grid, text="Monto Final:", font=("Arial", 9, "bold")).grid(row=1, column=2, sticky="e", padx=5, pady=2)
            ttk.Label(info_grid, text=f"${float(venta.monto_final):.2f}", foreground="green").grid(row=1, column=3, sticky="w", padx=5, pady=2)
            
            ttk.Label(info_grid, text="Ganancia Total:", font=("Arial", 9, "bold")).grid(row=2, column=0, sticky="e", padx=5, pady=2)
            ttk.Label(info_grid, text=f"${float(venta.ganancia_total):.2f}", foreground="blue").grid(row=2, column=1, sticky="w", padx=5, pady=2)
            
            ttk.Label(info_grid, text="Fecha:", font=("Arial", 9, "bold")).grid(row=2, column=2, sticky="e", padx=5, pady=2)
            fecha_str = venta.fecha.strftime("%Y-%m-%d %H:%M:%S") if venta.fecha else "N/A"
            ttk.Label(info_grid, text=fecha_str).grid(row=2, column=3, sticky="w", padx=5, pady=2)
            
            # Nota informativa
            note_frame = ttk.Frame(main_frame)
            note_frame.pack(fill="x", pady=(0, 10))
            ttk.Label(note_frame, text="Nota: Los productos mostrados corresponden al pedido original que generó esta venta.", 
                     font=("Arial", 8), foreground="gray").pack()
            
            # Productos de la venta (obtenidos del pedido original)
            try:
                from controladores import DetallePedidoControlador
                detalles = DetallePedidoControlador.obtener_detalle_completo_pedido(venta.pedido_id)
                
                products_frame = ttk.LabelFrame(main_frame, text="Productos Vendidos")
                products_frame.pack(fill="both", expand=True, pady=(0, 10))
                
                if detalles and len(detalles) > 0:
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
                    for detalle in detalles:
                        from controladores import ProductoControlador
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
                else:
                    ttk.Label(products_frame, text="No se encontraron detalles del pedido original.", 
                             font=("Arial", 10), foreground="red").pack(pady=20)
                    
            except Exception as e:
                ttk.Label(products_frame, text=f"Error al cargar productos: {str(e)}", 
                         font=("Arial", 10), foreground="red").pack(pady=20)
            
            # Botones
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill="x", pady=(10, 0))
            
            ttk.Button(button_frame, text="Cerrar", command=detail_window.destroy).pack(side="right", padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar detalles: {str(e)}")

    def export_sales(self):
        """Exporta las ventas a un archivo de texto"""
        try:
            ventas = VentaControlador.listar_ventas()
            if not ventas:
                messagebox.showwarning("Sin datos", "No hay ventas para exportar")
                return
            
            filename = f"ventas_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("REPORTE DE VENTAS\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                total_monto = 0
                total_ganancia = 0
                
                for venta in ventas:
                    cliente = ClientesControlador.obtener_cliente(venta.cliente.id)
                    cliente_nombre = cliente.nombre if cliente else "Cliente no encontrado"
                    
                    f.write(f"Venta ID: {venta.id}\n")
                    f.write(f"Pedido ID: {venta.pedido_id}\n")
                    f.write(f"Cliente: {cliente_nombre}\n")
                    f.write(f"Monto: ${float(venta.monto_final):.2f}\n")
                    f.write(f"Ganancia: ${float(venta.ganancia_total):.2f}\n")
                    f.write(f"Fecha: {venta.fecha.strftime('%Y-%m-%d %H:%M:%S') if venta.fecha else 'N/A'}\n")
                    f.write("-" * 30 + "\n")
                    
                    total_monto += float(venta.monto_final)
                    total_ganancia += float(venta.ganancia_total)
                
                f.write(f"\nRESUMEN:\n")
                f.write(f"Total Ventas: {len(ventas)}\n")
                f.write(f"Monto Total: ${total_monto:.2f}\n")
                f.write(f"Ganancia Total: ${total_ganancia:.2f}\n")
            
            messagebox.showinfo("Éxito", f"Ventas exportadas a: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")

    def delete_all_ventas(self):
        """Elimina todas las ventas de la base de datos"""
        confirm_msg = "⚠️ ADVERTENCIA ⚠️\n\n"
        confirm_msg += "Esta acción eliminará TODAS las ventas de la base de datos.\n\n"
        confirm_msg += "Esta acción NO se puede deshacer.\n\n"
        confirm_msg += "¿Está seguro de que desea continuar?"
        
        if messagebox.askyesno("Confirmar eliminación masiva", confirm_msg):
            # Doble confirmación
            if messagebox.askyesno("Confirmación final", "¿Realmente desea eliminar TODAS las ventas?\n\nEsta es su última oportunidad para cancelar."):
                try:
                    success = VentaControlador.eliminar_todas()
                    if success:
                        messagebox.showinfo("Éxito", "Todas las ventas han sido eliminadas exitosamente")
                        self.refresh()
                        # Refrescar también la vista de pedidos si existe el callback
                        if self.refresh_purchases_cb:
                            self.refresh_purchases_cb()
                    else:
                        messagebox.showerror("Error", "No se pudieron eliminar todas las ventas")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar ventas: {str(e)}")

    def cargar_clientes(self):
        """Carga la lista de clientes (método dummy para compatibilidad)"""
        pass
    
    def cargar_productos(self):
        """Carga la lista de productos (método dummy para compatibilidad)"""
        pass