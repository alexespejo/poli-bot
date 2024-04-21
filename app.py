from flask import Flask, request
import time
from poliBot import poli_bot
from ratelimit import limits, sleep_and_retry
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@sleep_and_retry
@limits(calls=1, period=1)
def poli_bot_with_rate_limit(context_input):
    time.sleep(3)  # Simulate processing time
    return poli_bot(context_input)

@app.route('/')
def index():
    return 'Hello, World!'  

@app.route('/prompt_gemini', methods=['POST'])
# Assuming a rate limit of 1 request per second with a burst of 5 requests
@sleep_and_retry
@limits(calls=1, period=1)
def endpoint():
    try:
        data = request.json["context"] # Get the JSON data from the request body
        print(data)
        time.sleep(3)
        summary = poli_bot_with_rate_limit(data)# Call the poli_bot function with the context from the JSON data
        return summary # Return the text field from the JSON data
    except (KeyError, TypeError) as e:
        print(e, "error")
        return 'Error' 

# @app.route("/conversation", methods=["POST"])
# def conversation():
#     try :
#         data = request.json
#         content = data["context"] 
#         print(content)
#         return "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Porro voluptates maiores doloremque, hic tempore est recusandae dolores consequuntur eligendi odio. Aperiam quos maiores ullam inventore cupiditate. Fuga dignissimos incidunt, magni repellendus velit hic ex pariatur a, quos nemo vitae sapiente!"
#     
#     except (KeyError, TypeError) as e:
#         print(e, "error")
#         return "error"