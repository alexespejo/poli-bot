from flask import Flask, request
from flask_cors import CORS

import os
from dotenv import load_dotenv

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

# may not be necessary
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

app = Flask(__name__)
CORS(app)

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

@app.route('/')
def index():
    return 'Hello, World!'  

@app.route('/summarize_text', methods=['POST'])
def endpoint():
    data = request.json # Get the JSON data from the request body
    try:
        print(data["context"])
        # return "Message From Bot " + data["context"] # Return the text field from the JSON data
        # return to_markdown(response.text)
        # change generate_content for query
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(data['context'])
        return response.text
    except:
        print("No text in the data")
        return 'Error' 

