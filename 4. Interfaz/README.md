
Esta carpeta contiene los programas de backend y frontend necesarios para ejecutar y mostrar la página web junto con sus funcionalidades. Entre ellos encontramos:

- El framework **flask**.
- Un archivo HTML (`principal.html.html`).
- La carpeta de imágenes locales (`statics`).
- Un generador de PDFs para cada ruta (`pdf_maker.py`).

---

- **app.py**  

  Código fuente del backend de la aplicación. Contiene la lógica para arrancar un servidor flask y atender las peticiones del frontend:

  - `GET /obtener_rutas` – Devuelve la lista de rutas disponibles y las pasa a `principal.html.html`.  
  - `GET /obtener_especies` – Devuelve las especies asociadas a la ruta seleccionada, realizando previamente consultas a la base de datos SQL para obtener la especie más común en las cuadrículas por las que discurre la ruta.  
  - `POST /personalizar_descripciones` – Envía el prompt de personalización al LLM junto con la lista de especies.  
  - `GET /generar_pdf` – Genera el PDF que muestra las especies filtradas, agrupadas por categoría taxonómica, con sus descripciones e información básica (nombres, estado de conservación, etc.).

- **pdf_maker.py**  

  Módulo en `scripts` que genera la estructura básica del PDF al elegir una ruta, utilizando la librería **fpdf2**. También emplea **pillow** para cargar las imágenes de las especies e incorporarlas al documento.

- **prompts.py**  

  Plantillas de prompt para el LLM:  
  - `TEXT2SQL_PROMPT` – Convierte texto libre en una consulta SQL.  
  - `PERSONALIZE_DESCRIPTION_PROMPT` – Adapta descripciones científicas al estilo indicado.

  Las imágenes de rutas y especies se descargan de forma asíncrona con **asyncio**. En particular, las de rutas se obtienen de [este repositorio público](https://huggingface.co/datasets/alberalm/hiking-trails-images-spain).

- **principal.html.html**  

  Interfaz del frontend: el archivo HTML que carga la parte visual de la página web y gestiona botones y filtros.  
  - **Primera parte:** CSS de la página.  
  - **Segunda parte:** Estructura HTML (botones, tabla, área de texto, imágenes, etc.).  
  - **Tercera parte:** JavaScript para conectar con el backend (`app.py`) y manejar las interacciones.

- **statics**  

  Carpeta con imágenes e íconos estáticos de la aplicación, de acceso directo para la interfaz.

---
