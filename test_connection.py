import tkinter as tk
from tkinter import messagebox
from testlink import TestlinkAPIClient
from config import reader_config as cfg

def mostrar_proyectos():
    try:
        tlc = TestlinkAPIClient(cfg.TESTLINK_SERVER_URL, cfg.TESTLINK_DEV_KEY)
        projects = tlc.getProjects()

        print("Proyectos obtenidos:", projects) 

        if not projects or not isinstance(projects, list):
            messagebox.showinfo("Proyectos", "No se encontraron proyectos o el formato es incorrecto.")
            return

        mensaje = "✅ Conexión exitosa. Proyectos disponibles:\n\n"
        for proyecto in projects:
            nombre = proyecto.get("name", "Sin nombre")
            id_ = proyecto.get("id", proyecto.get("id_proyecto", "Desconocido"))
            mensaje += f"- {nombre} (ID: {id_})\n"

        messagebox.showinfo("Proyectos TestLink", mensaje)

    except Exception as e:
        messagebox.showerror("Error de conexión", f"❌ Error conectando con TestLink:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  
    mostrar_proyectos()
