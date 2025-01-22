from flask import Flask, request, jsonify
from azure_speech import synthesize_speech
from openai_client import generate_response

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_request():
    """
    Endpoint para procesar solicitudes del bot.
    Recibe user_input, current_state y body_part como JSON.
    """
    data = request.json
    user_input = data.get("user_input")
    current_state = data.get("current_state", "START")
    body_part = data.get("body_part", None)

    # Generar respuesta del bot
    response_text = generate_response(user_input, current_state, body_part)

    # Opcional: sintetizar la respuesta en audio si es necesario
    synthesize_speech(response_text)

    return jsonify({"response": response_text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
