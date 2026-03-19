# NotFlix - Plataforma de Gestión de Contenido Audiovisual

**NotFlix** es una aplicación web desarrollada como proyecto final para el curso de Python de **Tokio School**. La plataforma permite a los usuarios explorar un catálogo de películas y series, gestionar sus favoritos y realizar un seguimiento de su tiempo de visualización.

## Descripción del Proyecto
El objetivo principal fue desarrollar una aplicación funcional y ordenada que permitiera poner en práctica los conocimientos de desarrollo backend con Django, gestión de bases de datos y lógica de negocio en Python.

### Funcionalidades principales:
* **Sistema de Autenticación:** Registro e inicio de sesión de usuarios.
* **Catálogo Dinámico:** Separación entre películas y series con información detallada (director, año, duración, etc.).
* **Gestión de Usuario:** Posibilidad de marcar contenidos como "Vistos" o "Favoritos".
* **Panel de Estadísticas:** Visualización gráfica del tiempo total de visualización mediante Chart.js.
* **Buscador:** Filtrado de contenido por título, género o director.

## Stack Tecnológico
* **Lenguaje:** Python 3.x
* **Framework Backend:** Django 5.1.2
* **Base de Datos:** SQLite
* **Frontend:** HTML5, CSS3 (Bootstrap 5) y JavaScript (Chart.js)
* **Estética:** SimpleUI para la personalización del panel de administración

## Modelo de Datos
La arquitectura de la base de datos se diseñó para permitir una clasificación eficiente del contenido audiovisual:
* **Película / Serie:** Entidades principales con sus atributos específicos.
* **Director / Categoría:** Modelos relacionados mediante claves foráneas para evitar redundancia.
* **ContenidoUsuario:** Modelo intermedio que gestiona la relación entre los usuarios y el contenido (favoritos/vistos).

## Evolutivos del Proyecto
Basado en el análisis de mejora realizado:
1.  **Búsqueda Avanzada:** Implementación de autocompletado y corrección de sensibilidad a tildes.
2.  **Social:** Sistema de valoraciones y comentarios de usuarios.
3.  **Administración:** Gestión de roles avanzada y visualización de tráfico de la aplicación.

---
Desarrollado por **Enzo Arena** - Noviembre 2024