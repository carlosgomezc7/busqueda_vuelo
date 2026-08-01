# ✈️ Sistema de Administración de Rutas Aéreas de México

Simulación de una red de rutas aéreas nacionales de México mediante **grafos dirigidos**. Cada ciudad es un nodo con coordenadas geográficas reales (latitud/longitud) y cada vuelo es una arista dirigida con su distancia en kilómetros calculada por la fórmula de Haversine.

La red se visualiza sobre el contorno geográfico de la República Mexicana con un estilo de grafo **minimalista oscuro** interactivo.

---

## 📸 Características Principales

### 🗺️ Visualización de Grafo Minimalista

- **Tema oscuro** con fondo profundo (`#0F1117`) y territorio sutil
- **Nodos con efecto glow**: tamaño proporcional al número de conexiones (hubs más grandes)
- **Aristas translúcidas** y finas para un mapa limpio sin saturación
- **Sin etiquetas de distancia** permanentes — mapa despejado
- **Sin ejes, grid ni bordes** — estilo mapa puro
- **Conteo de ciudades y rutas** discreto en esquina inferior

### 🖱️ Interactividad en el Mapa

- **Hover**: al pasar el puntero sobre un nodo aparece un tooltip con:
  - ✈ Nombre de la ciudad
  - Número de conexiones
  - Lista de ciudades destino
- **Clic**: fija el tooltip de una ciudad; un segundo clic lo libera
- **Ruta resaltada**: al buscar la ruta más corta, se puede visualizar con:
  - Línea coral (`#F06449`) con efecto glow
  - Flechas indicadoras de dirección
  - Nodos de la ruta en color de acento

### 🧮 Algoritmos

| Algoritmo | Descripción |
|---|---|
| **Dijkstra** | Ruta más corta por distancia (km) entre dos ciudades |
| **Shortest Path** | Ruta con menor número de escalas |
| **Haversine** | Cálculo de distancia real entre coordenadas geográficas |

### 📋 Operaciones CRUD

| Operación | Detalle |
|---|---|
| Agregar ciudad | Desde un catálogo de **65+ ciudades** mexicanas con búsqueda por nombre |
| Agregar ruta | Vuelo dirigido entre dos ciudades (con opción de ida y vuelta) |
| Eliminar ciudad | Elimina la ciudad y todas sus rutas asociadas |
| Eliminar ruta | Elimina un vuelo específico entre dos ciudades |

### 📊 Consultas

- **Distancia y duración de vuelo** entre cualquier par de ciudades (directo o con escalas)
- **Listado completo** de ciudades registradas con coordenadas
- **Catálogo de ciudades disponibles** con estado (en la red / disponible)
- **Estimación de tiempo de vuelo**: velocidad crucero de 850 km/h + 45 min de despegue/aterrizaje

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| **Python 3.12+** | Lenguaje principal |
| **NetworkX** | Modelado del grafo dirigido y algoritmos (Dijkstra) |
| **Matplotlib** | Visualización del mapa y eventos interactivos |
| **Tkinter** | Interfaz gráfica (GUI) |

---

## 📁 Estructura del Proyecto

```
proyecto_Vuelos/
├── main.py                # Archivo principal (lógica completa + CLI)
├── gui.py                 # Interfaz gráfica con Tkinter (tema oscuro)
├── src/
│   ├── __init__.py
│   ├── datos.py           # Datos geográficos (frontera, catálogo, rutas)
│   ├── red_vuelos.py      # Clase RedVuelos (grafo + visualización)
│   ├── utilidades.py      # Funciones auxiliares (Haversine, formato)
│   └── cli.py             # Menú interactivo por consola
└── documento_proyecto.pdf # Documentación del proyecto
```

---

## 🚀 Instalación y Ejecución

### Requisitos Previos

- Python 3.12 o superior
- pip (gestor de paquetes de Python)

### Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd proyecto_Vuelos

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# Instalar dependencias
pip install networkx matplotlib
```

### Ejecución

```bash
# Interfaz gráfica (Tkinter) — modo por defecto
python main.py
```

La aplicación se abre con la **interfaz gráfica** (GUI) que incluye un tema oscuro tipo Slate con botones interactivos y una consola de salida integrada.

---

## 📌 Menú de Opciones

```
=============================================
  SISTEMA DE RUTAS AÉREAS DE MÉXICO
  Red nacional de vuelos (grafo dirigido)
=============================================
 1. Agregar Ciudad
 2. Agregar Ruta de Vuelo
 3. Eliminar Ciudad
 4. Eliminar Ruta de Vuelo
 5. Mostrar Mapa de Rutas (Grafo)
 6. Ruta Más Corta entre Ciudades (Dijkstra)
 7. Distancia y Duración de Vuelo
 8. Listar Ciudades y Rutas Registradas
 9. Ver Ciudades Disponibles y Latitud
10. Salir
---------------------------------------------
```

---

## 🌐 Datos Precargados

El sistema arranca con **13 ciudades** y **25 rutas** de ejemplo:

**Ciudades iniciales**: Ciudad de México, Guadalajara, Monterrey, Tijuana, Cancún, Mérida, Veracruz, Oaxaca, Puebla, León, Puerto Vallarta, La Paz, San Luis Potosí.

El catálogo completo incluye más de **65 ciudades** mexicanas con coordenadas geográficas reales, listas para ser agregadas al grafo.

---

## 🔍 Características Técnicas

- **Normalización de nombres**: maneja mayúsculas, acentos y preposiciones automáticamente (`"ciudad DE méxico"` → `"Ciudad de México"`)
- **Búsqueda tolerante a acentos**: encontrar ciudades sin necesidad de escribir tildes
- **Grafo dirigido**: las rutas tienen dirección (ida ≠ vuelta)
- **Contorno geográfico real**: polígonos simplificados de los 32 estados de México
- **Interfaz dual**: GUI (Tkinter) y CLI (consola interactiva)
