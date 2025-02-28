from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# Clave de API de OpenRouter (directamente en el código)
OPENROUTER_API_KEY = "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"

# Cliente de OpenAI configurado para OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    try:
        # Llamada a la API de OpenRouter
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost:5000",  # Opcional: URL de tu sitio
                "X-Title": "Chatbot Python Example",      # Opcional: Nombre de tu sitio
            },
            model="cognitivecomputations/dolphin3.0-mistral-24b:free",
            messages=[
                {"role": "user", "content": user_message},
            ],
        )

        # Extraer la respuesta del modelo
        bot_response = completion.choices[0].message.content
        return jsonify({'message': bot_response})
    except Exception as e:
        print(f"Error al comunicarse con la API: {e}")
        return jsonify({'error': 'Error al procesar la solicitud'}), 500

if __name__ == '__main__':
    app.run(debug=True)
