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
    data = request.json # Get the JSON data from the request body
    try:
        print(data["context"])
        summary = poli_bot(data["context"]) # Call the poli_bot function with the context from the JSON data
        return summary # Return the text field from the JSON data
    except:
        print("No text in the data")
        return 'Error' 

