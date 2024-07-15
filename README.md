**\* About the project**

## Inspiration

The inspiration behind this project was the growing concern over election misinformation, fueled by clickbait media and AI-generated content, which can spread false narratives and undermine the integrity of the electoral process, especially with the upcoming 2024 presidential election.

## What it does

PoliAI is a tool designed to combat misinformation by summarizing and generating content related to political topics, while also incorporating fact-checking capabilities. This empowers users to access reliable information and encourages critical thinking.

## How we built it

We utilized various technologies to develop PoliAI:

1. **BigQuery**: We leveraged BigQuery to store and query a database of relevant political articles and information.
2. **Frontend**: The user interface was built using React and Tailwind CSS, providing an interactive and visually appealing experience.
3. **Backend**: Flask was used to handle the backend logic and integrate with the AI models.
4. **AI Models**: We integrated with the Google Studio API and the Gemini 1.5 Pro model from Anthropic to enable long context understanding and generate accurate political statements based on recent information.
5. **Chrome Extension**: Additionally, we developed a Chrome extension to enhance the accessibility and convenience of PoliAI for users.

## Challenges we ran into

During the development process, we faced challenges in familiarizing ourselves with the Google Studio API and understanding the intricacies of building a Chrome extension. These hurdles required dedicated research and effort to overcome.

## Accomplishments that we're proud of

We are proud to have created a tool that empowers users to engage with political information critically and promotes informed decision-making. PoliAI provides a platform for users to access reliable information and encourages critical thinking, which is vital in combating misinformation and fostering a well-informed electorate.

## What we learned

Throughout the development of PoliAI, we gained valuable experience in building interactive tools for users. Additionally, we became proficient in prompt engineering with Gemini, enabling us to create a political agent capable of generating accurate statements based on recent political information.

## What's next for PoliAI

Moving forward, we plan to continue enhancing PoliAI by regularly web scraping and adding recent political articles to the database. This will ensure that the tool remains up-to-date and relevant. Furthermore, we aim to improve the fact-checking function, enabling it to generate more cohesive arguments and leverage strong evidence to back up its responses to users.
