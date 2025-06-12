LUFE - Sistema de Integración
============================

Descripción
----------
LUFE es una aplicación web desarrollada en Django que permite consultar y gestionar información de entidades a través de una API. La aplicación proporciona funcionalidades para:

- Buscar entidades por CUIT
- Consultar indicadores financieros
- Ver autoridades de las entidades
- Gestionar documentos
- Consultar deudas

Requisitos
----------
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Entorno virtual (recomendado)

Instalación
----------
1. Clonar el repositorio:
   ```
   git clone [URL_DEL_REPOSITORIO]
   cd [NOMBRE_DEL_DIRECTORIO]
   ```

2. Crear y activar un entorno virtual:
   ```
   # En Windows
   python -m venv venv
   venv\Scripts\activate

   # En Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configurar las variables de entorno:
   - Crear un archivo `.env` en el directorio raíz
   - Agregar las siguientes variables:
     ```
     LUFE_API_URL=[URL_DE_LA_API]
     LUFE_API_KEY=[CLAVE_DE_LA_API]
     ```

5. Realizar las migraciones de la base de datos:
   ```
   python manage.py migrate
   ```

Ejecución
--------
1. Iniciar el servidor de desarrollo:
   ```
   python manage.py runserver
   ```

2. Abrir un navegador web y acceder a:
   ```
   http://localhost:8000
   ```

Estructura de Carpetas
---------------------
- `core/`: Aplicación principal
  - `templates/`: Plantillas HTML
  - `static/`: Archivos estáticos (CSS, JS, imágenes)
  - `views.py`: Lógica de las vistas
  - `urls.py`: Configuración de URLs
  - `lufe_api.py`: Integración con la API

Funcionalidades Principales
-------------------------
1. Búsqueda de Entidad
   - Ingresar CUIT para obtener información detallada
   - Visualización de datos en formato estructurado

2. Indicadores
   - Consulta de indicadores financieros
   - Visualización de métricas clave

3. Autoridades
   - Listado de autoridades de la entidad
   - Información de contacto y roles

4. Documentos
   - Búsqueda por CUIT y período
   - Descarga de documentos disponibles

5. Deudas
   - Consulta de deudas pendientes
   - Detalles de obligaciones

6. Períodos
   - Visualización de períodos disponibles
   - Filtrado por entidad

Notas Adicionales
---------------
- La aplicación requiere conexión a internet para acceder a la API
- Se recomienda usar un navegador moderno (Chrome, Firefox, Edge)
- Los datos se muestran en formato JSON estructurado
- Se pueden descargar reportes en formato ZIP

Soporte
-------
Para reportar problemas o solicitar ayuda:
- Crear un issue en el repositorio
- Contactar al equipo de desarrollo

Licencia
-------
[ESPECIFICAR LICENCIA] 