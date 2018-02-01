# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re

class BbctechSpider(scrapy.Spider):
    name = 'bbctech'
    #allowed_domains = ['http:\\www.baidu.com']
    start_urls = ['http://www.bbc.com/news/technology']

    def parse(self, response):     #找头条
        bbc_st = response.text
        bbc_st_soup = BeautifulSoup(bbc_st, 'lxml')
        txt_1 = bbc_st_soup.body.find('div',{'class':"container"}).find('a').get("href")
        url = 'http://www.bbc.com/' + txt_1
        yield scrapy.Request(url, callback=self.parseAgain)

    def parseAgain(self, response):    #找文章
        bbc_f = response.text
        bbc_soup = BeautifulSoup(bbc_f, 'lxml')
        essay = bbc_soup.head.title.string + '\n'     #标题
        for i in bbc_soup.body.find('p',{"class":"story-body__introduction"}).previous_sibling.next_siblings:
            if i.name in ['h1','h2']:
                essay += '\n'
                essay = self.findText(essay,i)
            elif i.name == 'p':
                essay = self.findText(essay, i)
            elif i.name == 'hr':
                if i.next_sibling.name in ['h1','h2']:
                    essay += '\n'
                    essay = self.findText(essay, i)
                else:
                    break
            else:
                continue
        essay = self.checkText(essay)
        with open('bbctech.txt', 'w',encoding='utf-8',errors='ignore') as f:
            f.write(essay)
        self.log('Saved file bbctech.')

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

    def checkText(self,in_text):
        out_text = ''
        li = in_text.split('\n')
        for i in range(len(li)):
            if li[i][-1] not in '.,?!\"':#句末无此符号可视为标题
                li.insert(i,'\n')#插入换行符
                if not li[i+1]:#若为最后一行且标题样式
                    li.pop(i)#删除此行
            out_text += li[i]
        return out_text