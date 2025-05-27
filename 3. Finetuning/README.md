Esta carpeta contiene todos los scripts y resultados para la generación y uso de los datasets empleados para el finetuning de los modelos.

Dado que el proyecto hace uso de técnicas de Text2SQL para poder extraer información de la base de datos construida en `2. Base de datos`, así como otro modelo de lenguaje para poder personalizar las descripciones de las especies de acuerdo a las preferencias de los usuarios, se crearon dos conjuntos de datos:

- En primer lugar, un conjunto que contiene diferentes prompts que simulan lo que el usuario puede introducir en la aplicación, así como la consulta SQL que se debe generar a partir de ellos, generadas por Google Gemini y revisadas manualmente. Estas consultas tienen un valor que actúa como plantilla mediante la cadena de texto `<idtaxon>`, que después se reemplaza por el valor correspondiente a cada especie. Cada uno de los prompts se reescribió de tres maneras diferentes para aumentar la generalidad de los modelos durante el entrenamiento.
- En segundo lugar, se usaron las consultas junto con el conjunto de espcies de la base de datos con el fin de utilizar la información recabada de la base de datos para modificar ligeramente las descripciones. Para ello, se dividieron tanto los prompts como las especies en dos conjuntos, uno de entrenamiento y otro de validación. A continuación, se utilizó *few-shot prompting* a partir de ejemplos construidos manualmente para cada prompt diferente, de modo que Google Gemini produjera mejores resultados. Por cada especie y prompt, se generaron tres descripciones alternativas, una por cada descripción presente en la tabla `Descripciones`, y cada una se insertó una vez por cada reescritura del prompt, de modo que se generaron un total de nueve ejemplos por cada par `(prompt, idtaxon)`. Los resultados de las consultas se incluyen en formato JSON, que es entendido fácilmente por máquinas.

La siguiente tabla resume el número de ejemplos presentes en cada dataset. Los cuadernos utilizados están disponibles en la carpeta `Datasets generation`, y los ejemplos manuales para crear ambos conjuntos se pueden encontrar en el archivo Excel `PROMPTS.xlsx`, dentro de esa misma carpeta.

| Dataset      | Cuaderno utilizado | Ejemplos creados  | Seleccionados para entrenamiento | Seleccionados para validación |
|--------------|---|-------------------|---------------|----------- |
| Text2SQL     | `Text2SQL_dataset_generator.ipynb`  | 51 prompts $\times$ 3 reescrituras | 133 | 20  |
| Descripciones | `Description_Dataset_Generator.ipynb` `dataset_pruning.ipynb` | 51 prompts $\times$ 50 especies por prompt $\times$ 9 reescrituras por ejemplo  | 20154 | 279 |

Una vez generados los datasets, se procedió al entrenamiento de los modelos. Dado que el dataset generado de descripciones era demasiado grande y el contexto excesivamente largo en ocasiones, se realizaron algunas modificaciones:

- Se limitó la búsqueda de resultados mediante las consultas SQL a 30 resultados por consulta (`SELECT TOP 30`).
- Se creó una versión reducida del dataset con 3300 ejemplos de entrenamiento y 63 ejemplos de validación.

Los datasets se guardaron en los archivos `Text2SQL_Data.xlsx` para el de Text2SQL y en los archivos `description_train_dataset.json` y `description_test_dataset.json`, junto con `mini_description_train_dataset.json` y `mini_description_test_dataset.json` para las versiones reducidas.

Dado que no se tenía acceso a GPUs, se procedió al entrenamiento mediante CPUs, seleccionando la más potente disponible en Azure, con 64 núcleos y más de 450 GB de RAM. En total, se realizaron tres entrenamientos mediante fine-tunings, todos con posterior evaluación manual en varios puntos del entrenamiento. En concreto:

- Primero, el modelo [Salamandra-2b-instruct](https://huggingface.co/BSC-LT/salamandra-2b-instruct) fue entrenado mediante fine-tuning completo con el dataset para Text2SQL por un total de 15 epoch, un batch size de 8, learning rate de 0.00005 y weight decay de 0.001, generándose ejemplos con el conjunto de validación tras cada epoch. Los métodos exactos se encuentran en el cuaderno `2b_finetune_text2sql.ipynb` de la carpeta `Finetuning scripts`.

- Después, dado que el modelo anterior no había proporcionado resultados satisfactorios, se realizó un proceso similar con el modelo [Salamandra-7b-instruct](https://huggingface.co/BSC-LT/salamandra-7b-instruct), que fue entrenado mediante LoRA con el dataset para Text2SQL con los mismos hiperparámetros que su contraparte 2b. De nuevo, las técnicas exactos se encuentran en el cuaderno `7b_finetune_text2sql.ipynb` de la carpeta `Finetuning scripts`.

- Finalmente, se entrenó el modelo [Salamandra-7b-instruct](https://huggingface.co/BSC-LT/salamandra-7b-instruct) mediante LoRA con el dataset de descripciones. En este caso, se entrenó por un solo epoch con un batch size de 16, un learning rate de 0.0001 y un weight decay de 0.001, generando ejemplos con el conjunto de validación tras cada 20 pasos (de un total de 207). Una vez más, el script entero se encuentra en el cuaderno `7b_finetune_descriptions.ipynb` de la carpeta `Finetuning scripts`.

Los resultados de estos entrenamientos pueden accederse en sendas carpetas dentro de `Finetuning scripts`. Su posterior evaluación manual reveló que el mejor modelo obtenido para Text2SQL es la versión de 7b tras 6 epoch, mientras que el mejor modelo para generar descripciones nuevas se obtiene tras 140 pasos. Tras esto, se combinaron los adaptadores de estas versiones con el modelo base mediante el script del cuaderno `model_merger.ipynb` en la carpeta `Modelos`. Finalmente, se cuantizaron estos modelos adaptados mediante la herramienta [GGUF my Repo](https://huggingface.co/spaces/ggml-org/gguf-my-repo), con cuantización Q8_0.

Todos los modelos mencionados son accesibles a través de Huggingface como repositorios públicos:

| Modelo | Adaptadores | Modelo combinado | Versión cuantizada |
|---|---|---|---|
| 7b-text2SQL | [Enlace](https://huggingface.co/alberalm/salamandra-7b-instruct-text2sql-adapters) | [Enlace](https://huggingface.co/alberalm/salamandra-7b-instruct-text2sql) | [Enlace](https://huggingface.co/alberalm/salamandra-7b-instruct-text2sql-Q8_0-GGUF) |
| 7b-descripciones | [Enlace](https://huggingface.co/alberalm/salamandra-7b-instruct-description-adapters) | [Enlace](https://huggingface.co/alberalm/salamandra-7b-instruct-description) | [Enlace](https://huggingface.co/alberalm/salamandra-7b-instruct-description-Q8_0-GGUF) |