# Estado de Conservación de las Especies – README

Esta carpeta contiene la información sobre el **estado de conservación de las especies** según la **UICN**, extraída de la página de **IEPNB-EIDOS**  ([enlace](https://iepnb.gob.es/areas-tematicas/especies-silvestres/eidos)) a través de una API.

El procesamiento se realiza mediante el cuaderno:

> `api_estado_conservacion_eidos.ipynb`

Los datos recopilados sobre el estado de conservación de **3.533 especies** están disponibles en el archivo:

> `EIDOS_estado_conservacion.xlsx`

---

## Categorías de Conservación

Se han establecido 9 categorías de amenaza, basadas en las definidas por la **Lista Roja de Especies Amenazadas de la UICN** (*IUCN Red List of Threatened Species*).

| Abreviatura | Categoría de conservación         | Número de especies |
|-------------|-----------------------------------|---------------------|
| LC          | Preocupación menor                | 279                 |
| VU          | Vulnerable                        | 1132                |
| EN          | En peligro                        | 499                 |
| CR          | En peligro crítico                | 436                 |
| DD          | Datos insuficientes               | 475                 |
| EX          | Extinto                           | 35                  |
| RE          | Extinto regionalmente             | 15                  |
| NT          | Casi amenazado                    | 413                 |
| EW          | Extinto en estado silvestre       | 3                   |
| NE          | No evaluado                       | 244                 |
| -           | Categoría no registrada           | 1                   |
