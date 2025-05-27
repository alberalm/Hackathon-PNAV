# Estado Legal de las Especies 

Esta carpeta contiene la información sobre las **especies invasoras silvestres en España** según el **Catálogo Español de Especies Exóticas Invasoras (CEEEI)**, extraída de la página de **IEPNB-EIDOS**  ([enlace](https://iepnb.gob.es/areas-tematicas/especies-silvestres/eidos)).

Se accede al estado legal proporcionado por **EIDOS** a través de la API para obtener esta información utilizando el siguiente cuaderno:

> `api_estado_legal_eidos.ipynb`

Los registros sobre el estado legal contenían información de diferentes normativas y catálogos, por lo que se filtraron para obtener únicamente las especies incluidas en el Catálogo Español de Especies Exóticas Invasoras (CEEEI).

## Archivo resultante

El resultado final del procesamiento es el archivo:

> `EIDOS_estado_legal.xlsx`

Este archivo recoge un total de **648 especies** consideradas como **Especies Exóticas Invasoras (EEI)** en España.
