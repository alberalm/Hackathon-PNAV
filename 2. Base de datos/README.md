Esta carpeta contiene las tablas con las que se ha poblado la base de datos. Estas se pueden obtener a partir de los datos recopilados en el paso previo, con las siguientes modificaciones:

- Se eliminaron manualmente especies cuyas descripciones eran demasiado cortas y carecían de información suficiente.
- Se filtraron las especies para las que existían ubicaciones y buenas descripciones de todas las tablas.
- Se eliminaron columnas innecesarias.

Para el segundo punto, véanse el archivo ``consistency_checker.ipynb`` y la carpeta ``Filtrado descripciones``.

Otros datos, como los archivos ``.shp`` que describían el recorrido de las rutas, no se tienen en cuenta para la base de datos.

En las carpetas ``Longitudes`` y ``Mapas`` se encuentran los cuadernos que se han empleado para completar la información faltante sobre las rutas para la base de datos.

- **Longitudes**: en esta carpeta se encuentra el cuaderno ``calcular_longitudes.ipynb`` que automatiza el cálculo de las longitudes de las rutas mediante la librería ``geopy``. Se extraen las coordenadas de cada ruta y se calcula la longitud midiendo las distancias punto a punto entre ellas, y se guardan en un archivo denominado ``longitudes_rutas.csv``. Este último se combina con la información que ya se tenía de las rutas obteniendo el archivo ``Rutas_longitudes.xlsx``.

- **Mapas**: en esta carpeta se encuentran los cuadernos ``mapa_españa.ipynb`` y ``mapa_por_ruta.ipynb``. El primero de ellos contiene el código necesario para la generar el mapa de España presente en la página web y emplea la librería ``matplotlib`` para insertar los círculos con colores por Comunidad Autonónoma y con tamaño relativo en función al número de rutas que hay en cada una. El segundo cuaderno contiene el código que genera los diferentes mapas por ruta y los sitúa dentro de su provincia correspondiente empleando las coordenadas. Ambos cuadernos utilizan la librería ``contextily`` que permite extraer mapas de sitios como **OpenStreetMap** ([enlace](https://www.openstreetmap.org/#map=6/40.01/-2.49)), de donde se han obtenido en este caso. Los mapas generados son accesibles a través de [este repositorio público](https://huggingface.co/datasets/alberalm/hiking-trails-images-spain).

Finalmente, se ingestaron todas las tablas en una base de datos SQL, tal y como se muestra en el archivo ``ingesta_datos.ipynb``.