# import azure.cognitiveservices.speech as speechsdk
# import os
# from dotenv import load_dotenv

# # Cargar las variables de entorno
# load_dotenv()

# # Recuperar las credenciales de Azure desde las variables de entorno
# speech_key = os.getenv("AZURE_SPEECH_KEY")
# speech_region = os.getenv("AZURE_SPEECH_REGION")

# # Verificar si las variables están correctamente cargadas
# if not speech_key or not speech_region:
#     raise ValueError("Las credenciales de Azure Speech no están configuradas correctamente.")

# # Configurar Speech SDK con las credenciales
# speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
# speech_config.speech_recognition_language="es-CO"
# speech_config.speech_synthesis_voice_name = "es-CO-GonzaloNeural"



# # def transcribe_audio():
# #     """Reconoce el habla y devuelve el texto transcrito."""
# #     audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
# #     speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,audio_config=audio_config)
# #     print("Habla ahora...")
# #     result = speech_recognizer.recognize_once_async().get()
# #     if result.reason == speechsdk.ResultReason.RecognizedSpeech:
# #         print(f"Usuario dijo: {result.text}")
# #         return result.text
# #     else:
# #         print("No se reconoció nada.")
# #         return None

# # def synthesize_speech(text):
# #     try:
# #         speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
# #         speech_synthesizer.voice_name = "es-CO-GonzaloNeural"  # O cualquier otra voz optimizada
# #         result = speech_synthesizer.speak_text_async(text).get()

# #         if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
# #             print("Respuesta sintetizada correctamente.")
# #         elif result.reason == speechsdk.ResultReason.Canceled:
# #             cancellation_details = result.cancellation_details
# #             print(f"Error: Síntesis cancelada. Razón: {cancellation_details.reason}")
# #             if cancellation_details.error_details:
# #                 print(f"Detalles del error: {cancellation_details.error_details}")
# #         else:
# #             print(f"Error: Resultado inesperado. Razón: {result.reason}")
# #     except Exception as e:
# #         print(f"Excepción durante la síntesis de voz: {e}")

# def transcribe_audio(audio_path):
#     """Transcribe un archivo de audio a texto."""
#     audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
#     speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
#     result = speech_recognizer.recognize_once()

#     if result.reason == speechsdk.ResultReason.RecognizedSpeech:
#         print(f"Transcripción: {result.text}")
#         return result.text
#     elif result.reason == speechsdk.ResultReason.NoMatch:
#         print("No se encontró coincidencia en el audio.")
#         return None
#     else:
#         print(f"Error al transcribir audio: {result.reason}")
#         return None

# def synthesize_speech(text):
#     """Convierte texto en un archivo de audio."""
#     ##audio_config = speechsdk.audio.AudioConfig(filename=output_path)
#     speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
#     result = speech_synthesizer.speak_text_async(text).get()

#     if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#         print("Audio sintetizado correctamente.")
#     else:
#         print(f"Error en la síntesis: {result.reason}")


import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

class AzureSpeech:
    def __init__(self):
        """Inicializa las configuraciones de Azure Speech."""
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")

        if not speech_key or not speech_region:
            raise ValueError("Las credenciales de Azure Speech no están configuradas correctamente.")

        self.speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        self.speech_config.speech_recognition_language = "es-CO"
        self.speech_config.speech_synthesis_voice_name = "es-CO-GonzaloNeural"

    def transcribe_audio(self, audio_path=None):
        """Transcribe un archivo de audio a texto o utiliza el micrófono por defecto."""
        try:
            if audio_path:
                audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
            else:
                audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)
            print("Escuchando...")
            result = speech_recognizer.recognize_once()

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print(f"Transcripción: {result.text}")
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No se encontró coincidencia en el audio.")
                return None
            else:
                print(f"Error al transcribir audio: {result.reason}")
                return None

        except Exception as e:
            print(f"Error al transcribir audio: {e}")
            return None

    def synthesize_speech(self, text, output_path=None):
        """Convierte texto a habla y lo reproduce o lo guarda en un archivo de audio."""
        try:
            # Configuración de salida de audio
            # audio_config = (
            #     speechsdk.audio.AudioConfig(filename=output_path) if output_path else None
            # )

            speech_synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config
            )

            # Síntesis del texto
            result = speech_synthesizer.speak_text_async(text).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                if output_path:
                    print(f"Audio sintetizado y guardado en: {output_path}")
                else:
                    print("Audio sintetizado correctamente.")
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print(f"Error: Síntesis cancelada. Razón: {cancellation_details.reason}")
                if cancellation_details.error_details:
                    print(f"Detalles del error: {cancellation_details.error_details}")
            else:
                print(f"Error al sintetizar audio: {result.reason}")

        except Exception as e:
            print(f"Error al sintetizar audio: {e}")