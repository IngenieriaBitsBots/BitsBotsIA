import azure.cognitiveservices.speech as speechsdk
#import openai
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Configurar las credenciales de la API
# AzureOpenAI.api_type = "azure"
# AzureOpenAI.api_base = os.getenv("OPENAI_API_BASE")
# AzureOpenAI.api_version = os.getenv("OPENAI_API_VERSION")
# AzureOpenAI.api_key = os.getenv("OPENAI_API_KEY")
speech_config = speechsdk.SpeechConfig(subscription=os.getenv("AZURE_SPEECH_KEY"), region=os.getenv("AZURE_SPEECH_REGION"))
speech_config.speech_synthesis_voice_name = "es-ES-AlvaroNeural"

def transcribe_audio():
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    print("Habla ahora...")
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Usuario dijo: {result.text}")
        return result.text
    else:
        print("No se reconoció nada.")
        return None

def generate_response(prompt):

    client = AzureOpenAI(
    api_version = os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_API_BASE"),
    api_key = os.getenv("OPENAI_API_KEY")

    )
    
    response = client.chat.completions.create(
        model="gpt-35-turbo", 
        messages=[
            {"role": "system", "content": "Eres un asistente útil y amable."},
            {"role": "user", "content": prompt}
        ],
         max_tokens=200
    )

    response_dict = json.loads(response.to_json())
    assistant_message = response_dict["choices"][0]["message"]["content"]

    return assistant_message

def synthesize_speech(text):
    try:
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        result = speech_synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Respuesta sintetizada correctamente.")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Error: Síntesis cancelada. Razón: {cancellation_details.reason}")
            if cancellation_details.error_details:
                print(f"Detalles del error: {cancellation_details.error_details}")
        else:
            print(f"Error: Resultado inesperado. Razón: {result.reason}")
    except Exception as e:
        print(f"Excepción durante la síntesis de voz: {e}")

def main():
    while True:
        user_input = transcribe_audio()
        if user_input:
            response = generate_response(user_input)
            print(f"Bot: {response}")
            synthesize_speech(response)

if __name__ == "__main__":
    main()