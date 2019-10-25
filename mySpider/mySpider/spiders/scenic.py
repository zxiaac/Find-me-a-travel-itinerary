# -*- coding: utf-8 -*-
import scrapy
import re
from mySpider.items import ScenicItem
 
class ScenicSpider(scrapy.Spider):
    name = 'scenic'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://piao.ctrip.com/dest/u-_ba_d3_c4_cf/s-tickets/P1/']
    count = 0
 
    def parse(self, response):
        trs = response.xpath("//div[@id='searchResultContainer']//div[@class='searchresult_product04']")
 
        for tr in trs:
            ctrip_url = tr.xpath(".//div[1]/a/@href").get()
            c1_url = ctrip_url.split("t/t")
            scemic_num = c1_url[1].split(".")
            scemic_num = scemic_num[0]
            scenic_url = ""
            image_url = tr.xpath(".//div[1]/a/img/@src").get()
            address = tr.xpath(".//div[1]/div[@class='adress']//text()").get().strip()
            address = re.sub(r"地址：", "", address)
            descript = tr.xpath(".//div[1]/div[@class='exercise']//text()").get().strip()
            descript = re.sub(r"特色：", "", descript)
            name = tr.xpath(".//div[1]//h2/a/text()").get().strip()
 
            cityinfo=address
            province = "河南省"
            city = ""
            county = ""
            if "省" in cityinfo:
                matchObj = re.match(r'(.*)[?省](.+?)市(.+?)([县]|[区])', cityinfo, re.M | re.I)
                if matchObj:
                    province = matchObj.group(1) + "省"
                    city = matchObj.group(2) + "市"
                    if "县" in cityinfo:
                        county = matchObj.group(3) + "县"
                    else:
                        county = matchObj.group(3) + "区"
                else:
                    matchObj2 = re.match(r'(.*)[?省](.+?)市(.+?)市', cityinfo, re.M | re.I)
                    matchObj1 = re.match(r'(.*)[?省](.+?)市', cityinfo, re.M | re.I)
                    if matchObj2:
                        city = matchObj2.group(2) + "市"
                        county = matchObj2.group(3) + "市"
                    elif matchObj1:
                        city = matchObj1.group(2) + "市"
                    else:
                        matchObj1 = re.match(r'(.*)[?省](.+?)([县]|[区])', cityinfo, re.M | re.I)
                        if matchObj1:
                            if "县" in cityinfo:
                                county = matchObj1.group(2) + "县"
                            else:
                                county = matchObj1.group(2) + "区"
 
            else:
                matchObj = re.match(r'(.+?)市(.+?)([县]|[区])', cityinfo, re.M | re.I)
                if matchObj:
                    city = matchObj.group(1) + "市"
                    if "县" in cityinfo:
                        county = matchObj.group(2) + "县"
                    else:
                        county = matchObj.group(2) + "区"
                else:
                    matchObj = re.match(r'(.+?)市', cityinfo, re.M | re.I)
                    if matchObj:
                        city = matchObj.group(1) + "市"
                    else:
                        matchObj = re.match(r'(.+?)县', cityinfo, re.M | re.I)
                        if matchObj:
                            county = matchObj.group(1) + "县"
 
            self.count += 1
            code = "A" + str(self.count)
 
            item = ScenicItem(name=name,province=province,city=city,county=county,address=address,descript=descript,
                              scenic_url=scenic_url,image_url=image_url,code=code)
 
            yield item
        next_url = response.xpath('//*[@id="searchResultContainer"]/div[11]/a[11]/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse,meta={})
