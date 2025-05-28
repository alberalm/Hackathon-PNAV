# BioSenda

## Descripción del proyecto

Este repositorio contiene el código, las fuentes de datos y los resultados correspondientes al desarrollo del caso de uso `Creación de itinerarios turísticos sostenibles con información sobre normativa y biodiversidad en la zona`, englobado como parte del [Hackathon 2 del Programa Nacional de Algoritmos Verdes](https://algoritmosverdes.gob.es/es/hackathon/hackathon-energia-hidropredictiva).

BioSenda es una aplicación que permite obtener información sobre rutas de senderismo en España, así como de las posibles especies que se pueden observar durante el recorrido, que aparecen con descripciones adaptadas para utilizar un vocabulario sencillo, así como de imágenes que facilitan su identificación. Además, permite la personalización de las descripciones mediante inteligencia artificial generativa a través de peticiones que los usuarios puedan solicitar.

![](demo.gif)

## Estructura del repositorio

El proyecto se ha desarrollado en varios pasos:

- En primer lugar, se recopilaron descripciones y ubicaciones de especies presentes en el ámbito español a través de diferentes fuentes de datos, así como de las rutas de senderismo que se pueden realizar en cada provincia española. Los detalles de este proceso se encuentran en `1. Obtención Y Procesado de Datos`.
- Posteriormente, se agregaron todos los datos en una base de datos que aunara aquellas especies de las que se disponían tanto de ubicaciones como descripciones, que fueron adaptadas mediante modelos de lenguage a un vocabulario sencillo para que los usuarios sin conocimientos técnicos sean capaces de entender e identificar las especies durante el recorrido de las rutas. La información relativa a este paso se encuentra en `2. Base de datos`, creándose una base de datos relacional para el resto del desarrollo a partir de las tablas generadas.
- A continuación, se crearon conjuntos de datos utilizando un modelo de lenguaje masivo (Google Gemini-Flash-2.0) y se entrenaron modelos específicos para la personalización de descripciones por parte de los usuarios. El proceso para realizar esta personalización consiste en emplear un modelo de lenguage específicamente entrenado para generar una consulta SQL que obtenga los datos relevantes para personalizar la descripción. Los resultados de esta consulta se utilizan junto a las descripciones originales para crear las descripciones adaptadas a través de otro modelo de lenguaje, que trata de realizar la menor cantidad de cambios posible. El proceso de generación de datasets y posteriores entrenamiento y análisis de resultados está ubicado en la carpeta `3. Finetuning`.
- Finalmente, se desarrolló una interfaz que permite el uso y comunicación de todos los elementos de manera sencilla por parte de usuarios sin demasiados conocimientos técnicos. Esta se encuentra en la carpeta `4. Interfaz`.

El proyecto ha sido desarrollado utilizando Microsoft Azure, midiendo a cada paso las emisiones de CO2 generadas. Estas se encuentran detalladas en `5. CodeCarbon`.

## Técnicas de inteligencia artificial empleadas

Durante el desarrollo del proyecto, se han utilizado las siguientes técnicas propias de inteligencia artificial:

- **Text2SQL**: una parte fundamental de la personalización de descripciones consiste en convertir las peticiones de los usuarios en consultas SQL que después se ejecuten.
- **Fine-tuning**: los dos modelos de lenguaje que se utilizan en la solución han sido debidamente entrenados mediante fine-tuning.
- **LoRA (Low-Rank Adaptations)**: dado que el modelo de lenguaje utilizado como base contiene 7 mil millones de parámetros, se utilizó una adaptación LoRA para reducir la carga computacional.
- **Cuantización**: los modelos entrenados se cuantizaron para reducir su tamaño y la carga computacional necesaria para utilizarlos.
- **Destilación**: la creación de datasets se realizó utilizando modelos con un tamaño mucho mayor al de los entrenados, con el fin de que los modelos entrenados aprendieran a imitar su comportamiento, lo que se conoce como destilación.
- **Prompt engineering**: las plantillas utilizadas para automatizar la generación de datos requirieron un cuidadoso diseño y posterior refinamiento con el fin de que la generación por parte de los modelos resultara en descripciones lo más claras, correctas y adecuadas posible.
- **Few-shot prompting**: la generación del conjunto de datos para entrenar los modelos se realizó mediante few-shot prompting, aprovechando ejemplos especialmente creados a mano.

## Modelos de lenguaje utilizados

Los modelos de lenguaje adaptados parten de la familia de modelos Alia. En particular, se hizo uso de los modelos Salamandra, tanto una prueba con el modelo de 2 mil millones de parámetros ([Salamandra-2b-instruct](https://huggingface.co/BSC-LT/salamandra-2b-instruct)) como el de 7 mil millones de parámetros ([Salamandra-7b-instruct](https://huggingface.co/BSC-LT/salamandra-7b-instruct)).

Además, se hizo uso de la API gratuita de Google Gemini para generar descripciones adaptadas de las cuales los modelos Salamandra tuvieron que aprender.

### Modo de empleo

La guía completa para utilizar el programa en un entorno local se encuentra dentro de la carpeta `4. Interfaz`. Para el ejemplo mostrado en la demo, se utiliza [KoboldCpp](https://github.com/LostRuins/koboldcpp) y los modelos adaptados cuantizados, disponibles en [Hugginface](https://huggingface.co/alberalm), así como una base de datos alojada en Microsoft Azure.