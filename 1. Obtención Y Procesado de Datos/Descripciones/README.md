Esta carpeta contiene el código necesario para descargar y procesar los datos de las diferentes fuentes que proporcionan descripciones de especies. Algunas de estas utilizan la librería ``selenium`` para realizar scraping de las páginas web.

En total, se han utilizado 5 fuentes de datos:

- **SEO BirdLife:** Recopilación de aves en España junto con descripciones y otra información adicional. Los datos de esta página se recopilan mediante scraping.

- **Fungipedia:** Recopilación de hongos en España junto con descripciones y otra información adicional. Los datos de esta página se recopilan mediante scraping.

- **IEET - Atlas y Libros Rojos de vertebrados:** Recopilación de vertebrados presentes en España, acompañados de fichas y cartografía, que se recopilaron mediante scraping. Después, para los mamíferos y los peces, que incluían descripciones en sus fichas, se creó un programa para extraerlas.

- **VertebradosIbericos:** Recopilación de vertebrados presentes en España, con muchas de ellos acompañados de descripciones y otros datos. Este conjunto de descripciones se extrajo de forma manual, y se encuentra dentro de la carpeta ``Datos VertebradosIbericos``.

- **IEPNB-EIDOS:** Se descargó de forma manual la información de la página web de EIDOS, ya que no se pueden obtener descripciones de las especies via la API. Para ello, se fueron filtrando los nombres mediante la barra de búsqueda de la plataforma, de forma que hubiera menos de 1000 resultados (cantidad a partir de la cual no permite las descargas en formato Excel). Para simplificar y hacer más eficiente el proceso, se creó un programa que sugería el término por el que filtrar con el que se obtendría información de la mayor cantidad de especies, lo que utilizaba los nombres aceptados de la taxonomía de EIDOS, que sí se obtuvo mediante API. En total, se recabó información de 52.783 especies (``Datos EIDOS/_EIDOS_base_de_datos.xlsx``), aunque tan solo 1.777 tenían descripción (``Datos EIDOS/EIDOS_descripciones.xlsx``).

| Fuente | Código empleado | Descripciones obtenidas |
|----------|----------|----------|
| SEO BirdLife    | ``seo_scraper.ipynb``   | Aves - 611   |
| Fungipedia    | ``fungipedia_scraper.ipynb``   | Hongos - 578   |
| IEET    | ``ieet_scraper.ipynb``<br>``ieet_description_extractor.ipynb``   | Mamíferos - 98<br>Peces - 44   |
| VertebradosIbericos    | Recopilación manual  | Anfibios - 31<br>Aves - 127<br>Mamíferos - 60<br>Peces - 50<br>Reptiles - 84  |
| IEPNB-EIDOS    | Recopilación manual con apoyo de<br>``eidos_webpage_filtering.ipynb``   | Algas - 10<br>Anfibios - 4<br>Aves - 14<br>Cromistas y Bacterias - 3<br>Hongos - 1<br>Invertebrados - 727<br>Mamíferos - 132<br>Peces - 72<br>Plantas no vasculares - 26<br>Plantas vasculares - 770<br>Reptiles - 18   |

Tras recopilar los datos de las diferentes fuentes, se combinaron en un solo archivo Excel que además incluyera el ``idtaxon`` asociado según el criterio de EIDOS. El código empleado para ello se encuentra en el archivo ``description_joiner.ipynb``. Dado que había unas pocas erratas en los nombres de algunas fuentes, se realizó un posterior asignado manual a unas 10 especies utilizando la plataforma de EIDOS. El resultado final es el archivo ``DESCRIPCIONES_TODAS.xlsx`` que se encuentra en esta carpeta.