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


import re, html, unicodedata

def limpiar_texto(texto: str) -> str:
    if not texto:
        return ''
    # 1) NFC mantiene los caracteres compuestos (á, ñ, ü…)
    texto = unicodedata.normalize('NFC', texto)
    # 2) quita etiquetas HTML
    texto = re.sub(r'<[^>]+>', '', texto)
    # 3) convierte entidades (&aacute; → á)
    texto = html.unescape(texto)
    # 4) trim
    return texto.strip()


@app.route('/')
def index():
    return render_template('principal.html.html')


@app.route('/personalizar_descripciones')
def personalizar_descripciones(id_ruta: int, lista_especies: list, prompt: str):
    """
    regenera el pdf personalizando las descripciones a traves del prompt
    """
    return generar_pdf(1, lista_especies)



import random
from flask import request, jsonify

@app.route('/obtener_especies', methods=['POST'])
def obtener_especies():
    data = request.get_json(force=True) or {}
    try:
        id_ruta = int(data.get('id_ruta', 1))
    except (TypeError, ValueError):
        id_ruta = 1

    # 1) Configuración de grupos y cuotas
    ALL_GROUPS = [
      "peces","mamiferos","hongos","plantas_vasculares",
      "plantas_no_vasculares","aves","anfibios","invertebrados","reptiles"
    ]
    QUOTAS = {
      0:(3,3), 1:(3,1), 2:(3,1), 3:(3,1),
      4:(3,1), 5:(3,1), 6:(3,1), 7:(3,1),
      8:(3,1), 9:(3,1)
    }
    raw_filters = data.get('taxonomias', [])
    sel = [g for g in ALL_GROUPS if g in map(str.lower, raw_filters)]
    k = len(sel)
    cuota_sel, cuota_rest = QUOTAS.get(k, QUOTAS[0])

    # 2) Paso 1: obtengo sólo idtaxon, grupo y conteo de ocurrencias
    sql_counts = """
        SELECT
          ce.idtaxon,
          LOWER(t.taxonomicgroup) AS grupo,
          COUNT(*)               AS ocurrencias
        FROM dbo.CuadriculasRutas cr
        JOIN dbo.CuadriculasEspecies ce
          ON cr.CUADRICULA = ce.cuadricula
        JOIN dbo.Taxonomia t
          ON ce.idtaxon = t.taxonid
         AND t.nametype = 'Aceptado'
        WHERE cr.ID_Ruta = ?
        GROUP BY ce.idtaxon, LOWER(t.taxonomicgroup)
    """
    df_counts = pd.read_sql_query(sql_counts, conn, params=[id_ruta])

    # 3) Paso 2: aplico filtros y cuotas en memoria
    if sel:
        df_sel  = df_counts[df_counts['grupo'].isin(sel)]
        df_rest = df_counts[~df_counts['grupo'].isin(sel)]
    else:
        df_sel, df_rest = df_counts.copy(), pd.DataFrame(columns=df_counts.columns)

    selected_ids = []
    grupos_proc = sel if sel else ALL_GROUPS

    for g in grupos_proc:
        sub = df_sel[df_sel['grupo'] == g]
        if not sub.empty:
            selected_ids += sub.nlargest(cuota_sel, 'ocurrencias')['idtaxon'].tolist()

    if sel:
        for g in [g for g in ALL_GROUPS if g not in sel]:
            sub = df_rest[df_rest['grupo'] == g]
            if not sub.empty:
                selected_ids += sub.nlargest(cuota_rest, 'ocurrencias')['idtaxon'].tolist()

    # 4) Paso 3: traigo sólo los detalles para esos idtaxon, incluidas las 3 geminis
    if selected_ids:
        placeholders = ",".join("?" for _ in selected_ids)
        sql_details = f"""
            SELECT
              ce.idtaxon,
              LOWER(t.taxonomicgroup)      AS grupo,
              ne.nombre_comun               AS nombre_comun,
              t.name                        AS nombre_cientifico,
              de.Gemini1,
              de.Gemini2,
              de.Gemini3,
              COUNT(*) OVER (PARTITION BY ce.idtaxon) AS ocurrencias
            FROM dbo.CuadriculasEspecies ce
            JOIN dbo.Taxonomia t
              ON ce.idtaxon = t.taxonid
             AND t.nametype = 'Aceptado'
            LEFT JOIN dbo.NombresEspecies ne
              ON ce.idtaxon = ne.idtaxon
             AND ne.idioma = 'Castellano'
             AND ne.espreferente = 1
            LEFT JOIN dbo.DescripcionesEspecies de
              ON ce.idtaxon = de.idtaxon
            WHERE ce.idtaxon IN ({placeholders})
        """
        df_details = pd.read_sql_query(sql_details, conn, params=selected_ids)

        # 5) Elijo una descripción al azar de Gemini1/2/3
        def pick_random_desc(row):
            opts = [row['Gemini1'], row['Gemini2'], row['Gemini3']]
            valid = [o for o in opts if o]
            return random.choice(valid) if valid else None

        df_details['descripcion'] = df_details.apply(pick_random_desc, axis=1)

        # 6) Limpio el DataFrame final
        df_details = (
            df_details
            .drop(columns=['Gemini1','Gemini2','Gemini3'])
            .drop_duplicates(subset=['idtaxon'])
            .replace({np.nan: None})
        )

        especies = df_details.to_dict(orient='records')
    else:
        especies = []

    return jsonify(especies)




import os
from flask import request, send_file
from fpdf import FPDF
import io
from collections import defaultdict

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    data = request.get_json(force=True)
    nombre   = limpiar_texto(data.get('nombre', 'Sin nombre'))
    duracion = limpiar_texto(data.get('duracion', 'Sin duración'))
    longitud = limpiar_texto(data.get('longitud', 'Sin longitud'))
    especies = data.get('especies') or []

    # Inicio PDF
    pdf = FPDF()
    pdf.add_page()

    # Usamos Arial (core font) que soporta Latin-1
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Ruta seleccionada', ln=True)
    pdf.cell(0, 10, f'Nombre: {nombre}', ln=True)
    pdf.cell(0, 10, f'Duración: {duracion}', ln=True)
    pdf.cell(0, 10, f'Longitud: {longitud}', ln=True)

    if especies:
        for grupo_key, lista in defaultdict(list, 
                  { (esp['grupo'] or 'sin grupo').strip(): [] for esp in especies }
               ).items():
            pass  # esto era un ejemplo; abajo está el bucle real

        # Agrupamos por grupo
        grupos_dict = defaultdict(list)
        for esp in especies:
            key = (esp.get('grupo') or 'sin grupo').strip()
            grupos_dict[key].append(esp)

        # Recorremos cada grupo
        for grupo_key, lista_especies in grupos_dict.items():
            pdf.ln(4)
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, grupo_key.replace('_', ' ').title(), ln=True)

            for esp in lista_especies:
                nc   = limpiar_texto(esp.get('nombre_comun') or '')
                sc   = limpiar_texto(esp.get('nombre_cientifico') or '')
                desc = limpiar_texto(esp.get('descripcion') or '')

                # Nombre común en negrita
                pdf.set_font('Arial', 'B', 12)
                titulo = nc or sc
                pdf.cell(0, 8, f"- {titulo}", ln=True)

                # Científico justo debajo en cursiva
                pdf.set_font('Arial', 'I', 10)
                pdf.cell(5)
                pdf.cell(0, 6, sc, ln=True)

                # Descripción normal
                pdf.set_font('Arial', '', 12)
                pdf.cell(5)
                pdf.multi_cell(0, 6, desc)
                pdf.ln(1)

    # Salida inline con codificación Latin-1
    raw = pdf.output(dest='S').encode('latin-1')
    buf = io.BytesIO(raw)
    buf.seek(0)
    return send_file(buf, mimetype='application/pdf', as_attachment=False)





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
