import scrapy
from litspider.items import LitspiderItem
from urllib.parse import urljoin
class LiteratureSpider(scrapy.Spider):
    name = 'literature'
    allowed_domains = ['labirint.ru']
    start_urls = ['http://labirint.ru/']
    visited_urls = []
    book_urls = []
    def parse(self, response):
        if (response.url not in self.visited_urls and len(self.book_urls) <1000):
            self.visited_urls.append(response.url)
            post_links = response.xpath('//a[contains(@href,"/books/") and not(contains(@class, "videoblock"))]/@href').re('/books/[0-9]*/')
            for post_link in post_links:
                url =  urljoin('http://labirint.ru/',post_link)
                yield response.follow(url, callback=self.parse_post)
            next_pages = response.xpath('//div[contains(@id, "right") or'
             'contains(@id, "left")]//a[not(contains(@href, "#")) and not(contains(@href, "?")) and not(contains(@href, ":"))]/@href').extract()
            for next_page in next_pages:
                next_page_url = urljoin('http://labirint.ru/', next_page)
                yield response.follow(next_page_url, callback=self.parse)
            # next_page = next_pages[-1]
            # next_page_url = urljoin('http://labirint.ru/', next_page)
            # print(next_page_url)
            # yield response.follow(next_page_url, callback=self.parse)
        # yield response.follow(next_page_url, callback=self.parse)
    
    def parse_post(self, response):
        if (response.url not in self.book_urls):
            self.book_urls.append(response.url)
            item = LitspiderItem()
            item['author'] = []
            title = response.xpath('//meta[@name="twitter:title"]/@content').extract()
            item['title'] = title
        # print(title)
            authors = response.xpath('//a[@data-event-label="author"]/@data-event-content').extract()
            if (len(authors)<1):
                authors.append("Нет автора")
            for author in authors:
                item['author'].append(author)
            item['publisher'] = response.xpath('//a[@data-event-label="publisher"]/@data-event-content').extract()
            yield item
