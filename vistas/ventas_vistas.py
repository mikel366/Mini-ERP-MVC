# app/vistas/ventas_vistas.py
import tkinter as tk
from tkinter import ttk

class VentasTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.build_ui()
        
    def build_ui(self):
        label = ttk.Label(self, text="Panel de Ventas - Aquí se mostrarán las ventas completadas")
        label.pack(pady=20)
        
        # Treeview para mostrar ventas
        cols = ("id", "cliente", "monto", "ganancia", "fecha")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        
        for col in cols:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    def refresh(self):
        """Método para actualizar la lista de ventas"""
        # Aquí implementarás la lógica para cargar las ventas
        print("Actualizando lista de ventas...")