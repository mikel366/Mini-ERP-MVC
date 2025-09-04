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
        # Frame de búsqueda
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=6, pady=6)
        
        ttk.Label(search_frame, text="Buscar:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=6)
        search_entry.bind('<KeyRelease>', lambda e: self.refresh())
        
        ttk.Button(search_frame, text="Limpiar", command=self.clear_search).pack(side="left", padx=4)

        # Frame de formulario
        form = ttk.LabelFrame(self, text="Gestión de Productos")
        form.pack(fill="x", padx=6, pady=6)
        
        # Página
        ttk.Label(form, text="Página:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.pagina_var = tk.StringVar()
        pagina_entry = ttk.Entry(form, textvariable=self.pagina_var, width=10)
        pagina_entry.grid(row=0, column=1, padx=6, pady=6)
        
        # Código
        ttk.Label(form, text="Código:").grid(row=0, column=2, padx=6, pady=6, sticky="e")
        self.codigo_var = tk.StringVar()
        codigo_entry = ttk.Entry(form, textvariable=self.codigo_var, width=20)
        codigo_entry.grid(row=0, column=3, padx=6, pady=6)
        
        # Precio
        ttk.Label(form, text="Precio:").grid(row=0, column=4, padx=6, pady=6, sticky="e")
        self.precio_var = tk.StringVar()
        precio_entry = ttk.Entry(form, textvariable=self.precio_var, width=10)
        precio_entry.grid(row=0, column=5, padx=6, pady=6)
        
        # Botones
        button_frame = ttk.Frame(form)
        button_frame.grid(row=0, column=6, padx=6, pady=6)
        
        ttk.Button(button_frame, text="Guardar", command=self.save).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Editar", command=self.edit_selected).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Eliminar", command=self.delete_selected).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Nuevo", command=self.new).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Cancelar", command=self.cancel_edit).pack(side="left", padx=2)

        # Treeview para listar productos
        cols = ("id", "pagina", "codigo", "precio")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        
        # Configurar columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("pagina", text="Página")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("precio", text="Precio")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("pagina", width=80, anchor="center")
        self.tree.column("codigo", width=150, anchor="w")
        self.tree.column("precio", width=100, anchor="e")
        
        # Scrollbar para el treeview
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        scrollbar.pack(side="right", fill="y", padx=(0, 6), pady=6)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.bind('<Double-1>', self.on_double_click)  # Doble clic para editar

    def on_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.selected_product_id = values[0]
            self.pagina_var.set(values[1])
            self.codigo_var.set(values[2])
            self.precio_var.set(values[3])

    def on_double_click(self, event):
        """Permite editar con doble clic en un elemento del treeview"""
        self.edit_selected()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_term = self.search_var.get().strip()
        productos = ProductoControlador.listar_productos(search_term)
        
        for producto in productos:
            # Formatear el precio para mostrar
            formatted_product = list(producto)
            formatted_product[3] = f"{formatted_product[3]:.2f}"  # Formatear precio con 2 decimales
            self.tree.insert("", "end", values=formatted_product)

    def clear_search(self):
        self.search_var.set("")
        self.refresh()

    def new(self):
        """Prepara el formulario para crear un nuevo producto"""
        self.selected_product_id = None
        self.pagina_var.set("")
        self.codigo_var.set("")
        self.precio_var.set("")
        self.tree.selection_remove(self.tree.selection())
        # Enfocar el campo de página
        self.focus_set()

    def cancel_edit(self):
        """Cancela la edición y vuelve al modo de creación"""
        self.new()

    def save(self):
        pagina = self.pagina_var.get().strip()
        codigo = self.codigo_var.get().strip()
        precio = self.precio_var.get().strip()
        
        if not all([pagina, codigo, precio]):
            messagebox.showwarning("Validación", "Todos los campos son requeridos")
            return
        
        try:
            if self.selected_product_id:
                # Modo edición
                success, message = ProductoControlador.actualizar_producto(
                    self.selected_product_id, codigo, precio, pagina
                )
                action = "actualizado"
            else:
                # Modo nuevo
                success, message = ProductoControlador.registrar_producto(codigo, precio, pagina)
                action = "creado"
            
            if success:
                messagebox.showinfo("Éxito", message)
                self.new()
                self.refresh()
                if self.refresh_purchases_cb:
                    self.refresh_purchases_cb()
            else:
                messagebox.showerror("Error", message)
                
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
        product_name = values[2]  # Código del producto
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar el producto '{product_name}'?"):
            success, message = ProductoControlador.eliminar_producto(self.selected_product_id)
            
            if success:
                messagebox.showinfo("Éxito", message)
                self.new()
                self.refresh()
                if self.refresh_purchases_cb:
                    self.refresh_purchases_cb()
            else:
                messagebox.showerror("Error", message)

    def focus_set(self):
        """Enfoca el primer campo del formulario"""
        # Encuentra y enfoca el primer campo de entrada
        for child in self.winfo_children():
            if isinstance(child, ttk.LabelFrame):
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, ttk.Entry):
                        grandchild.focus_set()
                        return