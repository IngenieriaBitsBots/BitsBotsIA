# import msvcrt
# from azure_speech import transcribe_audio, synthesize_speech
# from openai_client import generate_response


# def check_exit_condition(user_input):
#     """
#     Revisa si el usuario ha dicho 'chao' o 'adiós' para salir del flujo.
#     También verifica si el usuario presiona cualquier tecla para salir.
#     """
#     # Condición de salida por voz (si el usuario dice 'chao' o 'adiós')
#     if "chao" in user_input.lower() or "adiós" in user_input.lower() or "adios" in user_input.lower():
#         return True
#     return False

# state = "START"
# body_part = None  # Parte del cuerpo que se está consultando (ej. cabeza, pecho, etc.)

# def main():
#     global state, body_part

#     welcome_message = "Hola, has entrado al sistema de autotriaje de sura y estoy aquí para ayudarte. ¿Cuáles son tus síntomas?"
#     print(f"Bot: {welcome_message}")
#     synthesize_speech(welcome_message)
#     state = "COLLECTING_SYMPTOMS"  # Avanzamos directamente al siguiente estado

#     while True:
#         user_input = transcribe_audio()  # Transcripción del audio del usuario
        
#         if user_input:
#             # Verificar si el usuario quiere salir
#             if check_exit_condition(user_input):
#                 response = "¡Adiós! Espero haberte ayudado. ¡Cuídate!"
#                 print(f"Bot: {response}")
#                 synthesize_speech(response)
#                 break  # Salir del bucle y terminar el programa

#             if state == "START":
#                 response = "Hola, has entrado al sistema de autotriaje de SURA. ¿Me podrías indicar en pocas palabras cual es la zona del malestar?"
#                 synthesize_speech(response)
#                 state = "COLLECTING_SYMPTOMS"

#             elif state == "COLLECTING_SYMPTOMS":
#                 # Si el usuario menciona una parte del cuerpo, se asigna esa parte para preguntar sobre los síntomas
#                 if "cabeza" in user_input.lower():
#                     body_part = "cabeza"
#                     response = generate_response(user_input, current_state="COLLECTING_SYMPTOMS", body_part=body_part)
#                     synthesize_speech(response)

#                 elif "pecho" in user_input.lower():
#                     body_part = "pecho"
#                     response = generate_response(user_input, current_state="COLLECTING_SYMPTOMS", body_part=body_part)
#                     synthesize_speech(response)

#                 elif "abdomen" in user_input.lower():
#                     body_part = "abdomen"
#                     response = generate_response(user_input, current_state="COLLECTING_SYMPTOMS", body_part=body_part)
#                     synthesize_speech(response)

#                 elif "pierna" in user_input.lower() or "brazo" in user_input.lower():
#                     body_part = "extremidades"
#                     response = generate_response(user_input, current_state="COLLECTING_SYMPTOMS", body_part=body_part)
#                     synthesize_speech(response)

#                 else:
#                     response = "Lo siento, no pude entender qué parte del cuerpo mencionaste. ¿Podrías ser más específico?"
#                     synthesize_speech(response)
#                     continue  # Preguntar nuevamente si no se entiende

#                 state = "ANALYZING_SYMPTOMS"

#             elif state == "ANALYZING_SYMPTOMS":
#                 response = generate_response(user_input, current_state="ANALYZING_SYMPTOMS")
#                 synthesize_speech(response)

#                 if "dificultad para respirar" in user_input.lower():
#                     response = "Este es un síntoma grave. Por favor, busca atención médica inmediata."
#                     synthesize_speech(response)
#                     break  # Salir del flujo si es grave

#                 else:
#                     response = "¿Te gustaría recibir alguna recomendación para aliviar tus síntomas?"
#                     synthesize_speech(response)
#                     state = "RECOMMENDING"

#             elif state == "RECOMMENDING":
#                 response = generate_response(user_input, current_state="RECOMMENDING")
#                 synthesize_speech(response)
#                 break  # Finaliza la conversación

#         # Verificación de salida por teclado (permitiendo cualquier tecla para salir)
#         print("\nPresiona cualquier tecla para salir en cualquier momento...")
#         if msvcrt.kbhit():  # Espera una tecla sin bloquear la ejecución
#             msvcrt.getch()  # Captura la tecla presionada
#             response = "¡Adiós! Espero haberte ayudado. ¡Cuídate!"
#             print(f"Bot: {response}")
#             synthesize_speech(response)
#             break  # Salir del bucle y terminar el programa

# if __name__ == "__main__":
#     main()

# import time
# from azure_speech import transcribe_audio, synthesize_speech
# from openai_client import generate_response

# def check_exit_condition(user_input):
#     """Revisa si el usuario ha dicho 'chao' o 'adiós' para salir del flujo."""
#     return any(word in user_input.lower() for word in ["chao", "adiós", "adios"])

# state = "START"
# body_part = None  # Parte del cuerpo que se está consultando

# def main():
#     global state, body_part

#     # Mensaje de bienvenida inicial
#     welcome_message = "Hola, has entrado al sistema de autotriaje de SURA. ¿Cuáles son tus síntomas?"
#     synthesize_speech(welcome_message)
#     print(f"Bot: {welcome_message}")
#     state = "COLLECTING_SYMPTOMS"  # Avanzamos directamente al siguiente estado

#     while True:
#         # Escuchar al usuario
#         user_input = transcribe_audio()
        
#         if user_input:
#             # Verificar si el usuario quiere salir
#             if check_exit_condition(user_input):
#                 goodbye_message = "¡Adiós! Espero haberte ayudado. ¡Cuídate!"
#                 synthesize_speech(goodbye_message)
#                 print(f"Bot: {goodbye_message}")
#                 break  # Finalizar flujo

#             if state == "START":
#                 response = "¿Puedes indicarme en qué parte del cuerpo sientes el malestar?"
#                 synthesize_speech(response)
#                 state = "COLLECTING_SYMPTOMS"

#             elif state == "COLLECTING_SYMPTOMS":
#                 body_part = classify_body_part(user_input)
#                 if body_part:
#                     response = generate_response(user_input, current_state="COLLECTING_SYMPTOMS", body_part=body_part)
#                 else:
#                     response = "Lo siento, no entendí qué parte del cuerpo mencionaste. ¿Puedes repetirlo?"
#                 synthesize_speech(response)
#                 state = "ANALYZING_SYMPTOMS" if body_part else "COLLECTING_SYMPTOMS"

#             elif state == "ANALYZING_SYMPTOMS":
#                 response = generate_response(user_input, current_state="ANALYZING_SYMPTOMS")
#                 synthesize_speech(response)

#                 if "dificultad para respirar" in user_input.lower():
#                     emergency_message = "Este es un síntoma grave. Por favor, busca atención médica inmediata."
#                     synthesize_speech(emergency_message)
#                     break  # Salir del flujo si es grave
#                 else:
#                     followup_message = "¿Quieres que te recomiende algo para aliviar tus síntomas?"
#                     synthesize_speech(followup_message)
#                     state = "RECOMMENDING"

#             elif state == "RECOMMENDING":
#                 response = generate_response(user_input, current_state="RECOMMENDING")
#                 synthesize_speech(response)
#                 break  # Finalizar conversación

#         else:
#             # Manejar pausas largas
#             synthesize_speech("¿Sigues ahí? Si necesitas más tiempo, solo háblame.")
#             time.sleep(5)  # Dar tiempo para responder

#     print("Conversación terminada.")

# def classify_body_part(user_input):
#     """Clasifica las partes del cuerpo mencionadas por el usuario."""
#     if "cabeza" in user_input.lower():
#         return "cabeza"
#     elif "pecho" in user_input.lower():
#         return "pecho"
#     elif "abdomen" in user_input.lower():
#         return "abdomen"
#     elif "pierna" in user_input.lower() or "brazo" in user_input.lower():
#         return "extremidades"
#     return None  # No se identificó una parte del cuerpo

# if __name__ == "__main__":
#     main()

# import time
# from azure_speech import AzureSpeech
# from openai_client import OpenAIClient
# from state_manager import BotStateManager

# def check_exit_condition(user_input):
#     """Revisa si el usuario ha dicho 'chao' o 'adiós' para salir del flujo."""
#     return any(word in user_input.lower() for word in ["chao", "adiós", "adios"])

# def classify_body_part(user_input):
#     """Clasifica las partes del cuerpo mencionadas por el usuario."""
#     if "cabeza" in user_input.lower():
#         return "cabeza"
#     elif "pecho" in user_input.lower():
#         return "pecho"
#     elif "abdomen" in user_input.lower():
#         return "abdomen"
#     elif "pierna" in user_input.lower() or "brazo" in user_input.lower():
#         return "extremidades"
#     return None  # No se identificó una parte del cuerpo

# def main():
#     # Inicializar las clases
#     azure_speech = AzureSpeech()
#     openai_client = OpenAIClient()
#     bot_state = BotStateManager()

#     # Mensaje de bienvenida inicial
#     welcome_message = "Hola, has entrado al sistema de autotriaje de SURA. ¿Cuáles son tus síntomas?"
#     azure_speech.synthesize_speech(welcome_message)
#     print(f"Bot: {welcome_message}")
#     bot_state.set_state("COLLECTING_SYMPTOMS")  # Cambiar estado inicial

#     while True:
#         try:
#             # Escuchar al usuario
#             user_input = azure_speech.transcribe_audio()

#             if not user_input:
#                 azure_speech.synthesize_speech("No entendí lo que dijiste. Por favor, repítelo.")
#                 continue

#             # Verificar si el usuario quiere salir
#             if check_exit_condition(user_input):
#                 goodbye_message = "¡Adiós! Espero haberte ayudado. ¡Cuídate!"
#                 azure_speech.synthesize_speech(goodbye_message)
#                 break

#             current_state = bot_state.get_state()

#             if current_state == "COLLECTING_SYMPTOMS":
#                 body_part = classify_body_part(user_input)
#                 if body_part:
#                     bot_state.set_body_part(body_part)
#                     response = openai_client.generate_response(user_input, current_state, body_part)
#                     bot_state.set_state("ANALYZING_SYMPTOMS")
#                 else:
#                     response = "No entendí qué parte del cuerpo mencionaste. ¿Puedes repetirlo?"
#                 azure_speech.synthesize_speech(response)

#             elif current_state == "ANALYZING_SYMPTOMS":
#                 response = openai_client.generate_response(user_input, current_state)
#                 azure_speech.synthesize_speech(response)
#                 bot_state.set_state("RECOMMENDING")

#             elif current_state == "RECOMMENDING":
#                 response = openai_client.generate_response(user_input, current_state)
#                 azure_speech.synthesize_speech(response)
#                 bot_state.reset()
#                 break

#         except Exception as e:
#             print(f"Error en el flujo principal: {e}")
#             azure_speech.synthesize_speech("Hubo un problema técnico. Por favor, intenta más tarde.")
#             break

#     print("Conversación terminada.")

# if __name__ == "__main__":
#     main()

import time
from aiohttp import web
from azure_speech import AzureSpeech
from openai_client import OpenAIClient
from state_manager import BotStateManager

def check_exit_condition(user_input):
    """Revisa si el usuario ha dicho 'chao' o 'adiós' para salir del flujo."""
    return any(word in user_input.lower() for word in ["chao", "adiós", "adios"])

def classify_body_part(user_input):
    """Clasifica las partes del cuerpo mencionadas por el usuario."""
    if "cabeza" in user_input.lower():
        return "cabeza"
    elif "pecho" in user_input.lower():
        return "pecho"
    elif "abdomen" in user_input.lower():
        return "abdomen"
    elif "pierna" in user_input.lower() or "brazo" in user_input.lower():
        return "extremidades"
    return None  # No se identificó una parte del cuerpo

async def handle_call(request):
    """Procesa eventos de llamadas entrantes desde ACS y responde automáticamente."""
    try:
        data = await request.json()
        print("Evento recibido:", data)

        # Manejo del handshake de validación
        if "validationToken" in data:
            print("Solicitud de validación recibida.")
            validation_token = data["validationToken"]
            return web.Response(text=validation_token, status=200)

        # Procesar eventos normales de llamadas entrantes
        if data.get("type") == "incomingCall":
            print("Nueva llamada entrante.")

            # Respuesta automatizada
            response_text = "Hola, gracias por llamar. Este es un sistema automatizado de triaje médico. Por favor menciona tus síntomas."
            azure_speech = AzureSpeech()
            azure_speech.synthesize_speech(response_text)

        return web.Response(status=200)
    except Exception as e:
        print(f"Error procesando la llamada: {e}")
        return web.Response(status=500, text="Error procesando la llamada.")

def main_bot():
    """Flujo principal del bot."""
    # Inicializar las clases
    azure_speech = AzureSpeech()
    openai_client = OpenAIClient()
    bot_state = BotStateManager()

    # Mensaje de bienvenida inicial
    welcome_message = "Hola, has entrado al sistema de autotriaje de SURA. ¿Cuáles son tus síntomas?"
    azure_speech.synthesize_speech(welcome_message)
    print(f"Bot: {welcome_message}")
    bot_state.set_state("COLLECTING_SYMPTOMS")  # Cambiar estado inicial

    while True:
        try:
            # Escuchar al usuario
            user_input = azure_speech.transcribe_audio()

            if not user_input:
                azure_speech.synthesize_speech("No entendí lo que dijiste. Por favor, repítelo.")
                continue

            # Verificar si el usuario quiere salir
            if check_exit_condition(user_input):
                goodbye_message = "¡Adiós! Espero haberte ayudado. ¡Cuídate!"
                azure_speech.synthesize_speech(goodbye_message)
                break

            current_state = bot_state.get_state()

            if current_state == "COLLECTING_SYMPTOMS":
                body_part = classify_body_part(user_input)
                if body_part:
                    bot_state.set_body_part(body_part)
                    response = openai_client.generate_response(user_input, current_state, body_part)
                    bot_state.set_state("ANALYZING_SYMPTOMS")
                else:
                    response = "No entendí qué parte del cuerpo mencionaste. ¿Puedes repetirlo?"
                azure_speech.synthesize_speech(response)

            elif current_state == "ANALYZING_SYMPTOMS":
                response = openai_client.generate_response(user_input, current_state)
                azure_speech.synthesize_speech(response)
                bot_state.set_state("RECOMMENDING")

            elif current_state == "RECOMMENDING":
                response = openai_client.generate_response(user_input, current_state)
                azure_speech.synthesize_speech(response)
                bot_state.reset()
                break

        except Exception as e:
            print(f"Error en el flujo principal: {e}")
            azure_speech.synthesize_speech("Hubo un problema técnico. Por favor, intenta más tarde.")
            break

    print("Conversación terminada.")

if __name__ == "__main__":
    # Configurar el servidor web para manejar eventos de ACS
    app = web.Application()

    # Ruta para llamadas de ACS
    app.router.add_post("/api/calls", handle_call)

    # Iniciar el servidor
    web.run_app(app, host="0.0.0.0", port=8000)