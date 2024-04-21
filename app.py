from flask import Flask, request
from poliBot import poli_bot
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello, World!'  

@app.route('/prompt_gemini', methods=['POST'])
def endpoint():
    try:
        data = request.json["context"] # Get the JSON data from the request body
        print(data)
        summary = poli_bot(data) # Call the poli_bot function with the context from the JSON data
        return summary # Return the text field from the JSON data
    except (KeyError, TypeError) as e:
        print(e, "error")
        return 'Error' 

