from flask import Flask, render_template, send_file
from fpdf import FPDF
import io
import random
import unicodedata
import requests
from flask import request, jsonify
import pyodbc
import json
import pandas as pd
from sqlalchemy import create_engine
import urllib
import numpy as np



especies_cache = {}
app = Flask(__name__)
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=tcp:sql-server-mamba.database.windows.net,1433;"
    "DATABASE=sql-db-mamba;"
    "UID=sql-admin;"
    "PWD=serverpwd1!;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)
conn = pyodbc.connect(conn_str)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")

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


@app.route('/')
def index():
    return render_template('principal.html.html')


@app.route('/personalizar_descripciones')
def personalizar_descripciones(id_ruta: int, lista_especies: list, prompt: str):
    """
    regenera el pdf personalizando las descripciones a traves del prompt
    """
    return generar_pdf(1, lista_especies)


import numpy as np

@app.route('/obtener_especies', methods=['POST'])
def obtener_especies():
    """
    Devuelve todas las especies que aparecen en la ruta seleccionada,
    buscando en las cuadrículas asociadas a esa ruta.
    """
    data = request.get_json(force=True)
    # Primero intentamos con el nombre que envía el front (id_ruta),
    # si no llega, con la versión en mayúsculas (ID_Ruta), y si no, 1.
    raw_id = data.get('id_ruta', data.get('ID_Ruta', 1))
    try:
        id_ruta = int(raw_id)
    except (TypeError, ValueError):
        id_ruta = 1

    sql = """
        SELECT DISTINCT
            ce.idtaxon,
            COALESCE(ne.nombre_comun, t.name) AS nombre,
            de.Descripcion AS descripcion
        FROM dbo.CuadriculasRutas cr
        JOIN dbo.CuadriculasEspecies ce
          ON cr.CUADRICULA = ce.cuadricula
        LEFT JOIN dbo.NombresEspecies ne
          ON ce.idtaxon = ne.idtaxon
        LEFT JOIN dbo.DescripcionesEspecies de
          ON ce.idtaxon = de.idtaxon
        LEFT JOIN dbo.Taxonomia t
          ON ce.idtaxon = t.taxonid
        WHERE cr.ID_Ruta = ? AND ne.espreferente = 1
        ORDER BY nombre;
    """

    try:
        df = pd.read_sql_query(sql, conn, params=[id_ruta])
        df = df.replace({np.nan: None})
        especies = df.to_dict(orient='records')
        return jsonify(especies)

    except Exception as e:
        app.logger.exception("Error al obtener especies de la ruta %s", id_ruta)
        return jsonify({'error': 'Error interno al cargar especies'}), 500


@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    data = request.get_json(force=True)

    # limpiamos los datos de la ruta
    nombre   = limpiar_texto(data.get('nombre', 'Sin nombre'))
    duracion = limpiar_texto(data.get('duracion', 'Sin duración'))
    longitud = limpiar_texto(data.get('longitud', 'Sin longitud'))
    especies = data.get('especies')

    # si no vienen desde el front, las obtenemos de la caché o DB
    if especies is None:
        try:
            id_ruta = int(data.get('id_ruta', 1))
        except (TypeError, ValueError):
            id_ruta = 1
        especies = especies_cache.get(id_ruta) or ESPECIES_POR_RUTA.get(id_ruta, [])

    # generación del PDF
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
            # Nombre
            nombre_esp = limpiar_texto(esp.get('nombre') or f"ID {esp.get('idtaxon')}")
            pdf.cell(0, 8, f'- {nombre_esp}', ln=True)
            # Descripción
            desc_raw = esp.get('descripcion') or ''
            descripcion = limpiar_texto(desc_raw)
            # sangramos un poco la descripción
            pdf.cell(5)  # margen izquierdo
            pdf.multi_cell(0, 6, f'{descripcion}')
            pdf.ln(1)   # pequeño espacio antes de la siguiente especie

    # envío del PDF
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


@app.route('/obtener_rutas', methods=['GET'])
def obtener_rutas():
    provincia = request.args.get('provincia', default='', type=str).strip()

    try:
        # 1) Lee TODAS las rutas
        df_rutas = pd.read_sql(
            "SELECT ID_Ruta, Nombre_Ruta, Nombre_Etapa, ROUND(Longitud, 2) AS Longitud, CCAA, Provincia FROM Rutas",
            con=engine  # o conn si sigues con pyodbc
        )
        # 2) Normaliza NaN a None para el JSON
        df_rutas = df_rutas.replace({np.nan: "-"})

        # 3) Si hay filtro de provincia, aplica contains (caso insensible)
        if provincia:
            # Elimina espacios a ambos lados y busca substring
            df_rutas = df_rutas[
                df_rutas['Provincia']
                  .fillna('')
                  .str
                  .contains(provincia, case=False, na=False)
            ]

        rutas = df_rutas.to_dict(orient='records')
        return jsonify(rutas)

    except Exception as e:
        app.logger.exception("Error en obtener_rutas:")
        return jsonify({'error': str(e)}), 500







if __name__ == '__main__':
    app.run(debug=True)
