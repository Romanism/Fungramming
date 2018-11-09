# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# 9.4 스파이더 규칙 정하기
class BookCrawlSpider(CrawlSpider):
    # 크롤러의 이르입니다. 실제 크롤링할 할 때 사용합니다.
    name = 'book_crawl'

    # 크롤러 실행을 허용할 도메인을 여기서 지정합니다.
    # 해당 서버에서 실행되다가 허용된 도메인 이외에는 무시합니다.
    allowed_domains = ['www.hanbit.co.kr']

    # 시작점으로 사용할 URL입니다.
    # 리스트로 지정해 한 번에 여러 웹 페이지에서 크롤링을 시작하게 할 수 있습니다.
    start_urls = ['http://www.hanbit.co.kr/store/books/category_list.html?cate_cd=001',
                  'http://www.hanbit.co.kr/store/books/category_list.html?cate_cd=002',
                  'http://www.hanbit.co.kr/store/books/category_list.html?cate_cd=003',
                  'http://www.hanbit.co.kr/store/books/category_list.html?cate_cd=004',
                  'http://www.hanbit.co.kr/store/books/category_list.html?cate_cd=005',
                  'http://www.hanbit.co.kr/store/books/category_list.html?cate_cd=006',
                  'http://www.hanbit.co.kr/store/books/category_list.html?cate_cd=007',
                  'http://www.hanbit.co.kr/store/books/category_list.html?cate_cd=008',]

    # 크롤러가 어떻게 작동할지 규칙을 설정합니다.
    # 크롤러는 시작점의 모든 링크를 검사한 후 규칙에 맞는 링크가 있으면 정해진 콜백 메서드를 실해앟ㅂ니다.
    # follow가 True면 해당 페이지의 링크를 대상으로 재귀적으로 앞 작업을 반복합니다.
    rules = (
        # 크롤링할 링크 정규 표현식을 이용해서 표현합니다.
        Rule(LinkExtractor(allow = r'store/books/look.php\?p_code=.*'),
        # 해당 링크에 요청을 보내고 응답이 오면 실행할 콜백 메서드를 지정합니다.
        callback = 'parse_item',
        # True로 설정되어 있으면, 응답에 다시 한번 rules를 적용해 재귀적으로 실행합니다.
        follow = True),

        Rule(LinkExtractor(allow=r'store/books/category_list\.html\?page=\d+&cate_cd=00\d+&srt=p_pub_date'))

        # 이런식으로 여러 규칙을 정할 수 있습니다.
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),)
        )


    # 9.5 파서 함수 정의
    def parse_item(self, response):
        '''
        rules를 통과한 링크에 요청을 보내 응답을 받으면 Rule()에 설정한 콜백 메서드를 해당 응답 결과에 실행합니다.
        따라서 response를 파라미터로 받고 XPath라든가 CSS 선택자를 이용해서 원하는 요소를 추출할 수 있습니다.
        '''

        # 앞서 설정한 아이템에 맞춰 딕셔너리를 채우고 반환합니다.
        i = {}

        # 책이름
        i['book_title'] = response.xpath('//*[@id="container"]/div[1]/div[1]/div[1]/div[2]/h3/text()').extract()

        # 저자 이름
        i['book_author'] = response.xpath('//*[@id="container"]/div[1]/div[1]/div[1]/div[2]/ul/li[strong/text()="저자 : "]/span/text()').extract()

        # 번역자 이름
        i['book_translator'] = response.xpath('//*[@id="container"]/div[1]/div[1]/div[1]/div[2]/ul/li[strong/text()="번역 : "]/span/text()').extract()

        # 출간일
        i['book_pub_date'] = response.xpath('//*[@id="container"]/div[1]/div[1]/div[1]/div[2]/ul/li[strong/text()="출간 : "]/span/text()').extract()

        # ISBN
        i['book_isbn'] = response.xpath('//*[@id="container"]/div[1]/div[1]/div[1]/div[2]/ul/li[strong/text()="ISBN : "]/span/text()').extract()
        return i
