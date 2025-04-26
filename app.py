from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import base64

app = Flask(__name__)
CORS(app)

# Variables de entorno que necesitas configurar en Render
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")  # Ej: whatsapp:+14155238886 (Twilio sandbox o real)
OPERADOR_WHATSAPP_TO = os.getenv("OPERADOR_WHATSAPP_TO")  # Ej: whatsapp:+54911XXXXXXXX

@app.route("/derivar", methods=["POST"])
def derivar():
    try:
        data = request.get_json()

        nombre = data.get("nombre")
        direccion = data.get("direccion")
        localidad = data.get("localidad")
        fecha_nacimiento = data.get("fecha_nacimiento")
        cobertura = data.get("cobertura")
        afiliado = data.get("afiliado")
        telefono_paciente = data.get("telefono_paciente")
        tipo_atencion = data.get("tipo_atencion")
        imagen_base64 = data.get("imagen_base64")

        mensaje_texto = f"""{telefono_paciente}

Hola, tienes una nueva consulta de {nombre} para atenderse en {tipo_atencion}.

Datos del paciente:
- Nombre: {nombre}
- Dirección: {direccion}
- Localidad: {localidad}
- Fecha de nacimiento: {fecha_nacimiento}
- Cobertura: {cobertura}
- Número de afiliado: {afiliado}

Gracias compañero!!!"""

        url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"

        # Primero enviamos el mensaje de texto
        payload_text = {
            'From': TWILIO_WHATSAPP_FROM,
            'To': OPERADOR_WHATSAPP_TO,
            'Body': mensaje_texto
        }
        requests.post(url, data=payload_text, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))

        # Luego enviamos la imagen si existe
        if imagen_base64:
            # En Twilio, para enviar imagen deberías tenerla alojada en una URL pública.
            # Como alternativa temporal podríamos usar Twilio Media Services o directamente otro hosting.
            # Para esta primera versión, mandamos el mensaje de imagen en base64 como futuro paso.

            # O simplemente dejamos preparado para futura implementación de MEDIA_URL.
            pass

        return jsonify({"status": "OK"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def root():
    return "Servicio Derivador activo."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
