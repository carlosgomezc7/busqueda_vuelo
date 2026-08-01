import sys
from pathlib import Path

# Permitir la ejecución directa desde cualquier directorio de trabajo
_RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
if str(_RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(_RAIZ_PROYECTO))

from src.datos import CATALOGO_CIUDADES, VELOCIDAD_CRUCERO_KMH, TIEMPO_TIERRA_HORAS
from src.utilidades import plegar_acentos, formato_duracion, formato_km
from src.red_vuelos import RedVuelos


def mostrar_menu() -> None:
    """Imprime el menú de opciones en la consola."""
    print("\n=============================================")
    print("  SISTEMA DE RUTAS AÉREAS DE MÉXICO")
    print("  Red nacional de vuelos (grafo dirigido)")
    print("=============================================")
    print("1. Agregar Ciudad")
    print("2. Agregar Ruta de Vuelo")
    print("3. Eliminar Ciudad")
    print("4. Eliminar Ruta de Vuelo")
    print("5. Mostrar Mapa de Rutas (Grafo)")
    print("6. Ruta Más Corta entre Ciudades (Dijkstra)")
    print("7. Distancia y Duración de Vuelo")
    print("8. Listar Ciudades y Rutas Registradas")
    print("9. Ver Ciudades Disponibles y Latitud")
    print("10. Salir")
    print("---------------------------------------------")


def seleccionar_ciudad_del_catalogo(red: RedVuelos) -> str | None:
    """
    Permite elegir una ciudad del catálogo ampliado de México.
    Soporta búsqueda escribiendo parte del nombre (sin acentos).
    Devuelve el nombre canónico o None si se cancela.
    """
    print("\n--- Catálogo de Ciudades de México ---")
    busqueda = input("Escriba parte del nombre para buscar (ENTER = mostrar todas): ").strip()

    if busqueda:
        clave = plegar_acentos(busqueda)
        resultados = [n for n in CATALOGO_CIUDADES if clave in plegar_acentos(n)]
        if not resultados:
            print(f"Sin coincidencias para '{busqueda}'. Verifique el nombre.")
            return None
    else:
        resultados = sorted(CATALOGO_CIUDADES)

    for i, nombre in enumerate(resultados, 1):
        registrada = " (ya registrada)" if red.grafo.has_node(nombre) else ""
        print(f"  {i:2d}. {nombre}{registrada}")

    eleccion = input("Seleccione el número de la ciudad (0 = cancelar): ").strip()
    try:
        indice = int(eleccion)
    except ValueError:
        print("Error: Debe ingresar un número válido.")
        return None
    if indice == 0:
        return None
    if indice < 1 or indice > len(resultados):
        print("Error: Número fuera de rango.")
        return None

    nombre = resultados[indice - 1]
    if red.grafo.has_node(nombre):
        print(f"Error: La ciudad '{nombre}' ya existe en el sistema.")
        return None
    return nombre


def pedir_input(mensaje: str) -> str | None:
    """Solicita texto al usuario, permitiendo regresar con '0'."""
    valor = input(f"{mensaje} (o '0' para regresar): ").strip()
    if valor == '0':
        return None
    return valor

def principal() -> None:
    """Bucle principal del programa con el menú interactivo."""
    red = RedVuelos()

    while True:
        mostrar_menu()
        opcion_str = input("Seleccione una opción (1-10): ").strip()

        try:
            opcion = int(opcion_str)
            if opcion < 1 or opcion > 10:
                print("Error: Por favor, ingrese un número válido entre 1 y 10.")
                continue
        except ValueError:
            print("Error: Entrada no válida. Debe ingresar un número.")
            continue

        # 1. Agregar ciudad (desde el catálogo con búsqueda)
        if opcion == 1:
            nombre = seleccionar_ciudad_del_catalogo(red)
            if nombre is not None:
                red.agregar_ciudad(nombre)

        # 2. Agregar ruta de vuelo (con opción de ida y vuelta)
        elif opcion == 2:
            origen = pedir_input("Ingrese la ciudad de origen")
            if origen is None: continue
            destino = pedir_input("Ingrese la ciudad de destino")
            if destino is None: continue
            red.agregar_ruta(origen, destino)
            redonda = pedir_input("¿Desea agregar también el vuelo de regreso? (s/n)")
            if redonda and redonda.lower() in ("s", "si", "sí"):
                red.agregar_ruta(destino, origen)

        # 3. Eliminar ciudad
        elif opcion == 3:
            ciudad = pedir_input("Ingrese la ciudad a eliminar")
            if ciudad is None: continue
            red.eliminar_ciudad(ciudad)

        # 4. Eliminar ruta
        elif opcion == 4:
            origen = pedir_input("Ingrese la ciudad de origen de la ruta a eliminar")
            if origen is None: continue
            destino = pedir_input("Ingrese la ciudad de destino de la ruta a eliminar")
            if destino is None: continue
            red.eliminar_ruta(origen, destino)

        # 5. Mostrar mapa del grafo
        elif opcion == 5:
            red.mostrar_grafo()

        # 6. Ruta más corta (Dijkstra)
        elif opcion == 6:
            origen = pedir_input("Ingrese la ciudad de origen")
            if origen is None: continue
            destino = pedir_input("Ingrese la ciudad de destino")
            if destino is None: continue
            print("¿Qué desea minimizar?")
            print("  1. Distancia total (km)")
            print("  2. Número de escalas")
            criterio = pedir_input("Seleccione (1-2)")
            if criterio is None: continue
            por_km = criterio != "2"

            camino = red.ruta_mas_corta(origen, destino, por_km=por_km)
            if camino is None:
                continue

            km_total = sum(
                red.grafo.edges[u, v]["km"] for u, v in zip(camino, camino[1:])
            )
            escalas = len(camino) - 2
            horas = (km_total / VELOCIDAD_CRUCERO_KMH
                     + TIEMPO_TIERRA_HORAS * (len(camino) - 1))

            print(f"\nRuta más corta encontrada:")
            print(f"  Recorrido: {' -> '.join(camino)}")
            print(f"  Escalas: {escalas}")
            print(f"  Distancia total: {formato_km(km_total)} km")
            print(f"  Duración estimada: {formato_duracion(horas)}")

            dibujar = pedir_input("\n¿Desea ver la ruta resaltada en el mapa? (s/n)")
            if dibujar and dibujar.lower() in ("s", "si", "sí"):
                red.mostrar_grafo(ruta_resaltada=camino)

        # 7. Distancia y duración de vuelo
        elif opcion == 7:
            origen = pedir_input("Ingrese la ciudad de origen")
            if origen is None: continue
            destino = pedir_input("Ingrese la ciudad de destino")
            if destino is None: continue
            red.distancia_y_duracion(origen, destino)

        # 8. Listar ciudades y rutas registradas
        elif opcion == 8:
            red.listar_red()

        # 9. Ver ciudades disponibles y latitud
        elif opcion == 9:
            red.listar_ciudades_disponibles()

        # 10. Salir
        elif opcion == 10:
            print("Saliendo del sistema. ¡Hasta luego!")
            break


if __name__ == "__main__":
    try:
        principal()
    except KeyboardInterrupt:
        print("\nSaliendo del sistema abruptamente...")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")

