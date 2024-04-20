import newspaper
from data import urls
cnn_paper = newspaper.build(urls[0])

for article in cnn_paper.articles:
    print(article.url)
