# -*- coding: utf-8 -*-
import json

from scrapy import Spider,Request,FormRequest

from spider_chanlun.items import ChanlunItem,ArticleItem


class ChanlunSpider(Spider):
    name = 'chanlun'
    allowed_domains = ['blog.sina.com.cn']

    def start_requests(self):
        url = 'http://blog.sina.com.cn/s/articlelist_1215172700_10_11.html'
        yield Request(url = url, callback=self.parse_index)

    def parse_index(self,response):
        articles = response.css('.articleList .articleCell')[::-1]  #列表倒序
        for article in articles:
            title = article.css('.atc_title a::text').extract_first()
            href = article.css('.atc_title a::attr(href)').extract_first()
            if '股市闲谈' in title or '教你炒股票' in title:
                item = ChanlunItem()
                yield Request(url = href, callback= self.parse_articles, meta={'item':item}) #通过meta传递item

        previous_page = response.css('.SG_pages .SG_pgprev a::attr(href)').extract_first() #上一页
        if previous_page:
            yield Request(url = previous_page, callback=self.parse_index,dont_filter=True)

    def parse_articles(self, response):
        item = response.meta['item']
        title = response.css('.articalTitle .titName::text').extract_first()
        time = response.css('.time::text').extract_first()
        tags = ' '.join(response.css('#sina_keyword_ad_area .blog_tag  h3 a::text').extract())
        category = response.css('#sina_keyword_ad_area .blog_class a::text').extract_first()
        content = response.css('#sina_keyword_ad_area2').extract_first()
        item['title'] = title
        item['time'] = time
        item['tags'] = tags
        item['category'] = category
        item['content'] = content

        #about api info
        artical_url = response.url
        aids = artical_url[-11:-5]
        api_url = 'http://comet.blog.sina.com.cn/api?maintype=num&uid=486e105c&aids={}'.format(aids)  # api
        yield Request(url=api_url, callback=self.parse_api, meta={'item': item})

    '''
        get [readers,context, collects, transponds] infos
    '''
    def parse_api(self, response):
        item = response.meta['item']
        content = response.text[36:-3]
        artical_info = json.loads(content)
        likes = artical_info['d']
        readers = artical_info['r']
        comments = artical_info['c']
        collects = artical_info['f']
        transponds = artical_info['z']
        item['likes'] = likes
        item['readers'] = readers
        item['comments'] = comments
        item['collects'] = collects
        item['transponds'] = transponds
        yield item