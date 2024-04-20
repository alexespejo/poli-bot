import newspaper
# from data import urls
# cnn_paper = newspaper.build("http://washingtonindependent.com")
# 
# for article in cnn_paper.articles:
#     print(article.url)

article = newspaper.Article("https://www.cnn.com/politics/live-news/trump-hush-money-trial-04-15-24/index.html")

article.download()
article.parse()

# article text
print(article.text)

# article authors
print(article.authors)

#article publish date
print(article.publish_date)
