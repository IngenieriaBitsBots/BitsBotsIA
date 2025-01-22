import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Recuperar las credenciales de Azure desde las variables de entorno
speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")

# Verificar si las variables están correctamente cargadas
if not speech_key or not speech_region:
    raise ValueError("Las credenciales de Azure Speech no están configuradas correctamente.")

# Configurar Speech SDK con las credenciales
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
speech_config.speech_recognition_language="es-CO"
speech_config.speech_synthesis_voice_name = "es-CO-GonzaloNeural"


# speech_config.set_property(
#     property_id=speechsdk.PropertyId.SpeechServiceConnection_SingleLanguageIdPriority, 
#     value="Telephone"
# )


def transcribe_audio():
    """Reconoce el habla y devuelve el texto transcrito."""
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,audio_config=audio_config)
    print("Habla ahora...")
    result = speech_recognizer.recognize_once_async().get()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Usuario dijo: {result.text}")
        return result.text
    else:
        print("No se reconoció nada.")
        return None

def synthesize_speech(text):
    try:
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        speech_synthesizer.voice_name = "es-CO-GonzaloNeural"  # O cualquier otra voz optimizada
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
