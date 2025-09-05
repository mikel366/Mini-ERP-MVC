# app/vistas/productos_vistas.py
import tkinter as tk
from tkinter import ttk, messagebox
from controladores import ProductoControlador

class ProductosTab(ttk.Frame):
    def __init__(self, master, refresh_purchases_cb=None):
        super().__init__(master)
        self.refresh_purchases_cb = refresh_purchases_cb
        self.selected_product_id = None
        self.build_ui()
        self.refresh()

    def build_ui(self):
        # Frame principal con padding mejorado
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header con título y estadísticas
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        
        title_label = ttk.Label(header_frame, text="Gestión de Productos", font=("Arial", 14, "bold"))
        title_label.pack(side="left")
        
        self.stats_label = ttk.Label(header_frame, text="Total: 0 productos", font=("Arial", 10), foreground="gray")
        self.stats_label.pack(side="right")
        
        # Frame de búsqueda mejorado
        search_frame = ttk.LabelFrame(main_frame, text="Búsqueda y Filtros", padding=10)
        search_frame.pack(fill="x", pady=(0, 10))
        
        search_grid = ttk.Frame(search_frame)
        search_grid.pack(fill="x")
        
        ttk.Label(search_grid, text="Buscar producto:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_grid, textvariable=self.search_var, width=40, font=("Arial", 10))
        search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        search_entry.bind('<KeyRelease>', lambda e: self.refresh())
        
        ttk.Button(search_grid, text="🔍 Buscar", command=self.refresh).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(search_grid, text="✖ Limpiar", command=self.clear_search).grid(row=0, column=3)
        
        search_grid.columnconfigure(1, weight=1)

        # Frame de formulario mejorado
        form_frame = ttk.LabelFrame(main_frame, text="Información del Producto", padding=15)
        form_frame.pack(fill="x", pady=(0, 10))
        
        # Grid para el formulario
        form_grid = ttk.Frame(form_frame)
        form_grid.pack(fill="x")
        
        # Primera fila
        ttk.Label(form_grid, text="Página:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="e", padx=(0, 10), pady=5)
        self.pagina_var = tk.StringVar()
        pagina_entry = ttk.Entry(form_grid, textvariable=self.pagina_var, width=15, font=("Arial", 10))
        pagina_entry.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=5)
        
        ttk.Label(form_grid, text="Código:", font=("Arial", 9, "bold")).grid(row=0, column=2, sticky="e", padx=(0, 10), pady=5)
        self.codigo_var = tk.StringVar()
        codigo_entry = ttk.Entry(form_grid, textvariable=self.codigo_var, width=25, font=("Arial", 10))
        codigo_entry.grid(row=0, column=3, sticky="ew", pady=5)
        
        # Segunda fila
        ttk.Label(form_grid, text="Precio Compra:", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky="e", padx=(0, 10), pady=5)
        self.precio_compra_var = tk.StringVar()
        precio_compra_entry = ttk.Entry(form_grid, textvariable=self.precio_compra_var, width=15, font=("Arial", 10))
        precio_compra_entry.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=5)
        
        ttk.Label(form_grid, text="Precio Venta:", font=("Arial", 9, "bold")).grid(row=1, column=2, sticky="e", padx=(0, 10), pady=5)
        self.precio_venta_var = tk.StringVar()
        precio_venta_entry = ttk.Entry(form_grid, textvariable=self.precio_venta_var, width=15, font=("Arial", 10))
        precio_venta_entry.grid(row=1, column=3, sticky="w", pady=5)
        
        # Margen de ganancia calculado
        self.margen_label = ttk.Label(form_grid, text="Margen: $0.00 (0%)", font=("Arial", 9), foreground="blue")
        self.margen_label.grid(row=2, column=1, columnspan=2, sticky="w", pady=(5, 0))
        
        # Bind para calcular margen automáticamente
        precio_compra_entry.bind('<KeyRelease>', self.calculate_margin)
        precio_venta_entry.bind('<KeyRelease>', self.calculate_margin)
        
        # Estado del formulario
        self.form_status_label = ttk.Label(form_grid, text="Modo: Nuevo producto", font=("Arial", 9), foreground="blue")
        self.form_status_label.grid(row=2, column=3, sticky="e", pady=(5, 0))
        
        form_grid.columnconfigure(3, weight=1)
        
        # Frame de botones mejorado
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x", pady=(15, 0))
        
        # Botones principales
        btn_style = {"width": 12, "padding": 5}
        ttk.Button(button_frame, text="💾 Guardar", command=self.save, **btn_style).pack(side="left", padx=(0, 5))
        ttk.Button(button_frame, text="✏️ Editar", command=self.edit_selected, **btn_style).pack(side="left", padx=(0, 5))
        ttk.Button(button_frame, text="🗑️ Eliminar", command=self.delete_selected, **btn_style).pack(side="left", padx=(0, 5))
        ttk.Button(button_frame, text="➕ Nuevo", command=self.new, **btn_style).pack(side="left", padx=(0, 10))
        
        # Botones secundarios
        ttk.Button(button_frame, text="❌ Cancelar", command=self.cancel_edit, width=12).pack(side="left", padx=(0, 10))
        
        # Botones de la derecha
        ttk.Button(button_frame, text="🗑️ Eliminar Todos", command=self.delete_all_productos, 
                  style="Accent.TButton", width=15).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="🔄 Actualizar", command=self.refresh, width=12).pack(side="right")

        # Frame de lista mejorado
        list_frame = ttk.LabelFrame(main_frame, text="Lista de Productos", padding=10)
        list_frame.pack(fill="both", expand=True)
        
        # Treeview con scrollbars
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill="both", expand=True)
        
        cols = ("id", "pagina", "codigo", "precio_compra", "precio_venta", "margen")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=12)
        
        # Configurar columnas
        self.tree.heading("id", text="ID", anchor="center")
        self.tree.heading("pagina", text="Página", anchor="center")
        self.tree.heading("codigo", text="Código del Producto", anchor="w")
        self.tree.heading("precio_compra", text="P. Compra", anchor="e")
        self.tree.heading("precio_venta", text="P. Venta", anchor="e")
        self.tree.heading("margen", text="Margen", anchor="e")
        
        self.tree.column("id", width=60, anchor="center", minwidth=50)
        self.tree.column("pagina", width=80, anchor="center", minwidth=60)
        self.tree.column("codigo", width=200, anchor="w", minwidth=150)
        self.tree.column("precio_compra", width=100, anchor="e", minwidth=80)
        self.tree.column("precio_venta", width=100, anchor="e", minwidth=80)
        self.tree.column("margen", width=100, anchor="e", minwidth=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars y treeview
        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.bind('<Double-1>', self.on_double_click)
        
        # Configurar tags para alternar colores de filas
        self.tree.tag_configure('evenrow', background='#f0f0f0')
        self.tree.tag_configure('oddrow', background='white')
        self.tree.tag_configure('low_margin', background='#ffe6e6')  # Rojo claro para margen bajo
        self.tree.tag_configure('high_margin', background='#e6ffe6')  # Verde claro para margen alto

    def calculate_margin(self, event=None):
        """Calcula y muestra el margen de ganancia"""
        try:
            precio_compra = float(self.precio_compra_var.get() or 0)
            precio_venta = float(self.precio_venta_var.get() or 0)
            
            if precio_compra > 0:
                margen_absoluto = precio_venta - precio_compra
                margen_porcentaje = (margen_absoluto / precio_compra) * 100
                
                color = "green" if margen_porcentaje > 20 else "orange" if margen_porcentaje > 10 else "red"
                self.margen_label.config(
                    text=f"Margen: ${margen_absoluto:.2f} ({margen_porcentaje:.1f}%)",
                    foreground=color
                )
            else:
                self.margen_label.config(text="Margen: $0.00 (0%)", foreground="blue")
        except ValueError:
            self.margen_label.config(text="Margen: $0.00 (0%)", foreground="blue")

    def on_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.selected_product_id = values[0]
            self.pagina_var.set(values[1])
            self.codigo_var.set(values[2])
            # Remover formato de precio para edición
            precio_compra = values[3].replace('$', '') if values[3].startswith('$') else values[3]
            precio_venta = values[4].replace('$', '') if values[4].startswith('$') else values[4]
            self.precio_compra_var.set(precio_compra)
            self.precio_venta_var.set(precio_venta)
            self.calculate_margin()
            self.form_status_label.config(text=f"Modo: Editando producto ID {self.selected_product_id}", foreground="orange")

    def on_double_click(self, event):
        """Permite editar con doble clic en un elemento del treeview"""
        self.edit_selected()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_term = self.search_var.get().strip()
        productos = ProductoControlador.listar_productos(search_term)
        
        if productos:
            for i, producto in enumerate(productos):
                # Calcular margen para cada producto
                precio_compra = float(producto[3])
                precio_venta = float(producto[4])
                margen_absoluto = precio_venta - precio_compra
                margen_porcentaje = (margen_absoluto / precio_compra * 100) if precio_compra > 0 else 0
                
                # Formatear valores para mostrar
                formatted_product = [
                    producto[0],  # ID
                    producto[1],  # Página
                    producto[2],  # Código
                    f"${precio_compra:.2f}",
                    f"${precio_venta:.2f}",
                    f"${margen_absoluto:.2f} ({margen_porcentaje:.1f}%)"
                ]
                
                # Determinar tag basado en margen y fila
                base_tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                margin_tag = 'high_margin' if margen_porcentaje > 20 else 'low_margin' if margen_porcentaje < 10 else base_tag
                
                self.tree.insert("", "end", values=formatted_product, tags=(margin_tag,))
            
            # Actualizar estadísticas
            self.stats_label.config(text=f"Total: {len(productos)} productos")
        else:
            self.stats_label.config(text="Total: 0 productos")

    def clear_search(self):
        self.search_var.set("")
        self.refresh()

    def new(self):
        """Prepara el formulario para crear un nuevo producto"""
        self.selected_product_id = None
        self.pagina_var.set("")
        self.codigo_var.set("")
        self.precio_compra_var.set("")
        self.precio_venta_var.set("")
        self.tree.selection_remove(self.tree.selection())
        self.calculate_margin()
        self.form_status_label.config(text="Modo: Nuevo producto", foreground="blue")
        # Enfocar el campo de página
        self.focus_set()

    def cancel_edit(self):
        """Cancela la edición y vuelve al modo de creación"""
        self.new()

    def save(self):
        pagina = self.pagina_var.get().strip()
        codigo = self.codigo_var.get().strip()
        precio_compra = self.precio_compra_var.get().strip()
        precio_venta = self.precio_venta_var.get().strip()
        
        # Validaciones mejoradas
        if not all([pagina, codigo, precio_compra, precio_venta]):
            messagebox.showwarning("Validación", "Todos los campos son requeridos")
            return
        
        if len(codigo) < 2:
            messagebox.showwarning("Validación", "El código debe tener al menos 2 caracteres")
            return
        
        try:
            precio_compra_float = float(precio_compra)
            precio_venta_float = float(precio_venta)
            
            if precio_compra_float <= 0 or precio_venta_float <= 0:
                messagebox.showwarning("Validación", "Los precios deben ser mayores a cero")
                return
            
            if precio_venta_float <= precio_compra_float:
                if not messagebox.askyesno("Advertencia", 
                    "El precio de venta es menor o igual al precio de compra.\n"
                    "Esto resultará en pérdidas. ¿Desea continuar?"):
                    return
            
            if self.selected_product_id:
                # Modo edición
                success, message = ProductoControlador.actualizar_producto(
                    self.selected_product_id, codigo, precio_compra, precio_venta, pagina
                )
                action = "actualizado"
            else:
                # Modo nuevo
                success, message = ProductoControlador.registrar_producto(codigo, precio_compra, precio_venta, pagina)
                action = "registrado"
            
            if success:
                messagebox.showinfo("Éxito", f"Producto {action} exitosamente")
                self.new()
                self.refresh()
                if self.refresh_purchases_cb:
                    self.refresh_purchases_cb()
            else:
                messagebox.showerror("Error", f"Error al {action.replace('ado', 'ar')} producto: {message}")
                
        except ValueError:
            messagebox.showerror("Error", "Los precios deben ser números válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def edit_selected(self):
        """Carga el producto seleccionado para editar"""
        if not self.selected_product_id:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un producto para editar")
            return
        
        # Los datos ya están cargados en el formulario por on_select
        # Enfocar el campo de código para facilitar la edición
        self.focus_set()

    def delete_selected(self):
        """Elimina el producto seleccionado"""
        if not self.selected_product_id:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un producto para eliminar")
            return
        
        selected_item = self.tree.focus()
        values = self.tree.item(selected_item, 'values')
        product_code = values[2]  # Código del producto
        product_page = values[1]  # Página del producto
        
        confirm_msg = f"¿Está seguro de que desea eliminar el producto?\n\n"
        confirm_msg += f"Código: {product_code}\n"
        confirm_msg += f"Página: {product_page}\n\n"
        confirm_msg += "Esta acción no se puede deshacer."
        
        if messagebox.askyesno("Confirmar eliminación", confirm_msg):
            success, message = ProductoControlador.eliminar_producto(self.selected_product_id)
            
            if success:
                messagebox.showinfo("Éxito", "Producto eliminado exitosamente")
                self.new()
                self.refresh()
                if self.refresh_purchases_cb:
                    self.refresh_purchases_cb()
            else:
                messagebox.showerror("Error", f"Error al eliminar producto: {message}")

    def focus_set(self):
        """Enfoca el primer campo del formulario"""
        # Encuentra y enfoca el primer campo de entrada (página)
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.LabelFrame) and "Información del Producto" in str(child.cget("text")):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ttk.Frame):
                                for entry in grandchild.winfo_children():
                                    if isinstance(entry, ttk.Entry):
                                        entry.focus_set()
                                        return

    def delete_all_productos(self):
        """Elimina todos los productos de la base de datos"""
        confirm_msg = "⚠️ ADVERTENCIA ⚠️\n\n"
        confirm_msg += "Esta acción eliminará TODOS los productos de la base de datos.\n"
        confirm_msg += "También se eliminarán todos los pedidos, ventas y detalles relacionados.\n\n"
        confirm_msg += "Esta acción NO se puede deshacer.\n\n"
        confirm_msg += "¿Está seguro de que desea continuar?"
        
        if messagebox.askyesno("Confirmar eliminación masiva", confirm_msg):
            # Doble confirmación
            if messagebox.askyesno("Confirmación final", "¿Realmente desea eliminar TODOS los productos?\n\nEsta es su última oportunidad para cancelar."):
                try:
                    success = ProductoControlador.eliminar_todos()
                    if success:
                        messagebox.showinfo("Éxito", "Todos los productos han sido eliminados exitosamente")
                        self.new()
                        self.refresh()
                        if self.refresh_purchases_cb:
                            self.refresh_purchases_cb()
                    else:
                        messagebox.showerror("Error", "No se pudieron eliminar todos los productos")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar productos: {str(e)}")