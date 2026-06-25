# defining items from the blog to scrape

import scrapy


class tsspost(scrapy.Item):
    post_id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    categories = scrapy.Field()
    tags = scrapy.Field()
    published_date = scrapy.Field()
    text = scrapy.Field()
    date_scraped = scrapy.Field()
    links = scrapy.Field()
