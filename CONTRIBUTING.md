# Guía de contribución

## Estructura de ramas sugerida

- `main` — código estable y funcional
- `feature/nueva-funcionalidad` — nuevas características
- `fix/nombre-del-bug` — correcciones de errores

## Convenciones de código

- Nombres de funciones y variables en **snake_case** en español.
- Clases en **PascalCase**.
- Cada archivo agrupa una clase con las funciones de su submenú correspondiente.
- Las importaciones circulares se resuelven importando dentro de cada función.

## Cómo añadir una nueva opción al menú

1. Crea o edita el archivo `opcion_N.py` con una clase y sus métodos.
2. Importa la clase en `submenus.py` y añade la función de submenú.
3. Registra la nueva opción en el diccionario `opciones` de `menu_principal.py`.
4. Documenta la nueva consulta SQL en el `README.md`.
