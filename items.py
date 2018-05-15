# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 标题
    position_name = scrapy.Field()
    # 工作地址
    city = scrapy.Field()
    # 薪水待遇
    salary = scrapy.Field()
    # 工作经验
    work_year = scrapy.Field()
    # 公司名称
    company_full_name = scrapy.Field()
    # 融资情况
    finance_stage = scrapy.Field()
    # 发布时间
    create_time = scrapy.Field()
    pass
