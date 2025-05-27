
Esta carpeta continene los Programas tanto de Backend como de Frontend necesarios para correr y ejecutar la pagina web junto con sus funcionalidades, entre ellas encontramos un ``Flask``, un archivo html (``principal.html.html``), carpeta de imágenes en local (``statics``), y un generador de los pdf de cada ruta (`pdf_maker.py`)
- **app.py** 

    Este es el encargado de la parte del Backend y será el que ejecute en python las funciones necesarias para la funcionalidad e interconexión del fronted y otros programas. Punto de entrada de la aplicación Flask. Define las rutas REST:
    tenemos varias funciones:

  - `GET /obtener_rutas` – Devuelve la lista de rutas disponibles, despúes se las pasa a `principal.html.html`. 

  - `GET /obtener_especies` – Devuelve las especies asociadas a una ruta seleccionada que recibe del fronted, haciendo antes peticiones a la base de datos SQL que seleccionará la  especie más común en los mallas donde pase esta ruta.

  - `POST /personalizar_descripciones` – Envía el prompt y de personalización al LLM con la lista de espcies.  

  - `GET /generar_pdf` – Se encarga de generar el pdf que enseñará las especies despúes de pasar por los filtros anteriores en un listado separado por grupos taxonomicos y descripciones además de información basica como nombres, estado de conservación.

- **pdf_maker.py**

    La carpeta ``scripts`` contiene el código ``pdf_maker.py`` que genera la base del pdf que aparece al elegir una ruta, utilizando la librería ``fpdf2``.  Además, también emplea la librería ``pillow`` para cargar las imágenes de las especies e incorporarlas al pdf.

    - **prompts.py**  

        Plantillas de prompt para el LLM:
        - `TEXT2SQL_PROMPT` – Convierte texto libre en consulta SQL.  
        - `PERSONALIZE_DESCRIPTION_PROMPT` – Adapta descripciones científicas al estilo indicado.

    Las imágenes de las rutas y de las especies se descargan en paralelo utilizando la librería ``asyncio``. En concreto, las imágenes de las rutas se obtienen de [este repositorio público](https://huggingface.co/datasets/alberalm/hiking-trails-images-spain), que se crearon anteriormente (véase ``2. Base de datos``).

- **principal.html.html**  

   Es el equivalente al fronted y será el archivo html que cargará la parte visual de la pagina web además de las funcionalidades de botones y filtros.
  - Primera parte: CSS de la pagina web.
  - Segunda parte: Toda la programación del html con botones, tabla, area de texto, imagenes de la pagina etcetera.
  - Tercera parte: Toda la programación de JavaScript, donde se importan las funcionalidades de botones y conexiones con el backend (``app.py``).

- **statics**  

  Carpeta con imágenes e iconos estáticos de la aplicación, nombre predeterminado de facil acceso.

---

