Esta carpeta contiene los scripts y resultados para generar la tabla ``DescripcionesEspecies`` que se inserta en la base de datos. La API de ``gemini-2.0-flash``, gratuita hasta 1500 generaciones al día, se utilizó extensivamente.

El objetivo de los scripts es generar tres descripciones simplificadas de cada especie, de forma que actúen como patrón oro y sirvan de datos de entrenamiento para nuestro modelo propio.

Para ello, se parte del archivo ``DESCRIPCIONES_TODAS.xlsx`` y se divide en 3 conjuntos:

- Grupo 1: Especies que tienen más de una descripción (porque aparece en más de una fuente de datos).
- Grupo 2: Especies con una única descripción con menos de 300 caracteres.
- Grupo 3: Especies con una única descripción con longitud igual o superior a 300 caracteres.

300 caracteres se eligió como una buen filtro a partir de las cuales las descripciones originales contenían información suficiente para generar una buena descripción simplificada que ayudara a la identificación de la especie.

Para aquellas especies con una única descripción (grupos 2 y 3), se crearon las tres descripciones mediante la API de Gemini, y aquellas correspondientes a especies del grupo 2 se sometieron a una clasificación manual. El resultado de esta clasificación se encuentra en ``Descripciones_Gemini_Cortas.xlsx``, y el análisis a partir del cual se dedujo que 300 caracteres actuaba bien como corte está disponible en el cuaderno ``short_description_analyser.ipynb``, y las descripciones clasificadas como buenas se unieron a aquellas generadas para las especies del grupo 3 en el archivo ``Descripciones_Gemini_sin_repetir.xlsx``. El cuaderno para usar la API de Gemini y generar descripciones sencillas es ``gemini_description_generator.ipynb``.

Para las especies del grupo 1, se utilizó Gemini para producir una descripción conjunta mediante el código del cuaderno ``gemini_description_combiner.ipynb``, que fue revisada manualmente para evitar pérdidas de información y redundancias. Una vez obtenidas descripciones apropiadas, se generaron las tres descripciones simmplificadas con el mismo método usado para las de los grupos 2 y 3, resultando en el archivo ``Descripciones_Combinadas_Gemini.xlsx``. Finalmente, las descripciones se combinaron con el código del archivo ``description_table_joiner.ipynb``, dando como resultado la tabla ``DescripcionesEspecies``.