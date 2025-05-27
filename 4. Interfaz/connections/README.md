Esta carpeta debería contener archivos que utiliza la aplicación para conectarse a los diferentes servicios. Es necesario crearlos antes de poder ejecutar con éxito la aplicación.

#### 1. Base de datos

La conexión con la base de datos


#### 2. Conexión con modelos para descripciones y Text2SQL

Esta carpeta debería contener un archivo `llm_connection.py` que defina los métodos `async def send_description_prompt(prompt: str) -> str:` y `async def send_text2sql_prompt(prompt: str) -> str:`, que reciben una cadena de texto con el prompt completo y se la envían al modelo que se quiera utilizar. Por ejemplo, si se quieren utilizar los modelos entrenados, pueden usarse instancias de [KoboldCpp](https://github.com/LostRuins/koboldcpp) con las versiones cuantizadas de HuggingFace:

```python
import requests

def send_prompt_kobold(url, prompt, stop_sequence):
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    data = {
        "prompt": prompt,
        "stop_sequence": [stop_sequence]
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json().get("results", [{}])[0].get("text", "")

async def send_description_prompt(prompt: str) -> str:
    return send_prompt_kobold("http://localhost:5001/", prompt, '\n')

async def send_text2sql_prompt(prompt: str) -> str:
    return send_prompt_kobold("http://localhost:5002/", prompt, ';')
```

Alternativamente, se puede utilizar un modelo de OpenAI, Google o Anthropic, entre otros.