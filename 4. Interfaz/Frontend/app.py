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
    data = request.get_json(force=True) or {}
    try:
        id_ruta = int(data.get('id_ruta', 1))
    except (TypeError, ValueError):
        id_ruta = 1

    # Todos los grupos disponibles
    ALL_GROUPS = [
      "peces","mamiferos","hongos","plantas_vasculares",
      "plantas_no_vasculares","aves","anfibios","invertebrados","reptiles"
    ]

    # Cuotas según cuántos grupos tengas seleccionados
    QUOTAS = {
      0:(5,5), 1:(15,3), 2:(10,3), 3:(7,3),
      4:(6,3), 5:(7,2), 6:(6,2), 7:(5,2),
      8:(5,1), 9:(5,5)
    }

    # Grupos seleccionados por el usuario
    raw_filters = data.get('taxonomias', [])
    sel = [g for g in ALL_GROUPS if g in map(str.lower, raw_filters)]
    k   = len(sel)
    cuota_sel, cuota_rest = QUOTAS.get(k, QUOTAS[0])

    # 1) Hago la consulta agrupada para contar ocurrencias
    sql = """
               
        SELECT
            ce.idtaxon,
            COUNT(*) AS ocurrencias,
            ne.nombre_comun            AS nombre_comun,
            t.name                     AS nombre_cientifico,
            de.Descripcion             AS descripcion,
            LOWER(t.taxonomicgroup)    AS grupo
        FROM dbo.CuadriculasRutas cr
        JOIN dbo.CuadriculasEspecies ce
          ON cr.CUADRICULA = ce.cuadricula
        LEFT JOIN dbo.NombresEspecies ne
          ON ce.idtaxon = ne.idtaxon
         AND ne.idioma = 'Castellano'
        JOIN dbo.Taxonomia t
          ON ce.idtaxon = t.taxonid
         AND t.nametype = 'Aceptado'      -- <-- Sólo nombres científicos aceptados
        LEFT JOIN dbo.DescripcionesEspecies de
          ON ce.idtaxon = de.idtaxon
        WHERE cr.ID_Ruta = ?
        GROUP BY
            ce.idtaxon,
            ne.nombre_comun,
            t.name,
            de.Descripcion,
            LOWER(t.taxonomicgroup)

    """
    df = pd.read_sql_query(sql, conn, params=[id_ruta])
    df = df.replace({np.nan: None})

    # 2) Parto en dos: seleccionados vs resto (si hay filtros)
    if sel:
        df_sel  = df[df['grupo'].isin(sel)]
        df_rest = df[~df['grupo'].isin(sel)]
    else:
        # ninguno o todos -> tratamos todos como "seleccionados"
        df_sel, df_rest = df.copy(), pd.DataFrame(columns=df.columns)

    # 3) Para cada grupo seleccionado, cojo las top 'cuota_sel'
    muestras = []
    grupos_proc = sel if sel else ALL_GROUPS
    for g in grupos_proc:
        sub = df_sel[df_sel['grupo'] == g]
        if not sub.empty:
            top = sub.nlargest(cuota_sel, 'ocurrencias')
            muestras.append(top)

    # 4) Para cada grupo “restante”, cojo top 'cuota_rest'
    if sel:
        rest_grupos = [g for g in ALL_GROUPS if g not in sel]
        for g in rest_grupos:
            sub = df_rest[df_rest['grupo'] == g]
            if not sub.empty:
                top = sub.nlargest(cuota_rest, 'ocurrencias')
                muestras.append(top)

    # 5) Concateno y devuelvo
    if muestras:
        df_out = pd.concat(muestras, ignore_index=True)
    else:
        df_out = pd.DataFrame(columns=df.columns)

    especies = df_out.to_dict(orient='records')
    return jsonify(especies)






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
    pdf.set_font('Arial', size=12)
    pdf.cell(0, 10, 'Ruta seleccionada', ln=True)
    pdf.cell(0, 10, f'Nombre: {nombre}', ln=True)
    pdf.cell(0, 10, f'Duración: {duracion}', ln=True)
    pdf.cell(0, 10, f'Longitud: {longitud}', ln=True)

        # … dentro de tu función generar_pdf(), en lugar del bloque anterior:
    if especies:
        from collections import defaultdict
        grupos_dict = defaultdict(list)
        for esp in especies:
            grupo_key = (esp.get('grupo') or 'sin grupo').strip()
            grupos_dict[grupo_key].append(esp)

        for grupo_key, lista_especies in grupos_dict.items():
            pdf.ln(4)
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, grupo_key.replace('_', ' ').title(), ln=True)

            for esp in lista_especies:
                nc = limpiar_texto(esp.get('nombre_comun') or '')
                sc = limpiar_texto(esp.get('nombre_cientifico') or '')
                desc = limpiar_texto(esp.get('descripcion') or '')

                # Nombre común en negrita
                pdf.set_font('Arial', 'B', 12)
                if nc:
                    pdf.cell(0, 8, f"- {nc}", ln=True)
                else:
                    # Si no hay común, muestro directamente el científico en negrita
                    pdf.cell(0, 8, f"- {sc}", ln=True)

                # Nombre científico justo debajo, pequeño e itálico
                pdf.set_font('Arial', 'I', 10)
                pdf.cell(5)  # sangría
                pdf.cell(0, 6, sc, ln=True)

                # Volvemos a fuente normal para la descripción
                pdf.set_font('Arial', size=12)
                pdf.cell(5)
                pdf.multi_cell(0, 6, desc)
                pdf.ln(1)


    # Envío del PDF
    buffer = io.BytesIO(pdf.output(dest='S').encode('latin-1'))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name='ruta_personalizada.pdf',
        mimetype='application/pdf'
    )




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
