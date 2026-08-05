"""
Módulo de autenticación y gestión de usuarios del sistema.

Define los roles, las credenciales registradas y la lógica de
inicio de sesión con validación estricta.
"""

from src.datos import cargar_base_datos

# ── Roles del sistema ──────────────────────────────────────────
ROL_ADMINISTRADOR = "administrador"
ROL_PASAJERO = "pasajero"

# ── Base de datos de usuarios por defecto (fallback) ────────────
_USUARIOS_DEFAULT: dict[str, dict[str, str]] = {
    "Administrador": {
        "contrasena": "Administrador",
        "rol": ROL_ADMINISTRADOR,
    },
    "Pasajero": {
        "contrasena": "Pasajero",
        "rol": ROL_PASAJERO,
    },
}

_USUARIOS = _USUARIOS_DEFAULT


def obtener_usuarios_db() -> dict[str, dict[str, str]]:
    """Carga y retorna los usuarios almacenados en db.json."""
    datos_db = cargar_base_datos()
    return datos_db.get("usuarios", _USUARIOS_DEFAULT)


def iniciar_sesion(usuario: str, contrasena: str) -> dict | None:
    """
    Valida las credenciales del usuario de forma estricta.

    La comparación de usuario y contraseña es exacta (sensible a
    mayúsculas/minúsculas). Imprime mensajes de error específicos
    según el tipo de fallo.

    Devuelve un diccionario ``{"usuario": ..., "rol": ...}`` si las
    credenciales son correctas, o ``None`` si la validación falla.
    """
    usuarios = obtener_usuarios_db()
    datos = usuarios.get(usuario)
    if datos is None:
        print("Error: El usuario no existe en el sistema.")
        return None
    if datos.get("contrasena") != contrasena:
        print("Error: La contraseña es incorrecta.")
        return None
    return {"usuario": usuario, "rol": datos.get("rol", ROL_PASAJERO)}

