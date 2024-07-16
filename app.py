from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Get Azure keys from environment variables
AZURE_KEY = os.getenv('AZURE_KEY')
AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT')
AZURE_DEPLOYMENT_NAME = os.getenv('AZURE_DEPLOYMENT_NAME')

def get_azure_response(user_message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {AZURE_KEY}',
    }
    body = {
        'prompt': user_message,
        'max_tokens': 150,
        'temperature': 0.7,
        'top_p': 0.95,
        'frequency_penalty': 0,
        'presence_penalty': 0,
    }
    response = requests.post(f"{AZURE_ENDPOINT}/openai/deployments/{AZURE_DEPLOYMENT_NAME}/completions", headers=headers, json=body)
    if response.status_code == 200:
        return response.json()['choices'][0]['text'].strip()
    else:
        return "Sorry, I couldn't process your request."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response_message = get_azure_response(user_message)
    return jsonify({'response': response_message})

if __name__ == '__main__':
    app.run(debug=True)
