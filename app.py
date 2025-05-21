from flask import Flask, render_template, request
from azure.data.tables import TableServiceClient
from datetime import datetime
import random
import uuid
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Azure Table Storage connection
load_dotenv()
connection_string = os.getenv('AZURE_CONNECTION_STRING')
table_name = "HuellaCarbono"

emisiones = {
    'coche': 0.192,
    'moto': 0.12,
    'bus': 0.15,
    'tren': 0.045,
    'avion': 0.255,
    'bicicleta': 0.0,
    'pie': 0.0
}

def guardar_huella(email, resultado):
    service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = service.get_table_client(table_name=table_name)

    entidad = {
        'PartitionKey': email,
        'RowKey': str(uuid.uuid4()),
        'Fecha': datetime.utcnow().isoformat(),
        'Resultado': resultado,
    }

    table_client.create_entity(entity=entidad)

def obtener_vehiculo(transporte, km):

    if transporte == 'coche':
        return km * emisiones.get(transporte, 0)
    elif transporte == 'moto':
        return km * emisiones.get(transporte, 0)
    elif transporte == 'bus':
        return km * emisiones.get(transporte, 0)
    elif transporte == 'tren':
        return km * emisiones.get(transporte, 0)
    elif transporte == 'avion': 
        return km * emisiones.get(transporte, 0)
    elif transporte == 'bicicleta':
        return 0
    elif transporte == 'pie':
        return 0
    else:
        return 0

def recomendacion():
    recomendaciones = [
        "🧼 Usa productos de limpieza ecológicos y biodegradables.",
        "👕 Lava la ropa con agua fría y carga completa para ahorrar energía.",
        "🍽️ No desperdicies comida: planea tus comidas y guarda las sobras.",
        "🚿 Toma duchas más cortas para reducir el consumo de agua.",
        "🌬️ Ventila tu casa en vez de usar aire acondicionado si el clima lo permite.",
        "🛍️ Compra a granel para reducir envases innecesarios.",
        "🐟 Elige pescado de pesca sostenible y evita especies en peligro.",
        "📱 Alarga la vida de tus dispositivos electrónicos con buen mantenimiento.",
        "🌐 Usa motores de búsqueda ecológicos como Ecosia para apoyar reforestación.",
        "🚫 Evita el fast fashion: reutiliza, intercambia o dona ropa que ya no uses.",
        "🕯️ Aprovecha la luz natural al máximo antes de encender luces artificiales.",
        "🏡 Aísla bien tu casa para reducir la necesidad de calefacción o refrigeración.",
        "🪴 Crea un huerto urbano en casa para cultivar tus propias hierbas o verduras."
    ]

    return recomendaciones
    

@app.route('/', methods=['GET', 'POST'])

def index():
    result = None
    recomendacion_azar = random.choice(recomendacion())

    if request.method == "POST":
        result = None
        huella = 0
        try:
            email = request.form['email']
            km = float(request.form['km'])
            transporte = request.form['transporte']

            huella = obtener_vehiculo(transporte, km)
            result = f"Tu huella semanal estimada es de {huella:.2f} kg de Co2"

            guardar_huella(email, huella)

        except ValueError:
            result = "Por favor, ingresa un número válido."

    return render_template('index.html', result=result, recomendacion=recomendacion_azar)

if __name__ == '__main__':
    app.run()