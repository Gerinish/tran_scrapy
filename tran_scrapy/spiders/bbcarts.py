# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

class BbcartsSpider(scrapy.Spider):
    name = 'bbcarts'
    #allowed_domains = ['http://www.baidu.com']
    start_urls = ['http://www.bbc.com/news/entertainment_and_arts']

    def parse(self, response):
        bbc_st = response.text
        bbc_st_soup = BeautifulSoup(bbc_st, 'lxml')
        txt_1 = bbc_st_soup.body.find('div', {'class': "container"}).find('a').get("href")
        url = 'http://www.bbc.com/' + txt_1
        yield scrapy.Request(url, callback=self.parseAgain)

    def parseAgain(self,response):
        bbc_f = response.text
        bbc_soup = BeautifulSoup(bbc_f, 'lxml')
        essay = bbc_soup.head.title.string + '\n'  # 标题
        for i in bbc_soup.body.find('div',{"class":"story-body__inner"}).p.previous_sibling.next_siblings:
            if i.name not in ['p']:
                if i.name in ['h1','h2']:
                    essay += '\n'
                    essay = self.findText(essay,i)
                elif i.name in ['ul','li']:
                    essay = self.findTextList(essay,i)
                else:
                    continue
            elif i.name == 'hr':
                if i.next_sibling.name in ['h1','h2']:
                    essay += '\n'
                    essay = self.findText(essay, i)
                else:
                    break
            else:
                essay = self.findText(essay,i)
        with open('bbcarts.txt', 'w',encoding='utf-8',errors='ignore') as f:
            f.write(essay)
        self.log('Saved file bbcarts.')

    def findText(self,in_txt,in_soup):
        try:
            in_txt += '\n' + in_soup
        except:
            for x in in_soup.descendants:
                try:
                    in_txt += x
                except:
                    continue
            in_txt += '\n'
        return in_txt

    def findTextList(self, in_txt, in_soup):
        try:
            in_txt +=  in_soup
        except:
            for x in in_soup.descendants:
                try:
                    in_txt += x
                except:
                    continue
        return in_txt

