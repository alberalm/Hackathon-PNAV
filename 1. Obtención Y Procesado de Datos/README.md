Esta carpeta contiene el código para obtener y procesar los diferentes conjuntos de datos utilizados en el desarrollo de la solución. Estos se pueden dividir en cinco conjuntos:

- **Nombres de especies**: identificación de las especies, incluyendo el nombre científico y común en diferentes idiomas.
- **Descripciones**: recopilación de descripciones de las especies procedentes de diversas fuentes.
- **Estado de conservación**: categorización del nivel de amenaza de las especies según la **UICN**.
- **Estado legal de las especies**: información sobre las especies exóticas invasoras según el **CEEEI**.
- **Ubicaciones y media**: información sobre la localización geográfica de las especies y la obtención de imágenes.
- **Rutas**: conjunto de caminos naturales, rutas, senderos y vías verdes de España.

### Integración de conjuntos relacionados con especies

Los conjuntos relacionados con especies se unen las diferentes fuentes a través del ``idtaxon`` utilizado en EIDOS. Para ello, es necesario conocer los diferentes nombres por los que se conoce a una especie y su ``idtaxon`` asociado. Con este fin, se usa la API de EIDOS para obtener el archivo ``EIDOS_taxonomia.xlsx``, que contiene la información necesaria sobre cada especie. El código exacto empleado se puede encontrar en el cuaderno ``api_eidos_taxonomia.ipynb``.

### Integración de conjuntos relacionados con ubicaciones

Por otro lado, los conjuntos relacionados con ubicaciones se unen a través de **mallas de cuadrículas de España** (proporcionadas por **MITECO IEET**, formato 10x10 km), lo que permite combinar la información geoespacial sobre:

- Presencia de especies
- Rutas y caminos naturales
