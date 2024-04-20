import newspaper
import pandas as pd
from google.cloud import bigquery

project_id = 'delta-era-420905'
dataset_id = 'articles'
table_id = 'articles_info'


import newspaper
import pandas as pd
from google.cloud import bigquery

project_id = 'delta-era-420905'
dataset_id = 'articles'
table_id = 'articles_info'

def scrape_articles(urls):
    articles_data = []

    for url in urls:
        paper = newspaper.build(url, language='en', memoize_articles=False)
        print("Number of articles in", url, ":", len(paper.articles))
        for article in paper.articles:
            article.download()
            article.parse()

            if article.text:
                articles_data.append({
                    'url': article.url,
                    'title': article.title,
                    'text': article.text,
                })

    # Convert to Pandas DataFrame
    df = pd.DataFrame(articles_data)

    # Establish BigQuery client
    client = bigquery.Client(project=project_id)

    # Define table reference
    table_ref = client.dataset(dataset_id).table(table_id)

    # Load data into BigQuery
    job_config = bigquery.LoadJobConfig(
        # Specify schema if needed
        # schema=[
        #     bigquery.SchemaField("url", bigquery.enums.SqlTypeNames.STRING),
        #     bigquery.SchemaField("title", bigquery.enums.SqlTypeNames.STRING),
        #     bigquery.SchemaField("text", bigquery.enums.SqlTypeNames.STRING),
        # ],
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND  # Append to existing table
    )
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)

    job.result()  # Wait for the job to complete

    print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))

# Example usage (replace with your actual URLs)
urls = ["http://bbc.com"]
scrape_articles(urls)
