from flask import Flask, render_template, send_file
from fpdf import FPDF
import io
import random
import unicodedata
import requests
from flask import request, jsonify

# Definición de especies por ruta
ESPECIES_POR_RUTA = {
    1: [
        {'idtaxon': i, 'nombre': f'Especie {i}'} for i in range(1, 54)
    ],
    2: [
        {'idtaxon': i, 'nombre': f'Especie {i}'} for i in range(1, 54)
    ],
    3: [
        {'idtaxon': i, 'nombre': f'Especie {i}'} for i in range(1, 54)
    ],
}

def limpiar_texto(texto):
    return unicodedata.normalize('NFKD', texto).encode('latin-1', 'ignore').decode('latin-1')


 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('principal.html.html')

@app.route('/personalizar_descripciones')
def personalizar_descripciones(id_ruta: int, lista_especies: list, prompt: str):
    """
    regenera el pdf personalizando las descripciones a traves del prompt
    """
    return generar_pdf(1, lista_especies)

especies_cache = {}

@app.route('/obtener_especies', methods=['POST'])
def obtener_especies():
    """
    Devuelve una muestra de especies según el ID de ruta.
    Para rutas con más de 3 especies (el caso de la ruta 1), selecciona 3 aleatorias la primera vez y las cachea.
    """
    data = request.get_json(force=True)
    try:
        id_ruta = int(data.get('id_ruta', 1))
    except (TypeError, ValueError):
        id_ruta = 1

    especies_list = ESPECIES_POR_RUTA.get(id_ruta, [])
    # Si hay más de 3, muestreamos 3 aleatorias la primera vez
    if len(especies_list) > 3:
        if id_ruta not in especies_cache:
            especies_cache[id_ruta] = random.sample(especies_list, k=3)
        return jsonify(especies_cache[id_ruta])
    # Si no, devolvemos todo el listado
    return jsonify(especies_list)

    
    
   

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    data = request.get_json(force=True)
    nombre   = data.get('nombre', 'Sin nombre')
    duracion = data.get('duracion', 'Sin duración')
    longitud = data.get('longitud', 'Sin longitud')
    especies = data.get('especies')

    # Si no se envían desde el front, recuperamos de cache o completo
    if especies is None:
        try:
            id_ruta = int(data.get('id_ruta', 1))
        except (TypeError, ValueError):
            id_ruta = 1
        especies = especies_cache.get(id_ruta) or ESPECIES_POR_RUTA.get(id_ruta, [])

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.cell(0, 10, 'Ruta seleccionada', ln=True)
    pdf.cell(0, 10, f'Nombre: {nombre}', ln=True)
    pdf.cell(0, 10, f'Duración: {duracion}', ln=True)
    pdf.cell(0, 10, f'Longitud: {longitud}', ln=True)

    if especies:
        pdf.ln(4)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Especies encontradas:', ln=True)
        pdf.set_font('Arial', size=12)
        for esp in especies:
            nombre_esp = esp.get('nombre') or f"ID {esp.get('idtaxon')}"
            pdf.cell(0, 8, f'- {nombre_esp}', ln=True)

    buffer = io.BytesIO(pdf.output(dest='S').encode('latin-1'))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name='ruta_personalizada.pdf',
        mimetype='application/pdf'
    )

# Otros endpoints (clima, calidad de aire, rutas) pueden quedar igual



def obtener_clima():
    data = request.get_json()
    provincia = data.get('provincia')
    fecha = data.get('fecha')

    # Coordenadas por provincia
    coordenadas = {
        'leon': {'lat': 42.5987, 'lon': -5.5671},
        'burgos': {'lat': 42.3439, 'lon': -3.6969}
    }

    if not provincia or provincia not in coordenadas:
        return jsonify({'error': 'Provincia no válida'}), 400

    lat = coordenadas[provincia]['lat']
    lon = coordenadas[provincia]['lon']
    api_key = "324e25600b1f59ffb8362340f8c8c052"  

    try:
        url = (
            f'https://api.openweathermap.org/data/3.0/onecall'
            f'?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts'
            f'&appid={api_key}&units=metric&lang=es'
        )
        response = requests.get(url)
        datos = response.json()

        print(">>> RESPUESTA API:", datos)  

        if 'daily' not in datos:
            return jsonify({'error': 'No se recibió la información esperada de la API'}), 500

        from datetime import datetime
        fecha_consulta = datetime.strptime(fecha, '%Y-%m-%d')
        hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        diferencia = (fecha_consulta - hoy).days

        if diferencia < 0 or diferencia >= len(datos['daily']):
            return jsonify({'error': 'Fecha fuera de rango (0–7 días)'}), 400

        dia = datos['daily'][diferencia]
        descripcion = dia['weather'][0]['description']
        tipo = dia['weather'][0]['main']
        temp = round(dia['temp']['day'])

        return jsonify({
            'descripcion': descripcion,
            'temperatura': temp,
            'tipo': tipo
        })

    except Exception as e:
        return jsonify({'error': f'Error al obtener el clima: {str(e)}'}), 500

def calidad_aire():
    """
    Funcion que se encarga de obtener la calidad del aire en base a las coordenadas 
    """
    datos = request.get_json()
    lat = datos['lat']
    lon = datos['lon']
    
    api_key = "324e25600b1f59ffb8362340f8c8c052"
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

    response = requests.get(url)
    data = response.json()
    print(">>> CALIDAD AIRE:", data)

    if 'list' in data:
        info = data['list'][0]
        return jsonify({
            'aqi': info['main']['aqi'],
            'pm2_5': info['components']['pm2_5'],
            'pm10': info['components']['pm10'],
            'co': info['components']['co']
        })
    else:
        return jsonify({'error': 'No se pudo obtener calidad del aire'}), 500

@app.route('/obtener_rutas', methods=['POST'])
def obtener_rutas(filtros=[]):
    """
    Funcion que se encarga de obtener las rutas en base a los filtros seleccionados por el usuario  
    """
    data = request.get_json()
    provincia = data.get('provincia')

    # Aquí deberías implementar la lógica para obtener las rutas según la provincia
    # Por ejemplo, podrías hacer una consulta a una base de datos o un API externo.
    
    # Simulación de datos de rutas
    rutas = [
        {'ID_Ruta': 1, 'Nombre_Ruta': 'nombre', 'Nombre_Etapa': 'etsapa 1', 'Longitud': '10 km', 'Descripcion': 'Fácil', 'Nombre_Ingles': 'route 1', 'CCAA' : 'murcia', 'Provincia': 'murcia', 'Tiemp': 'sol 12º ,25 aire' },
    ] * 5

    return jsonify(rutas)



if __name__ == '__main__':
    app.run(debug=True)
