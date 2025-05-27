# Nombres de Especies 

Esta carpeta contiene la información relacionada con la **identificación de especies**, extraída de la página de **IEPNB-EIDOS**  ([enlace](https://iepnb.gob.es/areas-tematicas/especies-silvestres/eidos)). Estos datos se publican bajo la licencia CC-BY.

Se accede a los nombres comunes proporcionados por **EIDOS** a través de la API para obtener esta información utilizando el siguiente cuaderno:

> `api_eidos_nombres.ipynb`

---

## Archivo resultante

El archivo generado con la información es:

> `EIDOS_nombres.xlsx`

Contiene datos de un total de **53.784 especies**, incluyendo:

- **`idtaxon`**: número de identificación único asignado a cada especie.
- **`Nombre_aceptado`**: nombre científico completo (género, especie, autor y año).
- **`Nombre_común`**: nombres comunes asociados, indicando en la columna `espreferente` cuál es el nombre común aceptado para esa especie.
- **`Idioma`**: idioma del nombre común. Puede ser:
  - Castellano
  - Inglés
  - Francés
  - Portugués
  - Italiano
  - Alemán
  - Latín
  - Valenciano
  - Altoaragonés
  - Bable
  - Catalán
  - Euskera
  - Gallego
  - Mallorquín

---

> *Este conjunto de datos permite identificar de forma precisa y en diferentes idiomas las especies*
