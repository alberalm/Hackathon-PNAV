from flask import Flask, render_template, send_file
from fpdf import FPDF
import io
from flask import request
import unicodedata

def limpiar_texto(texto):
    return unicodedata.normalize('NFKD', texto).encode('latin-1', 'ignore').decode('latin-1')


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('principal.html.html')

@app.route('/ia')
def pagina_ia():
    return send_file('templates/index_static.html')


@app.route('/generar-pdf', methods=['POST'])
def generar_pdf():
    data = request.get_json()
    nombre = data.get('nombre', 'Sin nombre')
    duracion = data.get('duracion', 'Sin duración')
    longitud = data.get('longitud', 'Sin longitud')
    dificultad = data.get('dificultad', 'Sin dificultad')
    tiempo = data.get('tiempo', 'Sin tiempo')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Ruta seleccionada", ln=True)
    pdf.cell(200, 10, txt=f"Nombre: {nombre}", ln=True)
    pdf.cell(200, 10, txt=f"Duración: {duracion}", ln=True)
    pdf.cell(200, 10, txt=f"Longitud: {longitud}", ln=True)
    pdf.cell(200, 10, txt=f"Dificultad: {dificultad}", ln=True)
    pdf.cell(200, 10, txt=f"Tiempo: {limpiar_texto(tiempo)}", ln=True)



    pdf_output = pdf.output(dest='S').encode('latin-1')
    buffer = io.BytesIO(pdf_output)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="ruta_personalizada.pdf", mimetype='application/pdf')

import requests
from flask import request, jsonify

@app.route('/clima', methods=['POST'])
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
    api_key = "324e25600b1f59ffb8362340f8c8c052"  # ⚠️ Cámbiala después por seguridad

    try:
        url = (
            f'https://api.openweathermap.org/data/3.0/onecall'
            f'?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts'
            f'&appid={api_key}&units=metric&lang=es'
        )
        response = requests.get(url)
        datos = response.json()

        print(">>> RESPUESTA API:", datos)  # <-- Aquí verás si viene 'daily' o un error

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

@app.route('/calidad-aire', methods=['POST'])
def calidad_aire():
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



if __name__ == '__main__':
    app.run(debug=True)
