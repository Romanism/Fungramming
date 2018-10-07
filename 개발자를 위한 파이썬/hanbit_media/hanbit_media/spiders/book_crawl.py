# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookCrawlSpider(CrawlSpider):
    
    # 크롤러의 이름입니다. 실제 크롤링을 실행할 때 사용합니다.
    name = 'book_crawl'
    
    # 크롤러 실행을 허용할 도메인을 여기서 지정합니다.
    # 해당 서버에서 실행되다가 허용된 도메인 이외는 무시합니다.
    allowed_domains = ['hanbit.co.kr']
    
    # 시작점으로 사용할 URL입니다.
    # 리스트로 지정해 한 번에 여러 웹 페이지에서 크롤링을 시작하게 할 수 있습니다.
    start_urls = ['http://hanbit.co.kr/']

    # 크롤러가 어떻게 작동할지 규칙을 설정합니다.
    # 크롤러는 시작점의 모든 링크를 검사한 후, 규칙에 맞는 링크가 있으면 정해진 콜백 메서드를 실행합니다.
    # follow가 True면 해당 페이지의 링크를 대상으로 재귀적으로 앞 작업을 반복합니다.
    rules = (
        Rule(
            # 크롤링할 링크를 정규 표현식을 이용해서 표현합니다.
            LinkExtractor(allow=r'Items/'), 
            # 해당 링크에 요청을 보내고 응답이 오면 실행할 콜백 메서드를 지정합니다.
            callback='parse_item', 
            # True로 설정되어 있으면 응답에 다시 한번 rules를 적용해 재귀적으로 실행합니다.
            follow=True),
        
        # 이렇게 여러개의 규칙을 설정할 수 있습니다.
        # Rule(LinkExtractor(allow=r'.*'), callback = 'parse_item', follow = True),
    )

    def parse_item(self, response):
        # rules를 통과한 링크에 요청을 보내 응답을 받으면 Rule()에 설정한 콜백 메서드를 해당 응답 결과에 실행합니다.
        # 따라서 response를 파라미터로 받고 XPath라든가 CSS 선택자를 이용해서 원하는 요소를 추출할 수 있습니다.
        
        # 앞서 설정한 아이템에 맞춰 딕셔너리를 채우고 반환합니다.
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
