Esta carpeta contiene el código necesario para descargar y procesar los datos de las diferentes fuentes que proporcionan rutas en España. 

En total, se han utilizado X fuentes de datos:

- **Caminos Naturales:** sss

- **Rutas Parques Naturales:** ss

- **Senderos FEDME** ss

- **Vías Verdes:** ss


| Fuente | Código empleado | Descripciones obtenidas |
|----------|----------|----------|
| SEO BirdLife    | ``seo_scraper.ipynb``   | Aves - 611   |
| Fungipedia    | ``fungipedia_scraper.ipynb``   | Hongos - 578   |
| IEET    | ``ieet_scraper.ipynb``<br>``ieet_description_extractor.ipynb``   | Mamíferos - 98<br>Peces - 44   |
| VertebradosIbericos    | Recopilación manual  | Anfibios - 31<br>Aves - 127<br>Mamíferos - 60<br>Peces - 50<br>Reptiles - 84  |
| IEPNB-EIDOS    | Recopilación manual con apoyo de<br>``eidos_webpage_filtering.ipynb``   | Algas - 10<br>Anfibios - 4<br>Aves - 14<br>Cromistas y Bacterias - 3<br>Hongos - 1<br>Invertebrados - 727<br>Mamíferos - 132<br>Peces - 72<br>Plantas no vasculares - 26<br>Plantas vasculares - 770<br>Reptiles - 18   |

Tras recopilar los datos de las diferentes fuentes, se combinaron en un solo archivo ``"archivo_rutas.csv"`` a partir de los archivos ``.shp`` y ``.kml`` de las distintas fuentes.. El código empleado para ello se encuentra en el archivo ``1_código_para_unificar.ipynb``. 
A partir de ahí, se asignó cada ruta a sus cuadrículas correspondientes dentro de la malla de cuadrículas de España ([Miteco IEET Mallas 10x10km
](https://www.miteco.gob.es/es/biodiversidad/temas/inventarios-nacionales/inventario-especies-terrestres/inventario-nacional-de-biodiversidad/bdn-ieet-default.html)), a partir del código en ``2_asignacion_rutas_a_cuadricula.ipynb``, y usando unión espacial.
Una vez asignada cada ruta a una o varias cuadrículas, estas se unieron con información cartográfica de las comunidades autónomas y provincias de España, para poder asignar cada ruta a una o varias de ellas. Se realizó mediante el cuaderno ``3_asignacion_rutas_a_CCAA.ipynb``, y el resultado final se separó en un archivo ``csv`` con rutas por cada comunidad autónoma, incluidas en la carpeta "Rutas_Limpias". Hubo 5 rutas pertenecientes a las Islas Cíes que no habían sido asignadas a ninguna cuadrícula terrestre y por tanto no fueron asignadas a ninguna comunidad - manualmente se añadió la información para estas rutas y se añadieron al archivo de Galicia. El código de este cuaderno también genera como archivo intermedio "mallas_con_ccaa_y_prov.csv" que genera una correspondencia entre los códigos de cuadrícula de las mallas de España con sus correspondientes comunidades autónomas y provincias siempre que correspondan al territorio terrestre.