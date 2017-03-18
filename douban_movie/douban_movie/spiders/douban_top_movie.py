# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.http.request import Request
from douban_movie.items import DoubanMovieItem

class DoubanTopMovieSpider(Spider):
    name = "douban_top_movie"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers = self.headers)

    def parse(self, response):
        item = DoubanMovieItem()
        for movie in response.xpath('//ol[@class="grid_view"]/li'):
            item['rank'] = movie.xpath('.//div[@class="pic"]/em/text()').extract_first()
            item['movie_name'] = movie.xpath('.//div[@class="hd"]/a/span[1]/text()').extract_first()
            item['score'] = movie.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
            item['quote'] = movie.xpath('.//span[@class="inq"]/text()').extract_first()
            yield item

        next_url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_url:
            next_url = 'https://movie.douban.com/top250' +next_url
            yield  Request(next_url, headers=self.headers)


