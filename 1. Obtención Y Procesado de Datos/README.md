Esta carpeta contiene el código para obtener y procesar los diferentes conjuntos de datos utilizados en el desarrollo de la solución. Estos se pueden dividir en cinco conjuntos:

- **Descripciones de especies:** 

- **Ubicaciones e imágenes de especies:**

- **Rutas:**

- **Puntos de interés:**

- **Nombres de especies:**

Los conjuntos relacionados con especies se unen las diferentes fuentes a través del ``idtaxon`` utilizado en EIDOS. Para ello, es necesario conocer los diferentes nombres por los que se conoce a una especie y su ``idtaxon`` asociado. Con este fin, se usa la API de EIDOS para obtener el archivo ``EIDOS_taxonomia.xlsx``, que contiene la información necesaria sobre cada especie. El código exacto empleado se puede encontrar en el cuaderno ``api_eidos_taxonomia.ipynb``.

Por otro lado, los conjuntos relacionados con ubicaciones se unen a través de las mallas...