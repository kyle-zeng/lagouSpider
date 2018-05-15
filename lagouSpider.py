
import scrapy
from lagouSpider.items import LagouspiderItem
from scrapy import FormRequest

import time
import random
import json


class lagouSpider(scrapy.Spider):

    name = "lagouSpider"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
    }
    allowed_domains = ["lagou.com"]
    # url地址
    base_url = u'https://www.lagou.com/jobs/positionAjax.json?'# px=default&city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false
    # 页码
    page = 1

    def start_requests(self):
        # 请求第一页数据
        yield FormRequest(self.base_url, headers=self.headers,
                          formdata={
                              'needAddtionalResult': 'false',
                              'first': 'true',
                              'pn': str(self.page),
                              'kd': 'python',
                              'city': '深圳'
                          }, callback=self.parse)

    def parse(self, response):
        print(response.body)
        item = LagouspiderItem()
        # 解析
        data = json.loads(response.body.decode('utf-8'))
        result = data['content']['positionResult']['result']   # 职位信息
        result_size = data['content']['positionResult']['resultSize']  # 每页条数
        total_count = data['content']['positionResult']['totalCount']  # 总条数
        for position in result:    # 封装item字段
            item['position_name'] = position['positionName']
            item['city'] = position['city']
            item['salary'] = position['salary']
            item['work_year'] = position['workYear']
            item['company_full_name'] = position['companyFullName']
            item['finance_stage'] = position['financeStage']
            item['create_time'] = position['createTime']
            yield item

        time.sleep(random.randint(10, 30))  # 设置每个请求的间隔时间
        if int(result_size) == 15:
            allpage = int(total_count) / int(result_size) + 1  # 总页数
            if self.page < allpage:
                self.page += 1
                print('正在请求第 %s 页数据' % self.page)
                if self.page % 5 == 0:
                    time.sleep(20)  # 防止被禁
                yield FormRequest(self.base_url, headers=self.headers,
                                  formdata={
                                      'needAddtionalResult': 'false',
                                      'first': 'false',
                                      'pn': str(self.page),
                                      'kd': 'python',
                                      'city': '深圳'
                                  }, callback=self.parse)
