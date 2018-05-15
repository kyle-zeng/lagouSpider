# -*- coding: utf-8 -*-

import pymysql
from lagouSpider.items import LagouspiderItem
from lagouSpider import settings


class MySqlPipeline(object):

    def __init__(self):
        # 建立数据库链接
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOSTS,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DB,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if isinstance(item, LagouspiderItem):
            position_name = item['position_name']
            company_full_name = item['company_full_name']
            city = item['city']
            ret = self.select_title(position_name, company_full_name, city)
            if ret[0] == 1:
                print('已经存在')
                pass
            else:
                salary = item['salary']
                work_year = item['work_year']
                finance_stage = item['finance_stage']
                create_time = item['create_time']

                self.insert_course(position_name, city, salary, work_year, company_full_name, finance_stage, create_time)
                print("存入一条数据" + position_name)

    def insert_course(self, position_name, city, salary, work_year, company_full_name, finance_stage, create_time):
        data = {
            'position_name': position_name,
            'city': city,
            'salary': salary,
            'work_year': work_year,
            'company_full_name': company_full_name,
            'finance_stage': finance_stage,
            'create_time': create_time
        }
        table = 'logoujob'
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            self.connect.close()

    def select_title(self, position_name, company_full_name, city):
        sql = 'select exists (select 1 from logoujob where position_name = %(position_name)s ' \
              'and company_full_name = %(company_full_name)s and city = %(city)s );'
        value = {
            'position_name': position_name,
            'city': city,
            'company_full_name': company_full_name
        }
        self.cursor.execute(sql, value)
        return self.cursor.fetchall()[0]
