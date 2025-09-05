# app/main.py
from configuraciones.inicializacion import inicializar_bd
from vistas import ClientesTab, ProductosTab, PedidosTab, VentasTab
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

def main():
    # Inicializar base de datos
    try:
        inicializar_bd()
        print("Base de datos inicializada correctamente")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return

    # Crear ventana principal
    root = tk.Tk()
    root.title("Mini ERP MVC")
    root.geometry("")
    root.minsize(900, 600)
    
    def restart_app():
        """Reinicia la aplicación"""
        if messagebox.askyesno("Reiniciar Aplicación", 
                              "¿Está seguro de que desea reiniciar la aplicación?\n\nTodos los datos se mantendrán guardados."):
            root.destroy()
            # Reiniciar el script de Python
            os.execv(sys.executable, ['python'] + sys.argv)
    
    # Frame superior para botones de control
    control_frame = ttk.Frame(root)
    control_frame.pack(fill="x", padx=5, pady=(5, 0))
    
    # Botón de reinicio
    ttk.Button(control_frame, text="🔄 Reiniciar App", 
              command=restart_app, 
              style="Accent.TButton").pack(side="right", padx=(0, 5))

    # Crear notebook (pestañas)
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=5, pady=5)

    
    # Crear callbacks para refrescar entre pestañas
    def refresh_pedidos():
        pedidos_tab.refresh()
        pedidos_tab.cargar_clientes()
        pedidos_tab.cargar_productos()
    
    def refresh_ventas():
        ventas_tab.refresh()
        ventas_tab.cargar_clientes()
        ventas_tab.cargar_productos()
    
    def refresh_dropdowns():
        """Refresca los dropdowns de clientes y productos en pedidos y ventas"""
        try:
            pedidos_tab.cargar_clientes()
            pedidos_tab.cargar_productos()
            ventas_tab.cargar_clientes()
            ventas_tab.cargar_productos()
        except:
            pass  # En caso de que las pestañas no estén inicializadas aún
    
    clients_tab = ClientesTab(nb, refresh_purchases_cb=refresh_dropdowns)
    productos_tab = ProductosTab(nb, refresh_purchases_cb=refresh_dropdowns)
    
    pedidos_tab = PedidosTab(nb, refresh_purchases_cb=refresh_ventas)
    ventas_tab = VentasTab(nb, refresh_purchases_cb=refresh_pedidos)

    # Añadir pestañas al notebook
    nb.add(clients_tab, text="👥 Clientes")
    nb.add(productos_tab, text="📦 Productos")
    nb.add(pedidos_tab, text="📋 Pedidos")
    nb.add(ventas_tab, text="💰 Ventas")

    # Centrar ventana en la pantalla
    root.eval('tk::PlaceWindow . center')

    # Iniciar bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()