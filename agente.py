import google.generativeai as genai
import json
import requests
GEMINI_API_KEY = "AIzaSyBZ77ly3RuiiJPOzQ-dlWmiXw9KWjrr48I" 

genai.configure(api_key=GEMINI_API_KEY)

# Carga los datos JSON
try:
    with open('bd_local.json', 'r') as f:
        datos_locales = json.load(f)
except FileNotFoundError:
    print("Error: El archivo 'bd_local.json' no se encontró.")
    datos_locales = {}
except json.JSONDecodeError:
    print("Error: No se pudo decodificar el archivo JSON.")
    datos_locales = {}


# Inicializa el modelo de Gemini
gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_gemini_response(prompt):
    """
    Obtiene una respuesta del modelo de Gemini.
    """
    try:
        response = gemini_model.generate_content(f"{prompt}\n\nDatos relevantes del archivo local: {datos_locales}")
        return response.text
    except Exception as e:
        return f"Ocurrió un error con la API de Gemini: {e}"

def get_ollama_response(prompt, model_name):
    """
    Obtiene una respuesta de un modelo de Ollama.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": f"{prompt}\n\nDatos relevantes del archivo local: {datos_locales}",
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP incorrectos
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        return f"Ocurrió un error al comunicarse con Ollama. Asegúrate de que está en ejecución. Error: {e}"

def main():
    """
    Función principal del bucle de conversación del chatbot.
    """
    print("Chatbot de Gemini y Ollama. Escribe 'salir' para terminar.")
    
    # El usuario elige qué modelo usar
    model_choice = input("¿Qué modelo quieres usar? (gemini/ollama): ").lower()
    
    if model_choice == 'ollama':
        ollama_model_name = input("Introduce el nombre del modelo de Ollama a usar (por ejemplo, 'llama2'): ")
        
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == 'salir':
            print("Hasta luego!")
            break
        
        if model_choice == 'gemini':
            response = get_gemini_response(user_input)
        elif model_choice == 'ollama':
            response = get_ollama_response(user_input, ollama_model_name)
        else:
            response = "Elección de modelo no válida. Por favor, reinicia el programa y elige 'gemini' u 'ollama'."
            
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
