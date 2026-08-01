import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import contextlib
import io

# Importamos la lógica y datos desde main.py
from main import (
    RedVuelos, 
    CATALOGO_CIUDADES, 
    formato_km, 
    formato_duracion, 
    VELOCIDAD_CRUCERO_KMH, 
    TIEMPO_TIERRA_HORAS,
    plegar_acentos
)

# ----------------- COLORES DEL TEMA -----------------
BG_PRINCIPAL = "#0f172a"      # Slate 900
BG_PANELES = "#1e293b"        # Slate 800
COLOR_TEXTO = "#f8fafc"       # Slate 50
COLOR_ACCENTO = "#3b82f6"     # Blue 500
COLOR_ACCENTO_HOVER = "#2563eb" # Blue 600
BG_CONSOLA = "#020617"        # Slate 950
TEXTO_CONSOLA = "#e2e8f0"     # Slate 200
COLOR_SUBTITULO = "#94a3b8"   # Slate 400
# ----------------------------------------------------

class StdoutRedirector(io.StringIO):
    """
    Redirige la salida estándar (print) hacia un widget Text de Tkinter.
    """
    def __init__(self, text_widget):
        self.text_widget = text_widget
        super().__init__()

    def write(self, string):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')
        
    def flush(self):
        pass


class CustomDialog(tk.Toplevel):
    """
    Diálogo personalizado moderno para reemplazar simpledialog.askstring.
    Muestra un título descriptivo arriba de la caja de texto.
    """
    def __init__(self, parent, title, prompt):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG_PANELES)
        self.geometry("380x170")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Centrar ventana respecto al padre
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        self.result = None
        
        # Título descriptivo de la acción
        lbl_title = tk.Label(self, text=title, bg=BG_PANELES, fg=COLOR_ACCENTO, font=("Segoe UI", 12, "bold"))
        lbl_title.pack(pady=(15, 2))
        
        # Prompt (ej: "Ingrese la ciudad de origen:")
        lbl = tk.Label(self, text=prompt, bg=BG_PANELES, fg=COLOR_TEXTO, font=("Segoe UI", 10))
        lbl.pack(pady=(2, 8))
        
        self.entry = tk.Entry(self, font=("Segoe UI", 11), bg=BG_PRINCIPAL, fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO, relief=tk.FLAT)
        self.entry.pack(fill=tk.X, padx=20, pady=(0, 12), ipady=5)
        self.entry.focus_set()
        
        btn_frame = tk.Frame(self, bg=BG_PANELES)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        btn_ok = ttk.Button(btn_frame, text="Aceptar", command=self.on_ok, style="Accent.TButton")
        btn_ok.pack(side=tk.RIGHT, padx=(5, 0))
        
        btn_cancel = ttk.Button(btn_frame, text="Cancelar", command=self.on_cancel, style="Custom.TButton")
        btn_cancel.pack(side=tk.RIGHT)
        
        self.bind("<Return>", lambda e: self.on_ok())
        self.bind("<Escape>", lambda e: self.on_cancel())
        
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.wait_window(self)

    def on_ok(self):
        self.result = self.entry.get().strip()
        self.destroy()
        
    def on_cancel(self):
        self.result = None
        self.destroy()


class CitySelectionDialog(tk.Toplevel):
    """
    Diálogo para seleccionar una ciudad ya registrada en el sistema.
    Muestra un título descriptivo y una lista de ciudades registradas.
    """
    def __init__(self, parent, title, prompt, ciudades):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG_PANELES)
        self.geometry("380x450")
        self.resizable(False, True)
        self.transient(parent)
        self.grab_set()
        
        # Centrar ventana respecto al padre
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        self.result = None
        self.ciudades = sorted(ciudades)
        
        # Título descriptivo
        lbl_title = tk.Label(self, text=title, bg=BG_PANELES, fg=COLOR_ACCENTO, font=("Segoe UI", 12, "bold"))
        lbl_title.pack(pady=(15, 2))
        
        # Prompt descriptivo
        lbl = tk.Label(self, text=prompt, bg=BG_PANELES, fg=COLOR_TEXTO, font=("Segoe UI", 10))
        lbl.pack(pady=(2, 8))
        
        # Indicación
        lbl_hint = tk.Label(self, text="Seleccione una ciudad de la lista o haga doble clic:", bg=BG_PANELES, fg=COLOR_SUBTITULO, font=("Segoe UI", 9))
        lbl_hint.pack(pady=(0, 5))
        
        # Listbox con ciudades registradas
        list_frame = tk.Frame(self, bg=BG_PANELES)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 10),
            bg=BG_PRINCIPAL,
            fg=COLOR_TEXTO,
            selectbackground=COLOR_ACCENTO,
            selectforeground="#ffffff",
            relief=tk.FLAT,
            activestyle='none',
            yscrollcommand=scrollbar.set
        )
        self.listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        for ciudad in self.ciudades:
            self.listbox.insert(tk.END, ciudad)
        
        if not self.ciudades:
            self.listbox.insert(tk.END, "(No hay ciudades registradas)")
        
        self.listbox.bind('<Double-1>', self.on_select)
        
        # Botones
        btn_frame = tk.Frame(self, bg=BG_PANELES)
        btn_frame.pack(fill=tk.X, padx=20, pady=15)
        
        btn_seleccionar = ttk.Button(btn_frame, text="Seleccionar", command=self.on_select, style="Accent.TButton")
        btn_seleccionar.pack(side=tk.RIGHT, padx=(5, 0))
        
        btn_cancelar = ttk.Button(btn_frame, text="Cancelar", command=self.on_cancel, style="Custom.TButton")
        btn_cancelar.pack(side=tk.RIGHT)
        
        self.bind("<Return>", lambda e: self.on_select())
        self.bind("<Escape>", lambda e: self.on_cancel())
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.wait_window(self)
    
    def on_select(self, event=None):
        if not self.ciudades:
            messagebox.showwarning("Sin ciudades", "No hay ciudades registradas en el sistema.", parent=self)
            return
        seleccion = self.listbox.curselection()
        if seleccion:
            self.result = self.ciudades[seleccion[0]]
            self.destroy()
        else:
            messagebox.showinfo("Selección", "Seleccione una ciudad de la lista.", parent=self)
    
    def on_cancel(self):
        self.result = None
        self.destroy()


class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Rutas Aéreas de México - GUI")
        self.geometry("1000x700")
        self.configure(bg=BG_PRINCIPAL)
        
        # Configuración de estilos ttk
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Estilo para botones estándar
        self.style.configure("Custom.TButton", 
                             font=("Segoe UI", 10),
                             background=BG_PANELES, 
                             foreground=COLOR_TEXTO,
                             bordercolor=BG_PRINCIPAL,
                             lightcolor=BG_PANELES,
                             darkcolor=BG_PANELES,
                             padding=8)
        self.style.map("Custom.TButton",
                       background=[('active', '#334155')],
                       foreground=[('active', COLOR_TEXTO)])
        
        # Estilo para botones acentuados
        self.style.configure("Accent.TButton", 
                             font=("Segoe UI", 10, "bold"),
                             background=COLOR_ACCENTO, 
                             foreground="#ffffff",
                             bordercolor=BG_PRINCIPAL,
                             lightcolor=COLOR_ACCENTO,
                             darkcolor=COLOR_ACCENTO,
                             padding=8)
        self.style.map("Accent.TButton",
                       background=[('active', COLOR_ACCENTO_HOVER)],
                       foreground=[('active', "#ffffff")])
        
        self.red = RedVuelos()
        self.create_widgets()
        
    def create_widgets(self):
        # Frame de botones (Izquierda)
        btn_frame = tk.Frame(self, bg=BG_PANELES, width=280)
        btn_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 5), pady=10)
        btn_frame.pack_propagate(False) # Mantener ancho fijo
        
        lbl_titulo = tk.Label(btn_frame, text="MENÚ PRINCIPAL", font=("Segoe UI", 14, "bold"), bg=BG_PANELES, fg=COLOR_ACCENTO)
        lbl_titulo.pack(pady=(20, 20))
        
        botones = [
            ("1. Agregar Ciudad", self.agregar_ciudad),
            ("2. Agregar Ruta de Vuelo", self.agregar_ruta),
            ("3. Eliminar Ciudad", self.eliminar_ciudad),
            ("4. Eliminar Ruta de Vuelo", self.eliminar_ruta),
            ("5. Mostrar Mapa de Rutas", self.mostrar_mapa),
            ("6. Ruta Más Corta (Dijkstra)", self.ruta_mas_corta),
            ("7. Distancia y Duración", self.distancia_y_duracion),
            ("8. Listar Ciudades y Rutas", self.listar_rutas),
            ("9. Ver Catálogo y Latitud", self.ver_ciudades_disponibles),
            ("10. Salir", self.salir)
        ]
        
        for texto, comando in botones:
            estilo = "Accent.TButton" if texto.startswith("10.") else "Custom.TButton"
            btn = ttk.Button(btn_frame, text=texto, command=comando, style=estilo)
            btn.pack(fill=tk.X, padx=20, pady=5)
            
        # Frame de salida (Derecha)
        out_frame = tk.Frame(self, bg=BG_PRINCIPAL)
        out_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)
        
        header_out = tk.Frame(out_frame, bg=BG_PRINCIPAL)
        header_out.pack(fill=tk.X, pady=(5, 5))
        
        tk.Label(header_out, text="Consola de Salida", font=("Segoe UI", 12, "bold"), bg=BG_PRINCIPAL, fg=COLOR_TEXTO).pack(side=tk.LEFT)
        btn_clear = ttk.Button(header_out, text="Limpiar", command=self.limpiar_consola, style="Custom.TButton")
        btn_clear.pack(side=tk.RIGHT)
        
        self.text_out = scrolledtext.ScrolledText(
            out_frame, 
            state='disabled', 
            font=("Consolas", 11), 
            bg=BG_CONSOLA, 
            fg=TEXTO_CONSOLA,
            insertbackground=TEXTO_CONSOLA,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.text_out.pack(fill=tk.BOTH, expand=True)

    def ejecutar_con_salida(self, func, *args, **kwargs):
        """Ejecuta una función redirigiendo sys.stdout a la consola gráfica."""
        redirector = StdoutRedirector(self.text_out)
        with contextlib.redirect_stdout(redirector):
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Error inesperado: {e}")

    def limpiar_consola(self):
        """Limpia el texto de la consola gráfica."""
        self.text_out.configure(state='normal')
        self.text_out.delete(1.0, tk.END)
        self.text_out.configure(state='disabled')

    def ask_string(self, title, prompt):
        """Muestra un CustomDialog y devuelve la entrada del usuario."""
        dialog = CustomDialog(self, title, prompt)
        return dialog.result

    def obtener_ciudades_registradas(self):
        """Devuelve la lista de ciudades actualmente registradas en el grafo."""
        return list(self.red.grafo.nodes())

    def seleccionar_ciudad_registrada(self, title, prompt):
        """Muestra un diálogo para seleccionar una ciudad ya registrada."""
        ciudades = self.obtener_ciudades_registradas()
        if not ciudades:
            messagebox.showwarning("Sin ciudades", "No hay ciudades registradas en el sistema.\nPrimero agregue ciudades desde el menú.")
            return None
        dialog = CitySelectionDialog(self, title, prompt, ciudades)
        return dialog.result

    def seleccionar_ciudad_del_catalogo(self):
        """Muestra una ventana personalizada para buscar y seleccionar una ciudad del catálogo."""
        busqueda = self.ask_string("Agregar Ciudad", "Escriba parte del nombre para buscar\n(Deje en blanco para ver todas):")
        if busqueda is None:
            return None
            
        if busqueda.strip():
            clave = plegar_acentos(busqueda.strip())
            resultados = [n for n in CATALOGO_CIUDADES if clave in plegar_acentos(n)]
            if not resultados:
                messagebox.showerror("Error", f"Sin coincidencias para '{busqueda}'. Verifique el nombre.")
                return None
        else:
            resultados = sorted(CATALOGO_CIUDADES)
            
        # Ventana estilizada para mostrar la lista de resultados
        dialogo = tk.Toplevel(self)
        dialogo.title("Agregar Ciudad")
        dialogo.geometry("380x450")
        dialogo.configure(bg=BG_PANELES)
        dialogo.transient(self)
        dialogo.grab_set()
        
        # Centrar
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (380 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (450 // 2)
        dialogo.geometry(f"+{x}+{y}")
        
        ciudad_seleccionada = tk.StringVar()
        
        # Título descriptivo
        tk.Label(dialogo, text="Agregar Ciudad", bg=BG_PANELES, fg=COLOR_ACCENTO, font=("Segoe UI", 12, "bold")).pack(pady=(15, 2))
        tk.Label(dialogo, text="Seleccione la ciudad a agregar:", bg=BG_PANELES, fg=COLOR_TEXTO, font=("Segoe UI", 10)).pack(pady=(2, 5))
        tk.Label(dialogo, text="Doble clic o botón Seleccionar:", bg=BG_PANELES, fg=COLOR_SUBTITULO, font=("Segoe UI", 9)).pack(pady=(0, 5))
        
        listbox = tk.Listbox(
            dialogo, 
            font=("Segoe UI", 10), 
            bg=BG_PRINCIPAL, 
            fg=COLOR_TEXTO,
            selectbackground=COLOR_ACCENTO,
            selectforeground="#ffffff",
            relief=tk.FLAT,
            activestyle='none'
        )
        listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        for n in resultados:
            registrada = " (ya registrada)" if self.red.grafo.has_node(n) else ""
            listbox.insert(tk.END, f"{n}{registrada}")
            
        def on_select(event=None):
            seleccion = listbox.curselection()
            if seleccion:
                idx = seleccion[0]
                nombre = resultados[idx]
                if self.red.grafo.has_node(nombre):
                    messagebox.showerror("Error", f"La ciudad '{nombre}' ya existe en el sistema.")
                else:
                    ciudad_seleccionada.set(nombre)
                    dialogo.destroy()
                    
        listbox.bind('<Double-1>', on_select)
        
        btn_frame = tk.Frame(dialogo, bg=BG_PANELES)
        btn_frame.pack(fill=tk.X, padx=20, pady=15)
        
        btn_seleccionar = ttk.Button(btn_frame, text="Seleccionar", command=on_select, style="Accent.TButton")
        btn_seleccionar.pack(side=tk.RIGHT, padx=(5, 0))
        
        btn_cancelar = ttk.Button(btn_frame, text="Cancelar", command=dialogo.destroy, style="Custom.TButton")
        btn_cancelar.pack(side=tk.RIGHT)
        
        self.wait_window(dialogo)
        
        return ciudad_seleccionada.get() if ciudad_seleccionada.get() else None

    def agregar_ciudad(self):
        nombre = self.seleccionar_ciudad_del_catalogo()
        if nombre:
            print(f"\n--- Agregando ciudad '{nombre}' ---")
            self.ejecutar_con_salida(self.red.agregar_ciudad, nombre)

    def agregar_ruta(self):
        origen = self.seleccionar_ciudad_registrada("Agregar Ruta de Vuelo", "Seleccione la ciudad de ORIGEN:")
        if not origen: return
        destino = self.seleccionar_ciudad_registrada("Agregar Ruta de Vuelo", "Seleccione la ciudad de DESTINO:")
        if not destino: return
        
        if origen == destino:
            messagebox.showerror("Error", "La ciudad de origen y destino no pueden ser la misma.")
            return
        
        print(f"\n--- Agregando ruta de '{origen}' a '{destino}' ---")
        self.ejecutar_con_salida(self.red.agregar_ruta, origen, destino)
        
        redonda = messagebox.askyesno("Vuelo de regreso", "¿Desea agregar también el vuelo de regreso?")
        if redonda:
            print(f"--- Agregando ruta de regreso de '{destino}' a '{origen}' ---")
            self.ejecutar_con_salida(self.red.agregar_ruta, destino, origen)

    def eliminar_ciudad(self):
        ciudad = self.seleccionar_ciudad_registrada("Eliminar Ciudad", "Seleccione la ciudad a eliminar:")
        if ciudad:
            print(f"\n--- Eliminando ciudad '{ciudad}' ---")
            self.ejecutar_con_salida(self.red.eliminar_ciudad, ciudad)

    def eliminar_ruta(self):
        origen = self.seleccionar_ciudad_registrada("Eliminar Ruta de Vuelo", "Seleccione la ciudad de ORIGEN de la ruta:")
        if not origen: return
        destino = self.seleccionar_ciudad_registrada("Eliminar Ruta de Vuelo", "Seleccione la ciudad de DESTINO de la ruta:")
        if not destino: return
        print(f"\n--- Eliminando ruta de '{origen}' a '{destino}' ---")
        self.ejecutar_con_salida(self.red.eliminar_ruta, origen, destino)

    def mostrar_mapa(self):
        print("\n--- Mostrando Mapa de Rutas ---")
        self.ejecutar_con_salida(self.red.mostrar_grafo)

    def ruta_mas_corta(self):
        origen = self.seleccionar_ciudad_registrada("Ruta Más Corta (Dijkstra)", "Seleccione la ciudad de ORIGEN:")
        if not origen: return
        destino = self.seleccionar_ciudad_registrada("Ruta Más Corta (Dijkstra)", "Seleccione la ciudad de DESTINO:")
        if not destino: return
        
        if origen == destino:
            messagebox.showerror("Error", "La ciudad de origen y destino no pueden ser la misma.")
            return
        
        criterio = messagebox.askyesno("Criterio de búsqueda", "¿Desea minimizar la distancia total en kilómetros?\n(Sí = Minimizar Distancia, No = Minimizar Escalas)")
        por_km = criterio
        
        print(f"\n--- Calculando ruta más corta de '{origen}' a '{destino}' ---")
        
        def _calc():
            camino = self.red.ruta_mas_corta(origen, destino, por_km=por_km)
            if camino is None:
                return
            
            km_total = sum(self.red.grafo.edges[u, v]["km"] for u, v in zip(camino, camino[1:]))
            escalas = len(camino) - 2
            horas = (km_total / VELOCIDAD_CRUCERO_KMH + TIEMPO_TIERRA_HORAS * (len(camino) - 1))
            
            print(f"\nRuta más corta encontrada:")
            print(f"  Recorrido: {' -> '.join(camino)}")
            print(f"  Escalas: {escalas}")
            print(f"  Distancia total: {formato_km(km_total)} km")
            print(f"  Duración estimada: {formato_duracion(horas)}")
            
            dibujar = messagebox.askyesno("Mostrar Mapa", "¿Desea ver la ruta resaltada en el mapa?")
            if dibujar:
                self.red.mostrar_grafo(ruta_resaltada=camino)

        self.ejecutar_con_salida(_calc)

    def distancia_y_duracion(self):
        origen = self.seleccionar_ciudad_registrada("Distancia y Duración de Vuelo", "Seleccione la ciudad de ORIGEN:")
        if not origen: return
        destino = self.seleccionar_ciudad_registrada("Distancia y Duración de Vuelo", "Seleccione la ciudad de DESTINO:")
        if not destino: return
        
        if origen == destino:
            messagebox.showerror("Error", "La ciudad de origen y destino no pueden ser la misma.")
            return
        
        print(f"\n--- Calculando distancia y duración de '{origen}' a '{destino}' ---")
        self.ejecutar_con_salida(self.red.distancia_y_duracion, origen, destino)

    def listar_rutas(self):
        print("\n--- Listado de Ciudades y Rutas ---")
        self.ejecutar_con_salida(self.red.listar_red)

    def ver_ciudades_disponibles(self):
        print("\n--- Catálogo de Ciudades Disponibles y su Latitud ---")
        self.ejecutar_con_salida(self.red.listar_ciudades_disponibles)

    def salir(self):
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir del sistema?"):
            self.destroy()

if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()
