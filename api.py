import google.generativeai as genai

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
