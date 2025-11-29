# ScrappingS4B: Web Scraping Asistido por LLM

Este proyecto integra **Django** y **BeautifulSoup** para la recolección de datos web con la capacidad de procesamiento de lenguaje natural de **Ollama** (modelo Gemma3:4b). Esto permite a los usuarios realizar consultas y filtrados avanzados en la base de datos PostgreSQL utilizando lenguaje natural.

---

## Requisitos Previos

Asegúrate de tener instalado y configurado lo siguiente en tu sistema antes de comenzar:

1.  **Python (3.x):** Debe estar instalado.
2.  **PostgreSQL:** Motor de base de datos.
    - Versión de referencia: 18.x
3.  **Ollama:** Herramienta para ejecutar modelos de lenguaje localmente.
    - Modelo requerido: **Gemma3:4b**. Consíguelo ejecutando el siguiente comando:
      ```
      ollama run gemma3:4b
      ```

---

## Guía de Configuración e Instalación

Sigue estos pasos en orden para poner en marcha la aplicación.

### Paso 1: Clonar el Repositorio

Abre tu terminal, navega hasta la carpeta donde deseas alojar el proyecto y clona el repositorio:

git clone https://github.com/MMaxAR1901/ScrappingS4B.git
cd ScrappingS4B

### Paso 2: Crear y Activar el Entorno Virtual

Es fundamental crear un entorno virtual para que el proyecto funcione.

1.  **Crear el entorno virtual:**
    ```
    python -m venv venv
    ```
2.  **Activar el entorno:**
    - Windows (CMD/PowerShell):
      ```
      venv\Scripts\activate
      ```
    - Linux/macOS:
      ```
      source venv/bin/activate
      ```

### Paso 3: Instalar las Dependencias de Python

Con el entorno virtual activado (verás (venv) al inicio de tu línea de comandos), instala todas las librerías necesarias:

pip install Django==5.2.8 beautifulsoup4 ollama requests psycopg2-binary

### Paso 4: Configurar la Base de Datos (PostgreSQL)

1.  **Crear la Base de Datos:** En tu administrador de PostgreSQL, crea una nueva base de datos llamada **Scrapping**.
2.  **Ajustar settings.py:** Edita el archivo `Scrapping_app/Scrapping_app/settings.py` y configura la sección DATABASES con tus credenciales.

    > NOTA: Asegúrate de que los valores de USER, PASSWORD y PORT coincidan con tu configuración local de PostgreSQL.

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'Scrapping',
            'USER': 'postgres',      # <-- Cambiar si es necesario
            'PASSWORD': 'admin1901',  # <-- Cambiar con tu contraseña
            'HOST': 'localhost',
            'PORT': '5433',           # <-- Cambiar si es necesario
        }
    }
    ```

### Paso 5: Aplicar Migraciones

Desde la carpeta raíz del proyecto (donde se encuentra `manage.py`), ejecuta los comandos para crear las tablas en tu base de datos:

1.  **Crear archivos de migración (si hay cambios en modelos):**
    ```
    python manage.py makemigrations
    ```
2.  **Aplicar las migraciones a PostgreSQL:**
    ```
    python manage.py migrate
    ```

### Paso 6: Ejecutar la Aplicación

Inicia el servidor de desarrollo de Django:

python manage.py runserver

### Paso 7: Acceder y Probar

Ingresa a la URL de tu servidor (generalmente `http://127.0.0.1:8000/`) la cual correra el scrapper y una vez terminado redirigira a la lista de paises en donde podras interactuar con la aplicación.

---

## Uso de la Aplicación y Consulta LLM

El modelo **Gemma3:4b** transforma las consultas de **lenguaje natural** en código Django ORM, lo que permite un filtrado dinámico de los datos.

### Ejemplos de Consultas Válidas

Puedes introducir comandos de filtrado como:

1.  `Dame los paises que inicien con letra M y tengan una capital que termine con K`
2.  `Dame los paises que tienen una población mayor a 1000`
3.  `Dame los paises que tienen una población entre 1000 y 5000`
4.  `Dame los paises con un area menos a 10000`
