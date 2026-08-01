"""
Módulo con la clase principal RedVuelos para la gestión del grafo de vuelos.
"""

import matplotlib.pyplot as plt
import networkx as nx

from src.datos import (
    FRONTERA_MEXICO,
    CATALOGO_CIUDADES,
    CIUDADES_INICIALES,
    RUTAS_INICIALES,
    VELOCIDAD_CRUCERO_KMH,
    TIEMPO_TIERRA_HORAS,
)
from src.utilidades import (
    normalizar_nombre,
    plegar_acentos,
    distancia_haversine,
    formato_duracion,
    formato_km,
)


class RedVuelos:
    """
    Gestiona la red de rutas aéreas de México mediante un grafo dirigido
    (networkx.DiGraph). Cada nodo almacena su posición geográfica (lat, lon)
    y cada arista almacena su distancia en kilómetros.
    """

    def __init__(self) -> None:
        self.grafo = nx.DiGraph()
        self._cargar_datos_iniciales()

    # ----------------------- Datos iniciales -----------------------

    def _cargar_datos_iniciales(self) -> None:
        """Precarga las ciudades y rutas de ejemplo del sistema."""
        for nombre in CIUDADES_INICIALES:
            self._agregar_nodo(nombre)
        for origen, destino in RUTAS_INICIALES:
            self._agregar_arista(origen, destino)

    def _agregar_nodo(self, nombre: str) -> bool:
        """Agrega un nodo con su posición geográfica. Devuelve True si se agregó."""
        if nombre not in CATALOGO_CIUDADES:
            return False
        lat, lon = CATALOGO_CIUDADES[nombre]
        self.grafo.add_node(nombre, pos=(lat, lon))
        return True

    def _agregar_arista(self, origen: str, destino: str) -> bool:
        """Agrega una arista dirigida con su distancia en km. Devuelve True si se agregó."""
        if self.grafo.has_edge(origen, destino):
            return False
        lat1, lon1 = self.grafo.nodes[origen]["pos"]
        lat2, lon2 = self.grafo.nodes[destino]["pos"]
        km = distancia_haversine(lat1, lon1, lat2, lon2)
        self.grafo.add_edge(origen, destino, km=km)
        return True

    # ------------------------- Utilidades -------------------------

    def _buscar_ciudad(self, texto: str) -> str | None:
        """
        Busca el nombre canónico de una ciudad en el grafo, tolerando
        diferencias de mayúsculas y acentos. Devuelve None si no se encuentra.
        """
        texto_norm = plegar_acentos(normalizar_nombre(texto))
        if not texto_norm:
            return None
        candidatos = [
            n for n in self.grafo.nodes
            if plegar_acentos(n) == texto_norm
        ]
        if len(candidatos) == 1:
            return candidatos[0]
        if len(candidatos) > 1:
            print("Error: El nombre es ambiguo. ¿A cuál te refieres?")
            for c in candidatos:
                print(f"  - {c}")
            return None
        return None

    def _pedir_ciudad(self, mensaje: str) -> str | None:
        """Pide el nombre de una ciudad existente al usuario y la valida."""
        texto = input(mensaje)
        ciudad = self._buscar_ciudad(texto)
        if ciudad is None:
            print(f"Error: La ciudad '{texto.strip()}' no existe. Debe agregarla primero.")
        return ciudad

    # ---------------------- Operaciones del menú ----------------------

    def agregar_ciudad(self, nombre: str) -> None:
        """Agrega una nueva ciudad (nodo) al grafo."""
        nombre_norm = normalizar_nombre(nombre)
        if not nombre_norm:
            print("Error: El nombre de la ciudad no puede estar vacío.")
            return
        if nombre_norm not in CATALOGO_CIUDADES:
            print(f"Error: '{nombre_norm}' no está en el catálogo de México.")
            return
        if self.grafo.has_node(nombre_norm):
            print(f"Error: La ciudad '{nombre_norm}' ya existe en el sistema.")
            return
        self._agregar_nodo(nombre_norm)
        lat, lon = CATALOGO_CIUDADES[nombre_norm]
        print(f"Éxito: Ciudad '{nombre_norm}' agregada ({lat:.2f}, {lon:.2f}).")

    def agregar_ruta(self, origen: str, destino: str) -> None:
        """Agrega una ruta de vuelo dirigida entre dos ciudades."""
        origen_norm = self._buscar_ciudad(origen)
        if origen_norm is None:
            print(f"Error: La ciudad de origen '{origen.strip()}' no existe.")
            return
        destino_norm = self._buscar_ciudad(destino)
        if destino_norm is None:
            print(f"Error: La ciudad de destino '{destino.strip()}' no existe.")
            return
        if origen_norm == destino_norm:
            print("Error: El origen y el destino deben ser ciudades distintas.")
            return
        if self.grafo.has_edge(origen_norm, destino_norm):
            print(f"Error: La ruta de '{origen_norm}' a '{destino_norm}' ya existe.")
            return
        self._agregar_arista(origen_norm, destino_norm)
        km = self.grafo.edges[origen_norm, destino_norm]["km"]
        print(f"Éxito: Ruta de vuelo desde '{origen_norm}' hacia '{destino_norm}' "
              f"({formato_km(km)} km) agregada.")

    def eliminar_ciudad(self, ciudad: str) -> None:
        """Elimina una ciudad y todas sus rutas asociadas."""
        ciudad_norm = self._buscar_ciudad(ciudad)
        if ciudad_norm is None:
            print(f"Error: La ciudad '{ciudad.strip()}' no existe en el sistema.")
            return
        self.grafo.remove_node(ciudad_norm)
        print(f"Éxito: La ciudad '{ciudad_norm}' y todas sus rutas han sido eliminadas.")

    def eliminar_ruta(self, origen: str, destino: str) -> None:
        """Elimina una ruta de vuelo específica entre dos ciudades."""
        origen_norm = self._buscar_ciudad(origen)
        destino_norm = self._buscar_ciudad(destino)
        if origen_norm is not None and destino_norm is not None:
            if self.grafo.has_edge(origen_norm, destino_norm):
                self.grafo.remove_edge(origen_norm, destino_norm)
                print(f"Éxito: Ruta de '{origen_norm}' a '{destino_norm}' eliminada.")
                return
        print(f"Error: No existe una ruta directa desde '{origen.strip()}' "
              f"hacia '{destino.strip()}'.")

    def ruta_mas_corta(self, origen: str, destino: str, por_km: bool = True) -> list | None:
        """
        Calcula la ruta más corta entre dos ciudades usando el algoritmo de
        Dijkstra. Si por_km es True minimiza la distancia en kilómetros;
        en caso contrario minimiza el número de escalas.
        Devuelve la lista de ciudades del camino, o None si no existe.
        """
        origen_norm = self._buscar_ciudad(origen)
        if origen_norm is None:
            print(f"Error: La ciudad de origen '{origen.strip()}' no existe.")
            return None
        destino_norm = self._buscar_ciudad(destino)
        if destino_norm is None:
            print(f"Error: La ciudad de destino '{destino.strip()}' no existe.")
            return None
        if origen_norm == destino_norm:
            print("Error: El origen y el destino deben ser ciudades distintas.")
            return None

        try:
            if por_km:
                camino = nx.dijkstra_path(self.grafo, origen_norm, destino_norm, weight="km")
            else:
                camino = nx.shortest_path(self.grafo, origen_norm, destino_norm)
        except nx.NetworkXNoPath:
            print(f"Error: No existe una ruta (directa o con escalas) de "
                  f"'{origen_norm}' a '{destino_norm}'.")
            return None

        return camino

    def distancia_y_duracion(self, origen: str, destino: str) -> None:
        """
        Muestra la distancia y el tiempo estimado de vuelo entre dos
        ciudades. Si no hay vuelo directo, calcula el mejor recorrido
        con escalas.
        """
        origen_norm = self._buscar_ciudad(origen)
        if origen_norm is None:
            print(f"Error: La ciudad de origen '{origen.strip()}' no existe.")
            return
        destino_norm = self._buscar_ciudad(destino)
        if destino_norm is None:
            print(f"Error: La ciudad de destino '{destino.strip()}' no existe.")
            return

        if self.grafo.has_edge(origen_norm, destino_norm):
            km = self.grafo.edges[origen_norm, destino_norm]["km"]
            horas = km / VELOCIDAD_CRUCERO_KMH + TIEMPO_TIERRA_HORAS
            print(f"Vuelo directo '{origen_norm}' -> '{destino_norm}':")
            print(f"  Distancia: {formato_km(km)} km")
            print(f"  Duración estimada: {formato_duracion(horas)}")
            return

        camino = self.ruta_mas_corta(origen_norm, destino_norm, por_km=True)
        if camino is None:
            return

        km_total = sum(
            self.grafo.edges[u, v]["km"] for u, v in zip(camino, camino[1:])
        )
        escalas = len(camino) - 2
        horas = km_total / VELOCIDAD_CRUCERO_KMH + TIEMPO_TIERRA_HORAS * (len(camino) - 1)
        print(f"No hay vuelo directo. Mejor recorrido con escalas:")
        print(f"  Ruta: {' -> '.join(camino)} ({escalas} escala(s))")
        print(f"  Distancia total: {formato_km(km_total)} km")
        print(f"  Duración estimada: {formato_duracion(horas)}")

    def listar_red(self) -> None:
        """Imprime en consola todas las ciudades y rutas registradas."""
        print(f"\n=== RED ACTUAL: {self.grafo.number_of_nodes()} ciudades, "
              f"{self.grafo.number_of_edges()} rutas ===")
        print("\nCiudades registradas:")
        for nombre in sorted(self.grafo.nodes):
            lat, lon = self.grafo.nodes[nombre]["pos"]
            print(f"  - {nombre:<28} (Latitud: {lat:.2f}° N, Longitud: {abs(lon):.2f}° O)")
        print("\nRutas de vuelo (dirigidas):")
        if self.grafo.number_of_edges() == 0:
            print("  (Sin rutas registradas)")
        for origen, destino in sorted(self.grafo.edges):
            km = self.grafo.edges[origen, destino]["km"]
            print(f"  - {origen} -> {destino}   ({formato_km(km)} km)")

    def listar_ciudades_disponibles(self) -> None:
        """
        Muestra todas las ciudades disponibles en el catálogo de México
        junto con su latitud y su estado actual en la red.
        """
        total_catalogo = len(CATALOGO_CIUDADES)
        registradas = sum(1 for c in CATALOGO_CIUDADES if self.grafo.has_node(c))

        print("\n=============================================================")
        print("  CATÁLOGO DE CIUDADES DISPONIBLES EN MÉXICO")
        print("=============================================================")
        print(f"Total en catálogo: {total_catalogo} ciudades | En la red activa: {registradas} ciudades\n")
        print(f"  {'No.':<4} {'Ciudad':<30} {'Latitud':<12} {'Longitud':<12} {'Estado'}")
        print("  " + "-" * 70)

        for i, (nombre, (lat, lon)) in enumerate(sorted(CATALOGO_CIUDADES.items()), 1):
            estado = "En la red" if self.grafo.has_node(nombre) else "Disponible"
            lat_str = f"{lat:.2f}° N"
            lon_str = f"{abs(lon):.2f}° O"
            print(f"  {i:<4} {nombre:<30} {lat_str:<12} {lon_str:<12} {estado}")
        print("-------------------------------------------------------------\n")


    def mostrar_grafo(self, ruta_resaltada: list | None = None) -> None:
        """
        Dibuja la red de rutas aéreas sobre el mapa de México con un estilo
        de grafo minimalista (fondo oscuro, nodos limpios, aristas sutiles).
        Si se indica una ruta_resaltada (lista de ciudades), se pinta
        con un color de acento sobre el mapa.
        """
        if self.grafo.number_of_nodes() == 0:
            print("El sistema no tiene ciudades registradas para mostrar. "
                  "Agregue ciudades primero.")
            return

        print(f"Generando mapa con {self.grafo.number_of_nodes()} ciudades y "
              f"{self.grafo.number_of_edges()} rutas...")

        # ── Paleta minimalista ──────────────────────────────────────────
        COLOR_BG       = "#0F1117"   # fondo oscuro profundo
        COLOR_TERRA    = "#1A1E2B"   # relleno territorio
        COLOR_BORDE    = "#2A3045"   # borde territorio
        COLOR_ARISTA   = "#3A4060"   # aristas normales
        COLOR_NODO     = "#5B8DEE"   # nodos base (azul suave)
        COLOR_HALO     = "#5B8DEE"   # halo nodo
        COLOR_RUTA     = "#F06449"   # ruta resaltada (coral)
        COLOR_NODO_RT  = "#F06449"   # nodos de la ruta
        COLOR_TEXTO    = "#E8ECF1"   # texto claro

        fig, ax = plt.subplots(figsize=(14, 9))
        fig.patch.set_facecolor(COLOR_BG)
        ax.set_facecolor(COLOR_BG)

        # ── Contorno del territorio mexicano (sutil) ────────────────────
        todos_lons, todos_lats = [], []
        for anillo in FRONTERA_MEXICO:
            lons_anillo = [p[0] for p in anillo]
            lats_anillo = [p[1] for p in anillo]
            ax.fill(lons_anillo, lats_anillo, facecolor=COLOR_TERRA,
                    edgecolor=COLOR_BORDE, linewidth=0.8, zorder=1)
            todos_lons.extend(lons_anillo)
            todos_lats.extend(lats_anillo)

        # ── Posiciones geográficas ──────────────────────────────────────
        pos = {nombre: (datos["pos"][1], datos["pos"][0])  # (lon, lat)
               for nombre, datos in self.grafo.nodes(data=True)}

        grados = dict(self.grafo.degree())
        max_grado = max(grados.values()) if grados else 1

        # ── Aristas ────────────────────────────────────────────────────
        aristas_resaltadas = (set(zip(ruta_resaltada, ruta_resaltada[1:]))
                              if ruta_resaltada else set())
        aristas_normales = [
            (u, v) for u, v in self.grafo.edges
            if (u, v) not in aristas_resaltadas
        ]

        # Dibujar aristas manualmente para control de alpha
        for u, v in aristas_normales:
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            ax.plot([x0, x1], [y0, y1], color=COLOR_ARISTA,
                    linewidth=0.7, alpha=0.45, zorder=2, solid_capstyle="round")

        # ── Nodos ──────────────────────────────────────────────────────
        nodos_resaltados = set(ruta_resaltada) if ruta_resaltada else set()
        nombres_nodos = list(self.grafo.nodes)
        coords_nodos = [pos[n] for n in nombres_nodos]

        for nombre in nombres_nodos:
            cx, cy = pos[nombre]
            g = grados[nombre]
            # Radio proporcional al grado (normalizado)
            r_base = 4 + 6 * (g / max_grado)
            es_ruta = nombre in nodos_resaltados

            # Halo externo (glow)
            color_h = COLOR_RUTA if es_ruta else COLOR_HALO
            ax.plot(cx, cy, 'o', markersize=r_base + 5,
                    color=color_h, alpha=0.15, zorder=3)
            ax.plot(cx, cy, 'o', markersize=r_base + 2.5,
                    color=color_h, alpha=0.25, zorder=3)

            # Punto principal
            color_n = COLOR_NODO_RT if es_ruta else COLOR_NODO
            ax.plot(cx, cy, 'o', markersize=r_base,
                    color=color_n, alpha=0.95, zorder=4,
                    markeredgecolor="white", markeredgewidth=0.4)

        # ── Ruta resaltada ─────────────────────────────────────────────
        if ruta_resaltada:
            for u, v in aristas_resaltadas:
                x0, y0 = pos[u]
                x1, y1 = pos[v]
                # Glow de la ruta
                ax.plot([x0, x1], [y0, y1], color=COLOR_RUTA,
                        linewidth=4.5, alpha=0.18, zorder=5,
                        solid_capstyle="round")
                # Línea de la ruta
                ax.plot([x0, x1], [y0, y1], color=COLOR_RUTA,
                        linewidth=2.0, alpha=0.90, zorder=6,
                        solid_capstyle="round")
                # Flecha indicadora de dirección
                mx, my = (x0 + x1) / 2, (y0 + y1) / 2
                dx, dy = x1 - x0, y1 - y0
                ax.annotate("", xy=(mx + dx * 0.01, my + dy * 0.01),
                            xytext=(mx - dx * 0.01, my - dy * 0.01),
                            arrowprops=dict(arrowstyle="->", color=COLOR_RUTA,
                                            lw=1.8), zorder=7)
            print("Ruta resaltada: " + " → ".join(ruta_resaltada))

        # ── Tooltip interactivo (hover / clic) ─────────────────────────
        annot = ax.annotate(
            "", xy=(0, 0), xytext=(14, 14),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.5", fc="#1C2033", ec="#5B8DEE",
                      lw=1.2, alpha=0.95),
            fontsize=9, fontweight="bold", color=COLOR_TEXTO,
            zorder=10, visible=False,
        )

        ciudad_fijada = {"nombre": None}

        def _info_ciudad(nombre):
            """Genera texto informativo para el tooltip."""
            g = grados[nombre]
            vecinos = list(self.grafo.successors(nombre))
            lineas = [f"✈  {nombre}", f"   {g} conexiones"]
            if vecinos:
                lista = ", ".join(sorted(vecinos)[:6])
                if len(vecinos) > 6:
                    lista += f" (+{len(vecinos) - 6})"
                lineas.append(f"   → {lista}")
            return "\n".join(lineas)

        def _nodo_cercano(event):
            dist_min, nombre_min = float("inf"), None
            for nombre, (cx, cy) in zip(nombres_nodos, coords_nodos):
                px, py = ax.transData.transform((cx, cy))
                d = ((event.x - px) ** 2 + (event.y - py) ** 2) ** 0.5
                if d < dist_min:
                    dist_min, nombre_min = d, nombre
            return nombre_min if dist_min < 20 else None

        def _mostrar_tooltip(nombre):
            cx, cy = pos[nombre]
            annot.xy = (cx, cy)
            annot.set_text(_info_ciudad(nombre))
            annot.set_visible(True)

        def _on_move(event):
            if event.inaxes != ax or ciudad_fijada["nombre"]:
                return
            nombre = _nodo_cercano(event)
            if nombre:
                _mostrar_tooltip(nombre)
            else:
                annot.set_visible(False)
            fig.canvas.draw_idle()

        def _on_click(event):
            if event.inaxes != ax:
                return
            if ciudad_fijada["nombre"]:
                ciudad_fijada["nombre"] = None
                annot.set_visible(False)
                fig.canvas.draw_idle()
                return
            nombre = _nodo_cercano(event)
            if nombre:
                ciudad_fijada["nombre"] = nombre
                _mostrar_tooltip(nombre)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", _on_move)
        fig.canvas.mpl_connect("button_press_event", _on_click)

        # ── Límites y aspecto ──────────────────────────────────────────
        margen = 0.8
        ax.set_xlim(min(todos_lons) - margen, max(todos_lons) + margen)
        ax.set_ylim(min(todos_lats) - margen, max(todos_lats) + margen)
        ax.set_aspect(1.09)

        # Eliminar ejes y bordes para un look limpio
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Título discreto
        ax.set_title("Red de Rutas Aéreas",
                     fontsize=14, fontweight=300, color="#8090A8",
                     pad=12, loc="left")

        # Leyenda mínima
        ax.text(0.99, 0.02,
                f"{self.grafo.number_of_nodes()} ciudades  ·  "
                f"{self.grafo.number_of_edges()} rutas",
                transform=ax.transAxes, fontsize=8, color="#556070",
                ha="right", va="bottom")

        plt.tight_layout()
        plt.show()
