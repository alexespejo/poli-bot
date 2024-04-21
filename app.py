from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello, World!'  

@app.route('/summarize_text', methods=['POST'])
def endpoint():
    data = request.json # Get the JSON data from the request body
    try:
        print(data["context"])
        return "Message From Bot " + data["context"] # Return the text field from the JSON data
    except:
        print("No text in the data")
        return 'Error' 

