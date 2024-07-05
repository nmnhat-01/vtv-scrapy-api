import scrapy
from ..items import NewsItem
from datetime import datetime
import os


class VtvSpider(scrapy.Spider):
    name = "vtvspider"
    allowed_domains = ["vtv.vn"]
    start_urls = ["https://vtv.vn/the-gioi.htm"]

    # base URL
    base_url = 'https://vtv.vn'

    # url list to be scraped
    news_url_list = []

    def parse(self, response):
        # noibat news
        self.news_url_list.append(self.base_url + response.css('#noibatmuc .focus_left a::attr(href)').get())
        self.news_url_list.append(self.base_url + response.css('#noibatmuc .focus_left p.tlq a::attr(href)').get())

        # noibat_cate
        self.news_url_list.append(self.base_url + response.css('#noibatmuc .focus_right li.big a::attr(href)').get())

        # noibat_cate small li
        noibat_cate_right_news = response.css("#noibatmuc .focus_right li.small")

        for item in noibat_cate_right_news:
            self.news_url_list.append(self.base_url + item.css("h4 a::attr(href)").get())

        # slider
        noibat24h_news = response.xpath('//ul[@class="swiper-wrapper"]/li[@class="swiper-slide"]/h3/a/@href').extract()

        for item in noibat24h_news:
            self.news_url_list.append(self.base_url + item)

        # left news
        timeline_left_news = response.css(".list_news.timeline li.tlitem a::attr(href)")

        for item in timeline_left_news:
            self.news_url_list.append(self.base_url + item.root)

        # right news
        timeline_right_news = (response.css(".right .tieudiem li a::attr(href)") +
                               response.css(".right .cat_right_small li a::attr(href)"))

        for item in timeline_right_news:
            self.news_url_list.append(self.base_url + item.root)

        # self.logger.debug(f"news_url_list: %s", self.news_url_list)
        self.news_url_list = [url for url in self.news_url_list if "vtv8" not in url]
        news_unique_urls = set(self.news_url_list)

        # clean link
        news_unique_urls.remove("https://vtv.vn/the-gioi.htm")

        self.logger.debug(f"news_unique_urls: %s", news_unique_urls)

        for url in news_unique_urls:
            yield response.follow(url=url, callback=self.parse_news_detail)

    def parse_news_detail(self, response):
        news_item = NewsItem()

        url_split_array = ((response.url.replace(self.base_url, "").split("/")[2]).split(".")[0]).split("-")

        # self.logger.debug("url_split_array: %s", url_split_array)
        news_item['original_id'] = url_split_array[len(url_split_array)-1]
        news_item['original_url'] = response.url
        news_item['title'] = response.css("h1.title_detail::text").get()
        news_item['author'] = response.css("p.author::text").get()
        news_item['avatar'] = response.css("img.news-avatar::attr(src)").get()
        news_item['avatar_desc'] = response.css(".avatar-desc::text").get()
        news_item['sapo'] = response.css("h2.sapo::text").get()

        entry_body_nodes = response.xpath("//div[@id='entry-body']/node()").extract()
        clean_content = ""

        for node in entry_body_nodes:
            if "RelatedNews" not in node and "admzonelfu0vpwi" not in node and "VTVGo" not in node:
                clean_content += node

        news_item['content'] = clean_content.strip()
        news_item['scraped_time'] = datetime.now()

        yield news_item
