from fpdf import FPDF
import os
from collections import defaultdict

# ----- Variables de ejemplo

nombre_ruta = "Mi Ruta Superguay"
nombre_etapa = "Etapa 23123"
longitud = "32.213 km"
provincia = "Madrid"
CCAA = "Comunidad de Madrid"

especies = [
    {
        "idtaxon": 14070,
        "nombre_aceptado": "Xema sabini (Sabine, 1819)",
        "nombre_comun": "Gaviotón",
        "taxonomicgroup": "Aves",
        "descripcion": "La gaviota de Sabine es una gaviota pequeña con alas largas y vuelo elegante. Es fácil de identificar por su cola ligeramente ahorquillada, algo que no tienen otras gaviotas europeas. En verano, la cabeza del adulto es gris con un collar negro fino que destaca sobre el cuello blanco. En invierno, su cabeza se vuelve más blanca con manchas oscuras. Su cuerpo es blanco por debajo y gris por encima. Lo más llamativo son sus alas: tienen un triángulo blanco en la parte superior que contrasta con el gris del resto del ala y el negro de la punta. Las gaviotas jóvenes tienen un color marrón-grisáceo oscuro en la espalda y la cabeza, pero mantienen el mismo dibujo característico en las alas.",
        "photo_identifier": "https://inaturalist-open-data.s3.amazonaws.com/photos/51996507/original.jpeg",
        "rightsHolder": "Josep Gesti"
    },
    {
        "idtaxon": 10479,
        "nombre_aceptado": "Amandava amandava (Linnaeus, 1758)",
        "nombre_comun": "Bengalí rojo",
        "taxonomicgroup": "Aves",
        "descripcion": "Este charrán es un ave de tamaño mediano, de color pálido. Su espalda y alas son grises claras, con la parte baja de la espalda y la cola blancas, esta última con una forma de horquilla. En verano, los adultos tienen la cabeza negra, pico rojo con la punta negra y patas rojas. En invierno, su frente se vuelve blanca y el pico oscuro. Los jóvenes tienen un tono ocre en la espalda, con marcas marrones y blancas, pico oscuro con la parte inferior naranja y patas naranja pálido. Los jóvenes también tienen una línea oscura en el borde del ala. Una característica útil para identificarlo es que, cuando está posado, la cola no sobresale más allá de las alas. Su vuelo es un poco más pesado en comparación con otros charranes parecidos.",
        "photo_identifier": "https://inaturalist-open-data.s3.amazonaws.com/photos/350341158/original.jpeg",
        "rightsHolder": "Robert Martin"
    },
    {
        "idtaxon": 10708,
        "nombre_aceptado": "Geomalacus anguiformis (Morelet, 1845)",
        "nombre_comun": None,
        "taxonomicgroup": "Invertebrados",
        "descripcion": "Esta babosa mide unos 7 centímetros de largo. Las babosas jóvenes son de color entre negro y azulado, con pequeños bultos blancos y cuatro líneas casi negras en el lomo. Conforme crecen, se aclaran y el azul se vuelve más fuerte, escondiendo los bultos blancos. Las líneas del lomo se hacen más gruesas. Las babosas adultas tienen el lomo marrón, los lados amarillentos y cuatro líneas marrones oscuras, casi negras, en el lomo. La parte inferior del pie es blanquecina, y la baba que produce es amarillenta.",
        "photo_identifier": "https://inaturalist-open-data.s3.amazonaws.com/photos/52000298/original.jpeg",
        "rightsHolder": "Vsevolud Rudyi"
    },
    {
        "idtaxon": 10715,
        "nombre_aceptado": "Plecotus auritus (Linnaeus, 1758)",
        "nombre_comun": "Murciélago orejudo dorado",
        "taxonomicgroup": "Mamífero",
        "descripcion": "Este murciélago es de tamaño mediano y destaca por sus orejas largas y unidas en la base. Dentro de la oreja, tiene una estructura blanquecina y casi transparente. Su pelaje es abundante y largo, de color entre marrón amarillento y marrón grisáceo en la espalda, mientras que en la parte inferior es gris claro con toques amarillentos. Los murciélagos jóvenes tienen un color más pálido y la cara más oscura. Es difícil distinguirlo de otras especies similares a simple vista. Emite sonidos de alta frecuencia mientras busca comida, alcanzando su punto máximo alrededor de 50 kHz.",
        "photo_identifier": "https://inaturalist-open-data.s3.amazonaws.com/photos/286732715/original.jpg",
        "rightsHolder": "Anthony Batista"
    },
    {
        "idtaxon": 10555,
        "nombre_aceptado": "Medusais Cuasi (Morelet, 1234)",
        "nombre_comun": "Organismo medusiforme",
        "taxonomicgroup": "Peces",
        "descripcion": "Este organismo marino parece una pequeña medusa gelatinosa, pero sin aguijón. Mide entre 7 y 12 cm de largo y es transparente. Tiene una forma ovalada y aplanada a los lados. Para comer, usa dos grandes labios que tiene a cada lado de la boca, y debajo de ellos hay otros cuatro más pequeños. Lo más llamativo son las ocho bandas a lo largo de su cuerpo formadas por pequeños peines que brillan con colores del arcoíris durante el día y con un color verde brillante por la noche. Tiene cuatro líneas profundas y fáciles de ver en su cuerpo.",
        "photo_identifier": "https://inaturalist-open-data.s3.amazonaws.com/photos/415605212/original.jpg",
        "rightsHolder": "Diego González Dopico"
    },
    {
        "idtaxon": 10411,
        "nombre_aceptado": "Algus supremus (Linneaeaus, 213)",
        "nombre_comun": None,
        "taxonomicgroup": "Algas",
        "descripcion": "Es un alga pequeña, de color rojo rosado y muy ramificada, que crece formando grupos densos que parecen algodón, llegando a tener hasta 1 cm de grosor. Se fija al suelo marino o a otras algas mediante pequeñas raíces. Sus tallos son delgados y se levantan, creando una forma como de manto. Al final de muchas de sus ramitas se pueden observar unas células especiales con forma de huevo pequeño. El alga en total mide entre 0.5 y 1.5 cm de largo.",
        "photo_identifier": "https://inaturalist-open-data.s3.amazonaws.com/photos/137401599/original.jpeg",
        "rightsHolder": "Sara Navarro"
    }
] * 5


# ------ Código para generar el pdf

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', size=12)
pdf.cell(0, 10, 'Ruta seleccionada', ln=True)
pdf.cell(0, 10, f'Nombre: {nombre_ruta}', ln=True)
pdf.cell(0, 10, f'Longitud: {longitud}', ln=True)

pdf.ln(4)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Especies encontradas:', ln=True)
pdf.set_font('Arial', size=12)

# Agrupar especies por grupo taxonómico
grupos = defaultdict(list)
for especie in especies:
    grupos[especie['taxonomicgroup']].append(especie)

# Añadir especies al PDF, agrupadas por grupo taxonómico
for grupo, lista in grupos.items():
    pdf.ln(4)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'{grupo}:', ln=True)
    pdf.set_font('Arial', size=12)
    for especie in lista:
        texto = f"{especie['nombre_comun']} ({especie['nombre_aceptado']}): {especie['descripcion']}"
        pdf.multi_cell(0, 10, texto)

# ------- Exportar el PDF

# Guardar el PDF en el mismo directorio que el script
salida_path = os.path.join(os.path.dirname(__file__), "salida.pdf")
pdf.output(salida_path)