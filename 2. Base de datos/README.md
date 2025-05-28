Esta carpeta contiene las tablas con las que se ha poblado la base de datos. Estas se pueden obtener a partir de los datos recopilados en el paso previo, con las siguientes modificaciones:

- Se eliminaron manualmente especies cuyas descripciones eran demasiado cortas y carecían de información suficiente.
- Se filtraron las especies para las que existían ubicaciones y buenas descripciones de todas las tablas.
- Se eliminaron columnas innecesarias.

Para el segundo punto, véanse el archivo ``consistency_checker.ipynb`` y la carpeta ``Filtrado descripciones``.

Otros datos, como los archivos ``.shp`` que describían el recorrido de las rutas, no se tienen en cuenta para la base de datos.

En las carpetas ``Longitudes`` y ``Mapas`` se encuentran los cuadernos que se han empleado para completar la información faltante sobre las rutas para la base de datos.

- **Longitudes:** en esta carpeta se encuentra el cuaderno ``calcular_longitudes.ipynb`` que automatiza el cálculo de las longitudes de las rutas mediante la librería ``geopy``. Se extraen las coordenadas de cada ruta y se calcula la longitud midiendo las distancias punto a punto entre ellas, y se guardan en un archivo denominado ``longitudes_rutas.csv``. Este último se combina con la información que ya se tenía de las rutas obteniendo el archivo ``Rutas_longitudes.xlsx``.

- **Mapas:** en esta carpeta se encuentran los cuadernos ``mapa_españa.ipynb`` y ``mapa_por_ruta.ipynb``. El primero de ellos contiene el código necesario para la generar el mapa de España presente en la página web y emplea la librería ``matplotlib`` para insertar los círculos con colores por Comunidad Autonónoma y con tamaño relativo en función al número de rutas que hay en cada una. El segundo cuaderno contiene el código que genera los diferentes mapas por ruta y los sitúa dentro de su provincia correspondiente empleando las coordenadas. Ambos cuadernos utilizan la librería ``contextily`` que permite extraer mapas de sitios como **OpenStreetMap** ([enlace](https://www.openstreetmap.org/#map=6/40.01/-2.49)), de donde se han obtenido en este caso. Los mapas generados son accesibles a través de [este repositorio público](https://huggingface.co/datasets/alberalm/hiking-trails-images-spain).

Finalmente, se ingestaron todas las tablas en una base de datos SQL, tal y como se muestra en el archivo ``ingesta_datos.ipynb``.

La base de datos SQL contiene las siguientes tablas:

- **Cuadriculas:** esta tabla contiene todas las cuadrículas MGRS de 10x10 km pertenecientes al territorio español junto con la provincia y comunidad autónoma correspondientes.

- **CuadriculasEspecies:** esta tabla contiene la ubicación de las distintas especies. Se relaciona el identificador único de cada especie(``idtaxon``) de acuerdo al sistema de referencia de [EIDOS](https://iepnb.gob.es/areas-tematicas/especies-silvestres/eidos) con la cuadrícula MGRS de 10x10 km que indica su ubicación.

- **CuadriculasRutas:** esta tabla contiene la ubicación de las distintas rutas. Se relaciona el identificador único de cada ruta(``ID_Ruta``) con la cuadrícula MGRS de 10x10 km que indica su ubicación.

- **DescripcionesEspecies:** esta tabla contiene diferentes descripciones de cada especie con su identificador único (``idtaxon``), incluyendo la descripción original y tres descripciones adaptadas a un lenguaje sencillo por Google Gemini. Además, cada registro incluye la fuente de donde se ha extraído.

- **Imágenes:** esta tabla contiene las URLs necesarias para la descarga de las imágenes de cada especie con su identificador único (``taxonid``) y el autor/a de la fotografía.

- **NombresEspecies:** esta tabla contiene diferentes nombres comunes para cada especie junto con el idioma en el que están escritos, además de su identificador único (``idtaxon``). La columna ``espreferente`` indica el nombre que se utiliza con más frecuencia cuando es igual a 1, siendo este el que se muestra en la aplicación.

- **Rutas:** esta tabla contiene la información de cada ruta, especificando todas sus etapas, además de la longitud, provincia y comunidad autónoma por las que pasa.

- **Taxonomía:** esta tabla contiene la taxonomía de cada especie. En particular, detalla sus posibles nombres científicos (tanto aceptados como sinónimos), su clasificación taxonómica, su estado de conservación más reciente y su pertenencia al [Catálogo de Especies Exóticas Invasoras](https://www.miteco.gob.es/es/biodiversidad/temas/conservacion-de-especies/especies-exoticas-invasoras/ce-eei-catalogo.html), además de diferenciarlas con su identificador único (``taxonid``).