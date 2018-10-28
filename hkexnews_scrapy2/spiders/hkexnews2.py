import scrapy
import datetime

from hkexnews_scrapy2.items import ShanghaiStock

class kexnews2Spider(scrapy.Spider):
    name = "hkexnews2"
    allowed_domains = ['hkexnews.hk']

    def __init__(self, *args, **kwargs):
        self.date = kwargs.get('date', datetime.date.strftime(datetime.date.today() + datetime.timedelta(-1) , "%Y%m%d"))
        self.strToday = datetime.date.strftime(datetime.date.today(), "%Y%m%d")

    def start_requests(self):
        urls = [
            'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sh',
            'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sz',
            'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('gsdebug: step 2!!!!!!!')
        print('gsdebug: year: ' + self.date[0:4])
        print('gsdebug: m: ' + self.date[4:6])
        print('gsdebug: d: ' + self.date[6:8])
        yield scrapy.FormRequest(
            response.request.url,
            formdata={
                'today': self.strToday,
                'sortBy': 'stockcode',
                'sortDirection': 'asc',
                'alertMsg': '',
                'txtShareholdingDate': self.date[0:4]+"/"+self.date[4:6]+"/"+self.date[6:8],
                'btnSearch':'Search',
                '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                '__VIEWSTATEGENERATOR': response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first(),
                '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first()

            },
            callback=self.parse_results
        )

    def parse_results(self, response):
        print('gsdebug: step 3!!!!!!!, response size:' + str(len(response.body)))
        ########### test1
        # for quote in response.css("div.quote"):
        #     yield {
        #         'quote': quote.css('span.content ::text').extract_first(),
        #         'author': quote.css('span.author ::text').extract_first(),
        #         'tag': quote.css('span.tag ::text').extract_first(),
        #     }
        #page = response.url.split("/")[-2]
        #filename = 'sc-%s.html' % page

        ########### test2
        # filename = 'sc.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

        ########### test3
        records = response.xpath('//*[@id="mutualmarket-result"]/tbody/tr[*]')
        print('gsdebug: step 3!!!!!!!, records size:' + str(len(records)))

        for i in records:
            item = ShanghaiStock()
            # result = i.xpath('td/text()').extract()
            result = i.xpath('td[*]/div[@class="mobile-list-body"]/text()').extract()
            result = list(map(str.strip, result))
            if len(result)==3:
                result.append("0")
            item['code'] = result[0]
            item['stock_ename'] = result[1]
            item['share_holding'] = result[2].replace(',', '')
            item['percent'] = result[3]
            item['date'] = self.date

            yield item
