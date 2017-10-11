# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import scrapy
from scrapy.selector import Selector
from scrapy.http import  Request
import urllib,urllib2
import os

from filmcloud.items import FilmcloudItem

url_tem = "https://movie.douban.com/subject/%s/?from=playing_poster"

class DmozSpider(scrapy.Spider):
    name = "movie"
    # allowed_domains = ["movie.douban.com"]
    start_urls = [
        "https://movie.douban.com/cinema/nowplaying/chengdu/"
    ]

    def parse(self, response):
        #//*[@id="nowplaying"]/div[2]/ul
        selector_main = response.selector.xpath('//div[@id="nowplaying"]/div[@class="mod-bd"]/ul[@class="lists"]/li[@class="list-item"]')
        # print selector_main
        for sum_sel in selector_main:
            id_data = sum_sel.xpath('./@id').extract()[0]
            url = url_tem%(id_data)
            print url
            yield Request(callback=self.content_parse,url=url)

    def content_parse(self,response):
        name = response.xpath('//div[@id="content"]/h1/span[1]/text()').extract()[0] #要进行数组判断

        #//*[@id="mainpic"]/a/img
        picture = response.xpath('//div[@id="mainpic"]/a/img/@src').extract()[0]

        if not os.path.exists(os.curdir + "/moive_image/"):
            os.mkdir(os.curdir + "/moive_image/")


        path = os.curdir + "/moive_image/"

        urllib.urlretrieve(picture, path + '%s.jpg'%name)
        picture_name = '%s.jpg'%name

        score = response.xpath('//div[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        if len(score):
            score = score[0]
        else:
            score = 0.0
        #//*[@id="info"]/span[1]/span[2]
        director_a = response.xpath('//div[@id="info"]/span[1]/span[2]/a')

        director = ""
        for dir in director_a:
            director_name = dir.xpath('./text()').extract()
            if len(director_name):
                director_name = director_name[0]
            else:
                director_name = "未获取到"
            director += " %s"%(director_name)

        summary = response.xpath('//div[@id="link-report"]/span/text()').extract()[0]

        item = FilmcloudItem()
        item["name"] = name
        item["score"] = score
        item["director"] = director
        item["summary"] = summary
        item["picture"] = picture_name
        yield item
