# README - Base de Datos – Imágenes de Especies

Esta carpeta contiene el **código necesario para descargar y procesar imágenes** de especies (animales, hongos y plantas) desde diversas fuentes que proporcionan descripciones visuales.  
Se han filtrado únicamente aquellas imágenes con **licencias comercializables**, y se ha registrado el **autor** de cada fotografía.

---

## Fuentes utilizadas

Se han empleado las siguientes fuentes para la obtención de imágenes:

| Fuente             | Enlace                                                         | Código empleado                   | Tipo de imágenes obtenidas       |
|--------------------|----------------------------------------------------------------|------------------------------------|----------------------------------|
| iNaturalist        | [inaturalist.org](https://www.inaturalist.org/)               | `inaturalist_media_filter.ipynb`   | Animales, hongos, plantas        |
| Pl@ntNet           | [plantnet.org](https://identify.plantnet.org/es)              | `plantnet_scraper.ipynb`           | Plantas                          |
| Animalia.bio       | [animalia.bio](https://animalia.bio/)                         | Recopilación manual                | Animales                         |
| Wikimedia Commons  | [commons.wikimedia.org](https://commons.wikimedia.org/wiki/) | Recopilación manual                | Animales, hongos, plantas        |

---

## Procesado

- Inicialmente, se descargaron las imágenes de las observaciones de iNaturalist, que se combinaron con el resto de fuentes ya que **~900 especies** no contaban con imágenes (`Especies_Sin_Foto_iNaturalist.xlsx`).
- Tras incluir PlantNet, el número se redujo a **770 especies sin foto** (`Especies_Sin_Foto_iNaturalist_Plantnet.xlsx`).
- Tras todas las búsquedas combinadas, finalmente quedaron **888 especies sin imagen** disponibles (`Especies_Sin_Foto_final.xlsx`).
- Para evitar duplicados, se utilizó el cuaderno `images_table_creator.ipynb`.

---

## Imágenes obtenidas por grupo taxonómico

| Grupo taxonómico         | Especies con foto |
|--------------------------|-------------------|
| Algas                    | 7                 |
| Hongos                   | 379               |
| Plantas no vasculares    | 16                |
| Plantas vasculares       | 406               |
| Invertebrados            | 147               |
| Aves                     | 613               |
| Mamíferos                | 130               |
| Reptiles                 | 86                |
| Anfibios                 | 33                |
| Peces                    | 68                |

---

> *Este conjunto de imágenes servirá para ilustrar las especies en la guía pdf 
