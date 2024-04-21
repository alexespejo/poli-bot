import newspaper
import pandas as pd
from google.cloud import bigquery

project_id = 'delta-era-420905'
dataset_id = 'articles'
table_id = 'articles_info'
def scrape_articles(urls):
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)

    for url in urls:
        articles_data = []
        paper = newspaper.build(url, language='en')
        print("Number of articles in", url, ":", len(paper.articles))
        for article in paper.articles:
            try:
                article.download()
                article.parse()
                article.nlp()  # Assuming you need NLP processing 

                if article.text:
                    articles_data.append({
                        'url': article.url,
                        'title': article.title,
                        'text': article.text,
                        # Add any other extracted information here (e.g., keywords, summary)
                    })
            except Exception as e:
                print(f"Failed to process article: {article.url} - Error: {e}")
                # Push to BigQuery after processing articles from each URL
        if articles_data:  # Only push if there's data
            df = pd.DataFrame(articles_data)
            job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_APPEND)
            job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
            job.result()
            print(f"Loaded {job.output_rows} rows from {url} into {dataset_id}:{table_id}")
    print("Finished processing all URLs.")


if __name__ == '__main__':
    urls = ['http://www.huffingtonpost.com', 'http://cnn.com', 'http://www.time.com', 'http://www.ted.com', 'http://pandodaily.com', 'http://www.cnbc.com', 'http://www.mlb.com', 'http://www.pcmag.com', 'http://www.foxnews.com', 'http://theatlantic.com', 'http://www.bbc.co.uk', 'http://www.vice.com', 'http://www.elle.com', 'http://www.vh1.com', 'http://espnf1.com', 'http://espn.com', 'http://www.npr.org', 'http://www.sfgate.com', 'http://www.glamour.com', 'http://www.whosdatedwho.com', 'http://kotaku.com', 'http://thebostonchannel.com', 'http://www.suntimes.com', 'http://www.businessinsider.com', 'http://www.rivals.com', 'http://thebusinessjournal.com', 'http://www.newrepublic.com', 'http://allthingsd.com', 'http://www.topgear.com', 'http://thecitizen.com', 'http://www.ign.com', 'http://www.sci-news.com', 'http://www.morningstar.com', 'http://www.variety.com', 'http://medicalxpress.com', 'http://www.news.com.au', 'http://www.health.com', 'http://www.computerandvideogames.com', 'http://wsj.com', 'http://www.allure.com', 'http://www.theinsider.com', 'http://cnet.com', 'http://venturebeat.com', 'http://www.topspeed.com', 'http://thedailyworld.com', 'http://games.com', 'http://www.religionnews.com', 'http://blogs.berkeley.edu', 'http://www.sbnation.com', 'http://www.polygon.com', 'http://nytimes.com', 'http://www.thefrisky.com', 'http://telegram.com', 'http://yahoo.com', 'http://www.nbcnews.com', 'http://thedailypage.com', 'http://www.popsci.com', 'http://www.pbs.org', 'http://www.nasa.gov', 'http://www.guardiannews.com', 'http://www.weather.com', 'http://www.gq.com', 'http://www.etonline.com', 'http://telegraph.co.uk', 'http://www.fastcompany.com', 'http://www.infoworld.com', 'http://www.wired.com', 'http://www.pcgamer.com', 'http://sportingnews.com', 'http://theatlanticwire.com', 'http://thecarconnection.com', 'http://www.sun-sentinel.com', 'http://autoblog.com', 'http://www.environmentalleader.com', 'http://thecrimson.com', 'http://thecypresstimes.com', 'http://www.dailyfinance.com', 'http://www.politico.com', 'http://newsroom.fb.com', 'http://news.ycombinator.com', 'http://lifehacker.com', 'http://www.bet.com', 'http://independent.co.uk', 'http://www.mlssoccer.com', 'http://www.bodybuilding.com', 'http://www.cosmopolitan.com', 'http://www.apple.com', 'http://www.autonews.com', 'http://www.eonline.com', 'http://www.vanityfair.com', 'http://techdigest.tv', 'http://www.maximumpc.com', 'http://www.techradar.com', 'http://thedailyjournal.com', 'http://www.mlive.com', 'http://techworld.com.au', 'http://www.techmeme.com', 'http://thedailynewsegypt.com', 'http://thedailygrind.com.au', 'http://techcrunch.com', 'http://tehrantimes.com', 'http://www.hollywoodreporter.com', 'http://thedailysound.com', 'http://www.stltoday.com', 'http://deadspin.com', 'http://www.digitaltrends.com', 'http://seattletimes.com', 'http://seattlepi.com', 'http://www.cleveland.com', 'http://heritage.org', 'http://www.today.com', 'http://www.politifact.com', 'http://zdnet.com', 'http://www.nationalenquirer.com', 'http://egotastic.com', 'http://blogs.creativeloafing.com', 'http://townhall.com', 'http://www.eweek.com', 'http://www.vogue.co.uk', 'http://www.teenvogue.com', 'http://www.nypost.com', 'http://www.reuters.com', 'http://www.scientificamerican.com', 'http://www.miamiherald.com', 'http://www.nydailynews.com', 'http://www.newscientist.com', 'http://bigstory.ap.org', 'http://www.ebony.com', 'http://thedailystar.com', 'http://www.technologyreview.com', 'http://www.theverge.com', 'http://www.nba.com', 'http://www.cbssports.com', 'http://betabeat.com', 'http://www.tmz.com', 'http://tcnewsnet.com', 'http://www.latimes.com', 'http://www.c-span.org', 'http://www.style.com', 'http://www.peoplestylewatch.com', 'http://theboot.com', 'http://www.foxbusiness.com', 'http://www.pcworld.com', 'http://washingtontimes.com', 'http://thedailyreview.com', 'http://www.nfl.com', 'http://www.space.com', 'http://washingtontechnology.com', 'http://www.buzzfeed.com', 'http://inquirer.net', 'http://www.maxim.com', 'http://abcnews.com', 'http://www.extremetech.com', 'http://thedailytimes.com', 'http://mashable.com', 'http://washingtonexaminer.com', 'http://celebuzz.com', 'http://sciencemag.org', 'http://www.rollingstone.com', 'http://slashdot.org', 'http://www.slate.com', 'http://bleacherreport.com', 'http://www.nascar.com', 'http://www.forbes.com', 'http://washingtonpost.com', 'http://nymag.com', 'http://hbr.org', 'http://www.dailymail.co.uk', 'http://www.theautochannel.com', 'http://www.aljazeera.com', 'http://politicker.com', 'http://nbcsports.nbc.com', 'http://www.gamespot.com', 'http://news.sky.com', 'http://www.joystiq.com', 'http://www.escapistmagazine.com', 'http://www.thestreet.com', 'http://www.ew.com', 'http://www.nj.com', 'http://msn.com', 'http://thedailyreporter.com', 'http://www.economist.com', 'http://phys.org', 'http://www.glam.com', 'http://perezhilton.com', 'http://www.usmagazine.com', 'http://aol.com', 'http://www.cbsnews.com', 'http://www.tennis.com', 'http://washingtonian.com', 'http://www.sciencedaily.com', 'http://foxsports.com', 'http://www.popularmechanics.com', 'http://www.macworld.com', 'http://thinkprogress.org', 'http://www.mtv.com', 'http://discovery.com', 'http://www.people.com', 'http://thedailybeast.com', 'http://www.hollywood.com', 'http://www.engadget.com', 'http://www.usnews.com', 'http://www.billboard.com', 'http://nationalgeographic.com', 'http://thechronicle.com.au', 'http://tbnweekly.com', 'http://techreport.com', 'http://thedailyfix.com', 'http://www.realclearpolitics.com', 'http://usatoday.com', 'http://www.techspot.com', 'http://discovermagazine.com', 'http://arstechnica.com', 'http://foreignpolicy.com', 'http://www.marketwatch.com', 'http://cbn.com', 'http://www.bbcamerica.com', 'http://washingtonindependent.com']
    scrape_articles(urls)
