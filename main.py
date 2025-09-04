# app/main.py
import modelos
from vistas import ClientesTab, ProductosTab, VentasTab
import tkinter as tk
from tkinter import ttk

def main():
    # Inicializar base de datos
    try:
        modelos.inicializar_bd()
        print("Base de datos inicializada correctamente")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return

    # Crear ventana principal
    root = tk.Tk()
    root.title("Mini ERP MVC")
    root.geometry("1000x700")
    root.minsize(900, 600)

    # Crear notebook (pestañas)
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=5, pady=5)

    # Crear pestañas - el orden es importante para los callbacks
    sales_tab = VentasTab(nb)
    # clients_tab = ClientesTab(nb, refresh_purchases_cb=purchases_tab.refresh)
    # productos_tab = ProductosTab(nb, refresh_purchases_cb=purchases_tab.refresh)
    
    clients_tab = ClientesTab(nb)
    productos_tab = ProductosTab(nb)

    # Añadir pestañas al notebook
    nb.add(clients_tab, text="👥 Clientes")
    nb.add(productos_tab, text="📦 Productos")
    nb.add(sales_tab, text="💰 Ventas")

    # Centrar ventana en la pantalla
    root.eval('tk::PlaceWindow . center')

    # Iniciar bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()