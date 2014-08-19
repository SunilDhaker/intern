from scrapy.http import FormRequest
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector

from scrapy.spider import BaseSpider


class AcrisSpider(BaseSpider):
    name = "acris"
    allowed_domains = ["a836-acris.nyc.gov"]
    start_urls = ['http://a836-acris.nyc.gov/DS/DocumentSearch/DocumentType']


    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        document_classes = hxs.select('//select[@name="combox_doc_doctype"]/option')

        form_token = hxs.select('//input[@name="__RequestVerificationToken"]/@value').extract()[0]
        for document_class in document_classes:
            if document_class:
                doc_type = document_class.select('.//@value').extract()[0]
                doc_type_name = document_class.select('.//text()').extract()[0]
                formdata = {'__RequestVerificationToken': form_token,
                            'hid_selectdate': '7',
                            'hid_doctype': doc_type,
                            'hid_doctype_name': doc_type_name,
                            'hid_max_rows': '10',
                            'hid_ISIntranet': 'N',
                            'hid_SearchType': 'DOCTYPE',
                            'hid_page': '1',
                            'hid_borough': '0',
                            'hid_borough_name': 'ALL BOROUGHS',
                            'hid_ReqID': '',
                            'hid_sort': '',
                            'hid_datefromm': '',
                            'hid_datefromd': '',
                            'hid_datefromy': '',
                            'hid_datetom': '',
                            'hid_datetod': '',
                            'hid_datetoy': '', }
                yield FormRequest(url="http://a836-acris.nyc.gov/DS/DocumentSearch/DocumentTypeResult",
                                  method="POST",
                                  formdata=formdata,
                                  callback=self.parse_page,
                                  meta={'doc_type_name': doc_type_name})

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)

        rows = hxs.select('//form[@name="DATA"]/table/tbody/tr[2]/td/table/tr')
        for row in rows:
            item = AcrisItem()
            borough = row.select('.//td[2]/div/font/text()').extract()
            block = row.select('.//td[3]/div/font/text()').extract()

            if borough and block:
                item['borough'] = borough[0]
                item['block'] = block[0]
                item['doc_type_name'] = response.meta['doc_type_name']

                yield item