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
        form = ttk.LabelFrame(self, text="Gestión de Clientes")
        form.pack(fill="x", padx=6, pady=6)
        
        ttk.Label(form, text="Nombre:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.nombre_var = tk.StringVar()
        nombre_entry = ttk.Entry(form, textvariable=self.nombre_var, width=40)
        nombre_entry.grid(row=0, column=1, padx=6, pady=6)
        
        button_frame = ttk.Frame(form)
        button_frame.grid(row=0, column=2, padx=6, pady=6)
        
        ttk.Button(button_frame, text="Guardar", command=self.save).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Editar", command=self.edit).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Eliminar", command=self.delete).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Nuevo", command=self.new).pack(side="left", padx=2)

        # Treeview para listar clientes
        cols = ("id", "nombre")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        
        for col in cols:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100 if col == "id" else 200)
        
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def on_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.selected_id = values[0]
            self.nombre_var.set(values[1])

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_term = self.search_var.get()
        clientes = ClientesControlador.listar_clientes(search_term)
        
        for cliente in clientes:
            self.tree.insert("", "end", values=cliente)

    def clear_search(self):
        self.search_var.set("")
        self.refresh()

    def new(self):
        self.selected_id = None
        self.nombre_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def save(self):
        nombre = self.nombre_var.get().strip()
        
        if not nombre:
            messagebox.showwarning("Validación", "Nombre requerido")
            return
        
        if self.selected_id:
            # Modo edición
            success, message = ClientesControlador.editar_cliente(self.selected_id, nombre)
        else:
            # Modo nuevo
            success, message = ClientesControlador.registrar_cliente(nombre)
        
        if success:
            messagebox.showinfo("Éxito", message)
            self.new()
            self.refresh()
            if self.refresh_purchases_cb:
                self.refresh_purchases_cb()
        else:
            messagebox.showerror("Error", message)

    def edit(self):
        if not self.selected_id:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un cliente para editar")
            return
        
        # Los datos ya están cargados en el formulario por on_select
        # Solo necesitamos enfocar el campo de nombre
        self.focus_set()

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un cliente para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este cliente?"):
            success, message = ClientesControlador.eliminar_cliente(self.selected_id)
            
            if success:
                messagebox.showinfo("Éxito", message)
                self.new()
                self.refresh()
                if self.refresh_purchases_cb:
                    self.refresh_purchases_cb()
            else:
                messagebox.showerror("Error", message)