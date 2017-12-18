# -*- coding: utf-8 -*-
import scrapy
import requests
import os

class ConanSpider(scrapy.Spider):
    name = 'conan'
    start_urls = ['http://gocthugian.com.vn/truyen/t175//']

# GET LINK ALL EPISODES
    def parse(self, response):
        for quote in response.css('.VII'):    
            episode=quote.css('a::attr(href)').extract_first()     
            if episode is not None:
                yield response.follow(episode, callback=self.parse_chapter)   

# GET CHAPTER FROM URL EPISODE
    def parse_chapter(self, response):
        for quote in response.css('table.fe-table a'): 
            yield {
                'chapter': quote.css('::attr(href)').extract_first()                 
            }
            chapter_name=quote.css('::text').extract_first()
            chapter=quote.css('::attr(href)').extract_first()   
            if chapter is not None:              
                yield response.follow(chapter, callback=self.parse_img,meta={'chapter_name': chapter_name}) 
                
# GET IMAGES
    def parse_img(self, response):  
        directory='conan/'+response.meta['chapter_name']
        if not os.path.exists(directory):
            os.makedirs(directory)
        for quote in response.css('.TTCD img'):  
            img=quote.css('::attr(src)').extract_first()
            if img.find('?')!=-1:
                img=img[:img.find('?')]  
            filename=os.path.basename(img)
            filepath=directory+'/'+ filename
            r = requests.get(img)  
            with open(filepath, 'wb') as f:
                f.write(r.content)
