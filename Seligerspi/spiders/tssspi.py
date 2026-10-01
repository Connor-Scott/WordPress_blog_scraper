# The Story's Stroy blog scraper
# the goal of this project is to take all of the posts made to
# The Story's Story and turn them into a pd dataframe for spacy text annalysis

# find a way to ignore this part "Share this:ShareEmailFacebookRedditTwitterPrintLike this:Like Loading..."

import scrapy
from bs4 import BeautifulSoup
from items import tsspost
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor


class TSSspi(scrapy.Spider):
    name = "TSSspi"
    allowed_domains = ["jakeseliger.com"]
    start_urls = ["https://jakeseliger.com/2023/10/"]

    def parse(self, response):
        # Logic to extract blog post URLs
        archive_link_extractor = LinkExtractor(
            restrict_xpaths='//*[@id="archives-3"]//ul/li'
        )
        links = archive_link_extractor.extract_links(response)
        for link in links:
            yield response.follow(link.url, callback=self.parse_posts)

    def parse_posts(self, response):
        posts = response.xpath("//article")

        for post in posts:
            title_parts = post.css(".entry-title *::text").getall()
            title = " ".join([part.strip() for part in title_parts]).replace(
                "\xa0", " "
            )
            raw_html = post.css(".entry-content").get()
            soup = BeautifulSoup(raw_html, "html.parser")
            links = []
            text = soup.get_text()
            for p in soup.find_all("p"):
                for element in p.children:
                    if element.name == "a":
                        link_text = element.get_text()
                        link_url = element.get("href")
                        links.append({"url": link_url, "text": link_text})
                    else:
                        pass

            item = tsspost(
                date_scraped=datetime.now(),
                post_id=post.xpath("@id").get(),
                categories=post.css(".entry-categories a::text").getall(),
                tags=post.css(".entry-tags a::text").getall(),
                title=title,
                published_date=post.css(".entry-date a::text").get(),
                author=post.css(".author.vcard a::text").getall(),
                text=text,
                links=links,
            )
            yield item
