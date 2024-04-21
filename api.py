import google.generativeai as genai
from google.cloud import bigquery
import time
from ratelimit import limits, sleep_and_retry
import re
from google.api_core import retry

project_id = 'delta-era-420905'
dataset_id = 'articles'
table_id = 'articles_info'

def summarize(input: str) -> str:
    """ Summarize a political statement. """
    
    prompt_template = """
    ## Instructions for Response:

    {system_instructions}

    ## Context:

    {context}

    ## Response:
    """
    
    system_instructions = """
    You are a political analyst tasked with helping a reader understand the implications of a political statement.
    
    * Maintain neutrality and objectivity. 
    * Offer balanced perspectives and analysis.
    * Deliver a concise summary in under 200 characters.
    * Use clear language, avoiding emotional bias.
    * Focus on clarity and relevance for easy comprehension.
    * Analyze the political development and its potential impacts.
    * Aim to empower informed decision-making without promoting any specific agenda.
    * Consider how this development affects the person asking the question and the broader political landscape.
    * Consider the potential political biases that may exist in your response and tell the user what these biases are.
    """
    print('Summarizing')
    try:
        context = input
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        prompt = prompt_template.format(system_instructions=system_instructions, context=context)
        time.sleep(10)
        response = model.generate_content(prompt, request_options={'retry': retry.Retry()})
        return response.text
    except:
        return 'Our servers are currently busy. Please try again later. :('

# Assuming a rate limit of 1 request per second with a burst of 5 requests
@sleep_and_retry
@limits(calls=1, period=1)
def generate_articles(input: str) -> str:
    """Generate top 5 closely-related articles based on a political statement."""
    
    #print(f"Input for query: {input}")  # Print the input string
    
    # 1. Split input into words using regex
    words = re.findall(r"\w+", input.lower())

    # 2. Construct WHERE clause with OR conditions using LIKE
    conditions = " OR ".join([f"TEXT LIKE '%{word}%'" for word in words])
    
    print("conditions: ", conditions)
    query = f"""
        SELECT url, title
        FROM `{project_id}.{dataset_id}.{table_id}`
        WHERE {conditions}
        LIMIT 3
    """

    #print(f"Generated Query: {query}")  # Print the constructed query
    
    # 3. Execute Query and Fetch Results
    client = bigquery.Client(project=project_id)
    query_job = client.query(query)
    results = query_job.result()
    print(f"Number of results: {results.total_rows}")  # Print number of rows returned

    # system_instructions = """
    # You are a political analyst tasked with helping a reader understand the implications of a political statement.
    
    # You are going to get a query from the user first as well as a list of articles in the following format: 'Title (URL): content'. 
    # You will analyze the contents of the articles and determine which articles are relevant to user's query.
    # Then, you will output the relevant articles in the following format: 'Title (URL)'.

    # * Maintain neutrality and objectivity. 
    # * Offer balanced perspectives and analysis.
    # * Use clear language, avoiding emotional bias.
    # * Consider the potential political biases that may exist in your response and tell the user what these biases are.
    # """

    # 4. Process and Return Results
    if results.total_rows > 0:
        print("running this.")
        article_list = []
        for row in results:
            print('me')
            time.sleep(10)
            article_info = f"- {row.title} ({row.url})"
            article_list.append(article_info)
        # Here we query the model
        # context = input
        # model = genai.GenerativeModel('gemini-1.5-pro-latest')
        # prompt = prompt_template.format(system_instructions=system_instructions, context=context)
        # response = model.generate_content(prompt)
        return article_list
    else:
        return "No closely related articles found."

def fact_check(input: str) -> str:
    """Fact-check a political statement using prompt chaining and database queries."""
    
    system_instructions = """
    You are a political analyst tasked with helping a reader understand the implications of a political statement.
    
    * Maintain neutrality and objectivity. 
    * Offer balanced perspectives and analysis.
    * Deliver a concise summary in under 200 characters.
    * Use clear language, avoiding emotional bias.
    * Focus on clarity and relevance for easy comprehension.
    * Analyze the political development and its potential impacts.
    * Aim to empower informed decision-making without promoting any specific agenda.
    * Consider how this development affects the person asking the question and the broader political landscape.
    * Consider the potential political biases that may exist in your response and tell the user what these biases are.
    """
    # 1. Initial Answer Generation
    initial_prompt = f"""
    ## Instructions for Response:

    {system_instructions}

    ## Context:

    {input}

    ## Response:
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        initial_response = model.generate_content(initial_prompt, request_options={'retry': retry.Retry()})
    except:
        return 'Our servers are currently busy. Please try again later. :('
    # 2. Assumption Identification 
    prompt_assumptions = f"""
    Based on your previous response to the statement:

    {initial_response}

    What are the key assumptions or premises that underlie your analysis? 
    List them as concise points, one per line. 
    """
    assumptions_response = model.generate_content(prompt_assumptions, request_options={'retry': retry.Retry()})
    assumptions_list = assumptions_response.text.strip().splitlines()

    # 3. Assumption Verification with Database Queries and Prompt Chaining
    verified_information = []
    for assumption in assumptions_list:
        # 3a. Query Database for Related Information
        related_articles = generate_articles(assumption)  # Assuming you have this function

        # 3b. Construct Prompt for Verification
        prompt_verification = f"""
        ## Assumption Verification

        **Assumption:** {assumption}

        **Related Information from Database:**
        {related_articles} 

        Based on the assumption and the provided information from the database, 
        is the assumption accurate and supported by evidence? 
        Provide a clear explanation of your reasoning, addressing any potential contradictions or inconsistencies.
        """
        verification_response = model.generate_content(prompt_verification, request_options={'retry': retry.Retry()})
        verified_information.append(verification_response.text.strip())

    prompt_final = f"""
    ## Fact-Checking Analysis Results

    **Initial Analysis:** {initial_response.text}

    **Verified Information:**
    {verified_information}

    **Final Response:**

    Based on the initial analysis and the verification of assumptions, provide a comprehensive and informative assessment of the statement's accuracy. Address any inconsistencies or uncertainties identified during the fact-checking process and present a balanced conclusion. 
    """
    time.sleep(10)

    final_response = model.generate_content(prompt_final, request_options={'retry': retry.Retry()})  # Adjust as needed
    return final_response.text
    

    
