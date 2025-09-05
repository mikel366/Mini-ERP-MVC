import tkinter as tk
from tkinter import ttk, messagebox
from controladores import ClientesControlador

class ClientesTab(ttk.Frame):
    def __init__(self, master, refresh_purchases_cb=None):
        super().__init__(master)
        self.refresh_purchases_cb = refresh_purchases_cb
        self.selected_id = None
        self.build_ui()
        self.refresh()

    def build_ui(self):
        # Frame principal con padding mejorado
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header con título y estadísticas
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        
        title_label = ttk.Label(header_frame, text="Gestión de Clientes", font=("Arial", 14, "bold"))
        title_label.pack(side="left")
        
        self.stats_label = ttk.Label(header_frame, text="Total: 0 clientes", font=("Arial", 10), foreground="gray")
        self.stats_label.pack(side="right")
        
        # Frame de búsqueda mejorado
        search_frame = ttk.LabelFrame(main_frame, text="Búsqueda y Filtros", padding=10)
        search_frame.pack(fill="x", pady=(0, 10))
        
        search_grid = ttk.Frame(search_frame)
        search_grid.pack(fill="x")
        
        ttk.Label(search_grid, text="Buscar cliente:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_grid, textvariable=self.search_var, width=40, font=("Arial", 10))
        search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        search_entry.bind('<KeyRelease>', lambda e: self.refresh())
        
        ttk.Button(search_grid, text=" Buscar", command=self.refresh).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(search_grid, text=" Limpiar", command=self.clear_search).grid(row=0, column=3)
        
        search_grid.columnconfigure(1, weight=1)

        # Frame de formulario mejorado
        form_frame = ttk.LabelFrame(main_frame, text="Información del Cliente", padding=15)
        form_frame.pack(fill="x", pady=(0, 10))
        
        # Grid para el formulario
        form_grid = ttk.Frame(form_frame)
        form_grid.pack(fill="x")
        
        # Campo nombre
        ttk.Label(form_grid, text="Nombre completo:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="e", padx=(0, 10), pady=5)
        self.nombre_var = tk.StringVar()
        nombre_entry = ttk.Entry(form_grid, textvariable=self.nombre_var, width=50, font=("Arial", 10))
        nombre_entry.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Estado del formulario
        self.form_status_label = ttk.Label(form_grid, text="Modo: Nuevo cliente", font=("Arial", 9), foreground="blue")
        self.form_status_label.grid(row=1, column=1, sticky="w", pady=(5, 0))
        
        form_grid.columnconfigure(1, weight=1)
        
        # Frame de botones mejorado
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x", pady=(15, 0))
        
        # Botones principales
        btn_style = {"width": 12, "padding": 5}
        ttk.Button(button_frame, text="Guardar", command=self.save, **btn_style).pack(side="left", padx=(0, 5))
        ttk.Button(button_frame, text="Editar", command=self.edit, **btn_style).pack(side="left", padx=(0, 5))
        ttk.Button(button_frame, text="Eliminar", command=self.delete, **btn_style).pack(side="left", padx=(0, 5))
        ttk.Button(button_frame, text="Nuevo", command=self.new, **btn_style).pack(side="left", padx=(0, 10))
        
        # Botones de la derecha
        ttk.Button(button_frame, text="🗑️ Eliminar Todos", command=self.delete_all_clientes, 
                  style="Accent.TButton", width=15).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="Actualizar", command=self.refresh, width=12).pack(side="right")

        # Frame de lista mejorado
        list_frame = ttk.LabelFrame(main_frame, text="Lista de Clientes", padding=10)
        list_frame.pack(fill="both", expand=True)
        
        # Treeview con scrollbar
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill="both", expand=True)
        
        cols = ("id", "nombre")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=12)
        
        # Configurar columnas
        self.tree.heading("id", text="ID", anchor="center")
        self.tree.heading("nombre", text="Nombre del Cliente", anchor="w")
        
        self.tree.column("id", width=80, anchor="center", minwidth=60)
        self.tree.column("nombre", width=400, anchor="w", minwidth=200)
        
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

    def on_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.selected_id = values[0]
            self.nombre_var.set(values[1])
            self.form_status_label.config(text=f"Modo: Editando cliente ID {self.selected_id}", foreground="orange")

    def on_double_click(self, event):
        """Permite editar con doble clic"""
        if self.selected_id:
            self.edit()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_term = self.search_var.get()
        clientes = ClientesControlador.listar_clientes(search_term)
        
        if clientes:
            for i, cliente in enumerate(clientes):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=cliente, tags=(tag,))
            
            # Actualizar estadísticas
            self.stats_label.config(text=f"Total: {len(clientes)} clientes")
        else:
            self.stats_label.config(text="Total: 0 clientes")

    def clear_search(self):
        self.search_var.set("")
        self.refresh()

    def new(self):
        self.selected_id = None
        self.nombre_var.set("")
        self.tree.selection_remove(self.tree.selection())
        self.form_status_label.config(text="Modo: Nuevo cliente", foreground="blue")

    def save(self):
        nombre = self.nombre_var.get().strip()
        
        if not nombre:
            messagebox.showwarning("Validación", "El nombre del cliente es requerido")
            return
        
        if len(nombre) < 2:
            messagebox.showwarning("Validación", "El nombre debe tener al menos 2 caracteres")
            return
        
        if self.selected_id:
            # Modo edición
            success, message = ClientesControlador.editar_cliente(self.selected_id, nombre)
            action = "actualizado"
        else:
            # Modo nuevo
            success, message = ClientesControlador.registrar_cliente(nombre)
            action = "registrado"
        
        if success:
            messagebox.showinfo("Éxito", f"Cliente {action} exitosamente")
            self.new()
            self.refresh()
            if self.refresh_purchases_cb:
                self.refresh_purchases_cb()
        else:
            messagebox.showerror("Error", f"Error al {action.replace('ado', 'ar')} cliente: {message}")

    def edit(self):
        if not self.selected_id:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un cliente para editar")
            return
        
        # Los datos ya están cargados en el formulario por on_select
        # Enfocar el campo de nombre para facilitar la edición
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.LabelFrame) and "Información del Cliente" in str(child.cget("text")):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ttk.Frame):
                                for entry in grandchild.winfo_children():
                                    if isinstance(entry, ttk.Entry):
                                        entry.focus_set()
                                        entry.select_range(0, tk.END)
                                        return

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un cliente para eliminar")
            return
        
        try:
            cliente_nombre = self.nombre_var.get()
            confirm_msg = f"¿Está seguro de que desea eliminar el cliente '{cliente_nombre}'?\n\nEsta acción no se puede deshacer."
            
            if messagebox.askyesno("Confirmar eliminación", confirm_msg):
                success, message = ClientesControlador.eliminar_cliente(self.selected_id)
                
                if success:
                    messagebox.showinfo("Éxito", f"Cliente '{cliente_nombre}' eliminado exitosamente")
                    self.new()
                    self.refresh()
                    if self.refresh_purchases_cb:
                        self.refresh_purchases_cb()
                else:
                    messagebox.showerror("Error", f"Error al eliminar cliente: {message}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")

    def delete_all_clientes(self):
        """Elimina todos los clientes de la base de datos"""
        confirm_msg = "⚠️ ADVERTENCIA ⚠️\n\n"
        confirm_msg += "Esta acción eliminará TODOS los clientes de la base de datos.\n"
        confirm_msg += "También se eliminarán todos los pedidos, ventas y detalles relacionados.\n\n"
        confirm_msg += "Esta acción NO se puede deshacer.\n\n"
        confirm_msg += "¿Está seguro de que desea continuar?"
        
        if messagebox.askyesno("Confirmar eliminación masiva", confirm_msg):
            # Doble confirmación
            if messagebox.askyesno("Confirmación final", "¿Realmente desea eliminar TODOS los clientes?\n\nEsta es su última oportunidad para cancelar."):
                try:
                    success = ClientesControlador.eliminar_todos()
                    if success:
                        messagebox.showinfo("Éxito", "Todos los clientes han sido eliminados exitosamente")
                        self.new()
                        self.refresh()
                        if self.refresh_purchases_cb:
                            self.refresh_purchases_cb()
                    else:
                        messagebox.showerror("Error", "No se pudieron eliminar todos los clientes")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar clientes: {str(e)}")