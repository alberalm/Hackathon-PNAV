Esta carpeta contiene el código necesario para descargar y procesar los datos de las diferentes fuentes que proporcionan rutas en España. 

En total, se han utilizado 4 fuentes de datos:

- **Caminos Naturales ([enlace](https://centrodedescargas.cnig.es/CentroDescargas/caminos-naturales)):** Conjuntos de caminos que discurren por infraestructuras de transporte, vías pecuarias, plataformas de ferrocarril, caminos de sirga o caminos tradicionales en desuso, que han sido reutilizados para el uso recreativo del campo. Los datos se descargan directamente desde la página del Instituo Geográfico Nacional (IGN) en formato ``.shp``. Estos datos se publican bajo la licencia CC-BY.

- **Rutas Parques Naturales ([enlace](https://centrodedescargas.cnig.es/CentroDescargas/rutas-parques-nacionales)):** Conjunto de rutas para los Parques Nacionales de Ordesa y Monte Perdido, Caldera de Taburiente, Timanfaya, Teide, Garajonay, Picos de Europa, Aigüestortes i Estany de Sant Maurici, Monfragüe, Sierra de Guadarrama, Cabañeros, Doñana, Islas Atlánticas de Galicia, Sierra Nevada, Tablas de Daimiel, Archipiélago de Cabrera y Sierra de las Nieves. Los datos se descargan directamente de la página del IGN en formato ``.kml``. Estos datos se publican bajo la licencia CC-BY.

- **Senderos FEDME ([enlace](https://centrodedescargas.cnig.es/CentroDescargas/senderos-fedme)):** Conjunto de etapas de los Senderos de Gran Recorrido (GR), de los Senderos de Pequeños Recorrido (PR) y de los Senderos Locales (SL) homologados por la Federación Española de Deportes de Montaña y Escalada (FEDME). Los datos se descargan directamente de la página del IGN en formato ``.shp`` clasificados en esas tres categorías. Estos datos se publican bajo la licencia CC-BY.

- **Vías Verdes ([enlace](https://centrodedescargas.cnig.es/CentroDescargas/vias-verdes)):** Conjunto de etapas aportadas por la Fundación de Ferrocarriles Españoles mediante su Programa Vías Verdes, desarrolladas a partir de líneas de ferrocarril en desuso o que nunca llegaron a prestar servicio por quedar inconclusas las obras de construcción. Estos antiguos trazados ferroviarios se han acondicionado para ser recorridos por cicloturistas y caminantes, y son accesibles para personas con movilidad reducida. Los datos se descargan directamente de la página del IGN en formato ``.shp``. Estos datos se publican bajo la licencia CC-BY.


| Fuente | Rutas obtenidas |
|----------|----------|
| Caminos Naturales    | 762   |
| Rutas Parques Naturales    | 391   |
| Senderos FEDME    | 3433  |
| Vías Verdes    | 140   |

Tras recopilar los datos de las diferentes fuentes, se combinaron en un solo archivo ``archivo_rutas.csv`` a partir de los archivos ``.shp`` y ``.kml`` de las distintas fuentes.. El código empleado para ello se encuentra en el archivo ``1_codigo_para_unificar.ipynb``. 
A partir de ahí, se asignó cada ruta a sus cuadrículas correspondientes dentro de la malla de cuadrículas de España ([Miteco IEET Mallas 10x10km
](https://www.miteco.gob.es/es/biodiversidad/temas/inventarios-nacionales/inventario-especies-terrestres/inventario-nacional-de-biodiversidad/bdn-ieet-default.html)), a partir del código en ``2_asignacion_rutas_a_cuadricula.ipynb``, y usando unión espacial.
Una vez asignada cada ruta a una o varias cuadrículas, estas se unieron con información cartográfica de las comunidades autónomas y provincias de España, para poder asignar cada ruta a una o varias de ellas. Se realizó mediante el cuaderno ``3_asignacion_rutas_a_CCAA.ipynb``, y el resultado final se separó en un archivo ``.csv`` con rutas por cada comunidad autónoma, incluidas en la carpeta "Rutas_Limpias". Hubo 5 rutas pertenecientes a las Islas Cíes que no habían sido asignadas a ninguna cuadrícula terrestre y por tanto no fueron asignadas a ninguna comunidad - manualmente se añadió la información para estas rutas y se añadieron al archivo de Galicia. El código de este cuaderno también genera como archivo intermedio ``mallas_con_ccaa_y_prov.csv`` que genera una correspondencia entre los códigos de cuadrícula de las mallas de España con sus correspondientes comunidades autónomas y provincias siempre que correspondan al territorio terrestre.