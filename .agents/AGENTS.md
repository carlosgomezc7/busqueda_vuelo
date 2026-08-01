# Reglas del Proyecto — Sistema de Rutas Aéreas de México

## Idioma

- Todo el código, comentarios, docstrings, mensajes al usuario, nombres de variables, nombres de funciones y documentación deben estar **en español**.
- Las únicas excepciones son palabras reservadas de Python y nombres de librerías externas (e.g., `NetworkX`, `Matplotlib`, `Tkinter`).

## Arquitectura y Estructura del Proyecto

- **Respetar la estructura modular existente**:
  - `src/datos.py` → Datos geográficos, catálogo de ciudades, constantes.
  - `src/red_vuelos.py` → Clase `RedVuelos` con la lógica del grafo dirigido.
  - `src/utilidades.py` → Funciones auxiliares (Haversine, formato, normalización).
  - `src/cli.py` → Menú interactivo por consola.
  - `gui.py` → Interfaz gráfica con Tkinter.
  - `main.py` → Archivo principal (versión monolítica de referencia).
- Los módulos nuevos deben colocarse en `src/` y registrar sus imports en `src/__init__.py` si es necesario.
- No duplicar lógica que ya exista en `src/`. Si `main.py` contiene funcionalidad que también está en `src/`, priorizar el uso de `src/`.

## Convenciones de Código

### Nombres

- Variables, funciones y métodos en **snake_case** en español: `ruta_mas_corta`, `agregar_ciudad`, `formato_duracion`.
- Clases en **PascalCase** en español: `RedVuelos`, `CustomDialog`.
- Constantes en **MAYÚSCULAS_CON_GUIONES**: `VELOCIDAD_CRUCERO_KMH`, `CATALOGO_CIUDADES`.
- Nombres privados con prefijo `_`: `_cargar_datos_iniciales`, `_buscar_ciudad`.

### Documentación

- Todas las funciones y clases deben tener **docstrings** en español describiendo su propósito.
- Los docstrings usan comillas triples `"""..."""`.
- Los comentarios de sección usan el estilo: `# ── Descripción ──────────`.

### Type Hints

- Usar **type hints** de Python 3.12+ (e.g., `str | None` en lugar de `Optional[str]`).
- Los métodos que devuelven booleanos de éxito usan `-> bool`.
- Los métodos sin retorno explícito usan `-> None`.

## Grafo y Modelo de Datos

- El grafo es un **`networkx.DiGraph`** (dirigido): las rutas tienen dirección (ida ≠ vuelta).
- Cada **nodo** almacena su posición como `pos=(latitud, longitud)`.
- Cada **arista** almacena la distancia en kilómetros como `km=<valor>`.
- Las distancias se calculan con la **fórmula de Haversine** (`distancia_haversine` en `src/utilidades.py`).
- Los nombres de ciudades se normalizan con `normalizar_nombre()` (capitalización correcta, respetando preposiciones como "de", "del", "la").
- La búsqueda de ciudades debe ser **tolerante a acentos** usando `plegar_acentos()`.

## Visualización (Matplotlib)

- Usar el **tema oscuro minimalista** del proyecto:
  - Fondo: `#0F1117`
  - Territorio: `#1A1E2B`
  - Nodos: `#5B8DEE` (azul suave)
  - Ruta resaltada: `#F06449` (coral)
  - Texto: `#E8ECF1`
- Los nodos tienen **tamaño proporcional al número de conexiones** (hubs más grandes).
- Las aristas son **translúcidas y finas** para mantener un mapa limpio.
- **No** mostrar ejes, grid ni bordes — estilo mapa puro.
- Los tooltips interactivos muestran: nombre de la ciudad, número de conexiones y destinos.

## GUI (Tkinter)

- Mantener el **tema Slate oscuro** existente:
  - `BG_PRINCIPAL = "#0f172a"` (Slate 900)
  - `BG_PANELES = "#1e293b"` (Slate 800)
  - `COLOR_ACCENTO = "#3b82f6"` (Blue 500)
- Los diálogos personalizados (`CustomDialog`) se prefieren sobre los diálogos nativos de Tkinter.
- La consola integrada redirige `stdout` con `StdoutRedirector`.

## Mensajes al Usuario

- Los mensajes de **éxito** comienzan con `"Éxito: ..."`.
- Los mensajes de **error** comienzan con `"Error: ..."`.
- Las distancias se formatean con `formato_km()` (separador de miles con espacio).
- Las duraciones se formatean con `formato_duracion()` (formato `"X h YY min"`).
- La estimación de tiempo de vuelo usa: velocidad crucero de **850 km/h** + **45 min** de despegue/aterrizaje por tramo.

## Dependencias

- **Solo** se usan las siguientes librerías externas:
  - `networkx` — modelado del grafo y algoritmos (Dijkstra).
  - `matplotlib` — visualización del mapa e interactividad.
  - `tkinter` — interfaz gráfica (incluida con Python).
- No agregar dependencias nuevas sin justificación explícita.

## Documentación del Proyecto

- Cada vez que se haga un cambio significativo en el proyecto, **actualizar `README.md`** para reflejar el estado actual.
- El `README.md` debe mantenerse en español y seguir la estructura existente (características, tecnologías, estructura, instalación, menú).

## Testing y Ejecución

- El punto de entrada principal es `python main.py` (abre la GUI por defecto).
- La CLI se ejecuta desde `src/cli.py` directamente: `python -m src.cli`.
- Antes de entregar cambios, verificar que no haya errores de importación y que la estructura del grafo sea consistente.
