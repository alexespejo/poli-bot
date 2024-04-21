import os
import google.generativeai as genai
from dotenv import load_dotenv
from api import summarize, generate_articles, fact_check
import time
import urllib3
from google.api_core import retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# pip install --upgrade google-api-python-client
# pip install python-dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

POLI_BOT_PROMPT = """
    You are a political analyst tasked with helping a reader understand the implications of a political statement.
    If the user asks for a summary, use the provided 'summarize' function to generate a concise overview.
    If the user wants to learn more about a particular political statement, use the 'generate_articles' function to provide relevant articles.
    
    * Maintain neutrality and objectivity. 
    * Offer balanced perspectives and analysis.
    * Deliver a concise summary in under 200 characters.
    * Use clear language, avoiding emotional bias.
    * Focus on clarity and relevance for easy comprehension.
    * Analyze the political development and its potential impacts.
    * Aim to empower informed decision-making without promoting any specific agenda.
    * Consider how this development affects the person asking the question and the broader political landscape.
"""

def poli_bot(user_input):
  model_name = 'gemini-1.5-pro-latest'
  model = genai.GenerativeModel(model_name, tools=[summarize, generate_articles, fact_check], system_instruction=POLI_BOT_PROMPT)
  convo = model.start_chat(enable_automatic_function_calling=True)
  # convo = model.generate_content()

  # print('Welcome to the Political Analysis Tool!\n')

  while True:
    user_input = input('> You: ')
    if user_input.lower() == 'exit':
      break
    try:
      response = convo.send_message(user_input)
      print(f"\nPolitical Analyst: {response.text}\n")
    except:
      print('Our servers are currently busy. Please try again later. :(')
    
  print('\nThank you for using the Political Analysis Tool!')
  return response.text

if __name__ == '__main__':
  poli_bot()