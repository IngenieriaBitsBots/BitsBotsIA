# from openai import AzureOpenAI
# import os
# import json
 
# def generate_response(user_input, current_state, body_part=None):

#     if current_state == "COLLECTING_SYMPTOMS":
#         if body_part:
#             prompt = f"El usuario ha mencionado los siguientes síntomas en la parte del cuerpo {body_part}: {user_input}. ¿Hay algún otro síntoma relacionado con esa parte del cuerpo?"
#         else:
#             prompt = f"El usuario ha mencionado los siguientes síntomas: {user_input}. ¿Puedes indicar en qué parte del cuerpo se encuentran estos síntomas?"
    
#     elif current_state == "ANALYZING_SYMPTOMS":
#         prompt = f"El usuario ha reportado los siguientes síntomas: {user_input}. ¿Son síntomas graves, moderados o leves? Proporciona recomendaciones basadas en estos síntomas, hazlo como si hablaras de tu a tu con la persona."
    
#     elif current_state == "RECOMMENDING":
#         prompt = f"Basado en los síntomas reportados por el usuario: {user_input}, ¿qué recomendación médica le darías? en caso de que sean sintomas que tu consideres muy graves podrías indicarle que se dirija por urgencias a su ips sura, si son sintomas leves puedes darle algunas recomendaciones basicas"
#     else:
#         prompt = f"Usuario: {user_input}. Bot:"


#     """Genera una respuesta usando OpenAI."""
#     client = AzureOpenAI(
#         api_version=os.getenv("OPENAI_API_VERSION"),
#         azure_endpoint=os.getenv("OPENAI_API_BASE"),
#         api_key=os.getenv("OPENAI_API_KEY")
#     )

#     response = client.chat.completions.create(
#         model="gpt-35-turbo",
#         messages=[
#             {"role": "system", "content": "Eres un asistente útil y amable."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=150,
#         temperature=0.6
#     )

#     # Procesar la respuesta
#     response_dict = json.loads(response.to_json())
#     assistant_message = response_dict["choices"][0]["message"]["content"]

#     return assistant_message

from openai import AzureOpenAI
import os
import json

class OpenAIClient:
    def __init__(self):
        """Inicializa el cliente de OpenAI con las configuraciones desde las variables de entorno."""
        # openai.api_type = "azure"
        # openai.api_version = os.getenv("OPENAI_API_VERSION")
        # openai.api_base = os.getenv("OPENAI_API_BASE")
        # openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_response(self, user_input, current_state, body_part=None):
        """Genera una respuesta de OpenAI basada en el estado y el input del usuario."""
        try:
            # Construir el prompt según el estado
            prompt = self._build_prompt(user_input, current_state, body_part)

            client = AzureOpenAI(
                api_version=os.getenv("OPENAI_API_VERSION"),
                azure_endpoint=os.getenv("OPENAI_API_BASE"),
                api_key=os.getenv("OPENAI_API_KEY")
            )

            response = client.chat.completions.create(
                model="gpt-35-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente útil, amable y habla de tu a tu con los pacientes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.6
            )

            # Procesar la respuesta
            response_dict = json.loads(response.to_json())
            assistant_message = response_dict["choices"][0]["message"]["content"]

            return assistant_message

        except Exception as e:
            print(f"Error al generar respuesta de OpenAI: {e}")
            return "Lo siento, hubo un problema técnico al generar una respuesta."

    def _build_prompt(self, user_input, current_state, body_part):
        """Construye el prompt para OpenAI según el estado."""
        if current_state == "COLLECTING_SYMPTOMS":
            if body_part:
                return f"El usuario ha mencionado los siguientes síntomas en la parte del cuerpo {body_part}: {user_input}. ¿Hay algún otro síntoma relacionado con esa parte del cuerpo?"
            return f"El usuario ha mencionado los siguientes síntomas: {user_input}. ¿Puedes indicar en qué parte del cuerpo se encuentran estos síntomas?"

        elif current_state == "ANALYZING_SYMPTOMS":
            return f"El usuario ha reportado los siguientes síntomas: {user_input}. ¿Son síntomas graves, moderados o leves? Proporciona recomendaciones basadas en estos síntomas, hazlo como si hablaras de tú a tú con la persona."

        elif current_state == "RECOMMENDING":
            return f"Basado en los síntomas reportados por el usuario: {user_input}, ¿qué recomendación médica le darías? En caso de que sean síntomas graves, indícale que se dirija a urgencias en su IPS. Si son síntomas leves, da recomendaciones básicas."

        return f"Usuario: {user_input}. Bot:"
