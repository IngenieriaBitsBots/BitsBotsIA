from openai import AzureOpenAI
import os
import json
 
def generate_response(user_input, current_state, body_part=None):

    if current_state == "COLLECTING_SYMPTOMS":
        if body_part:
            prompt = f"El usuario ha mencionado los siguientes síntomas en la parte del cuerpo {body_part}: {user_input}. ¿Hay algún otro síntoma relacionado con esa parte del cuerpo?"
        else:
            prompt = f"El usuario ha mencionado los siguientes síntomas: {user_input}. ¿Puedes indicar en qué parte del cuerpo se encuentran estos síntomas?"
    
    elif current_state == "ANALYZING_SYMPTOMS":
        prompt = f"El usuario ha reportado los siguientes síntomas: {user_input}. ¿Son síntomas graves, moderados o leves? Proporciona recomendaciones basadas en estos síntomas, hazlo como si hablaras de tu a tu con la persona."
    
    elif current_state == "RECOMMENDING":
        prompt = f"Basado en los síntomas reportados por el usuario: {user_input}, ¿qué recomendación médica le darías? en caso de que sean sintomas graves podrías indicarle que se dirija por urgencias"
    else:
        prompt = f"Usuario: {user_input}. Bot:"


    """Genera una respuesta usando OpenAI."""
    client = AzureOpenAI(
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY")
    )

    response = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente útil y amable."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.6
    )

    # Procesar la respuesta
    response_dict = json.loads(response.to_json())
    assistant_message = response_dict["choices"][0]["message"]["content"]

    return assistant_message
