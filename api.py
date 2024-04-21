import google.generativeai as genai
from google.cloud import bigquery
import time
from ratelimit import limits, sleep_and_retry
import re

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
    """
    
    context = input
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    prompt = prompt_template.format(system_instructions=system_instructions, context=context)
    response = model.generate_content(prompt)
    return response.text

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
        LIMIT 5
    """

    #print(f"Generated Query: {query}")  # Print the constructed query
    
    # 3. Execute Query and Fetch Results
    client = bigquery.Client(project=project_id)
    query_job = client.query(query)
    results = query_job.result()
    print(f"Number of results: {results.total_rows}")  # Print number of rows returned
    # 4. Process and Return Results
    if results.total_rows > 0:
        print("running this.")
        article_list = []
        for row in results:
            time.sleep(3)
            article_info = f"- {row.title} ({row.url})"
            article_list.append(article_info)
        return article_list
    else:
        return "No closely related articles found."

def fact_check(input: str) -> str:
    """Fact-check a political statement using prompt chaining and database queries."""

    # 1. Initial Answer Generation
    prompt_initial = f"""
    You are a political analyst tasked with providing an objective analysis of the following statement:

    {input}

    Please provide a neutral and informative response.
    """
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    initial_response = model.generate_text(prompt_initial, max_output_tokens=100)

    # 2. Assumption Identification 
    prompt_assumptions = f"""
    Based on your previous response to the statement:

    {initial_response.text}

    What are the key assumptions or premises that underlie your analysis? 
    List them as concise points, one per line. 
    """
    assumptions_response = model.generate_text(prompt_assumptions, max_output_tokens=50)
    assumptions = assumptions_response.text.strip().splitlines()

    # 3. Assumption Verification with Database Queries and Prompt Chaining
    verified_information = []
    for assumption in assumptions:
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
        verification_response = model.generate_text(prompt_verification, max_output_tokens=150)
        verified_information.append(verification_response.text.strip())

    prompt_final = f"""
    ## Fact-Checking Analysis Results

    **Initial Analysis:** {initial_response.text}

    **Verified Information:**
    {'\n'.join(verified_information)}

    **Final Response:**

    Based on the initial analysis and the verification of assumptions, provide a comprehensive and informative assessment of the statement's accuracy. Address any inconsistencies or uncertainties identified during the fact-checking process and present a balanced conclusion. 
    """
    final_response = model.generate_text(prompt_final, max_output_tokens=250)  # Adjust as needed
    return final_response.text
    

    
