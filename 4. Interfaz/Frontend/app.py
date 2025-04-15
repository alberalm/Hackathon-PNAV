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



if __name__ == '__main__':
    app.run(debug=True)
