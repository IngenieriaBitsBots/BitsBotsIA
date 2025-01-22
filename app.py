from flask import Flask, request, jsonify,send_file
from azure_speech import transcribe_audio, synthesize_speech
from openai_client import generate_response
import os

app = Flask(__name__)

# @app.route("/process", methods=["POST"])
# def process_request():
#     """
#     Endpoint para procesar solicitudes del bot.
#     Recibe user_input, current_state y body_part como JSON.
#     """
#     data = request.json
#     user_input = data.get("user_input")
#     current_state = data.get("current_state", "START")
#     body_part = data.get("body_part", None)

#     # Generar respuesta del bot
#     response_text = generate_response(user_input, current_state, body_part)

#     # Opcional: sintetizar la respuesta en audio si es necesario
#     synthesize_speech(response_text)

#     return jsonify({"response": response_text})


@app.route("/process_audio", methods=["POST"])
def process_audio():
    """
    Endpoint para procesar solicitudes del bot con grabaciones de audio.
    Recibe un archivo de audio, lo transcribe y genera una respuesta.
    """
    if "audio" not in request.files:
        return jsonify({"error": "No se envió un archivo de audio."}), 400

    # Guardar el archivo temporalmente
    audio_file = request.files["audio"]
    file_path = f"/tmp/{audio_file.filename}"
    audio_file.save(file_path)

    try:
        # Transcribir el archivo de audio
        user_input = transcribe_audio(file_path)

        if not user_input:
            return jsonify({"error": "No se pudo transcribir el audio."}), 400

        # Extraer estado y parte del cuerpo (parámetros opcionales)
        current_state = request.form.get("current_state", "START")
        body_part = request.form.get("body_part", None)

        # Generar respuesta del bot
        response_text = generate_response(user_input, current_state, body_part)

        # Sintetizar la respuesta en audio
        response_audio_path = f"/tmp/response_{os.path.basename(file_path)}"
        synthesize_speech(response_text, response_audio_path)

        # Devolver el archivo de audio como respuesta
        return send_file(response_audio_path, as_attachment=True, download_name="response.wav")

    finally:
        # Limpiar archivos temporales
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
