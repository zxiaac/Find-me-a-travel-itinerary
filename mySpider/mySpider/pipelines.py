# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
'''
import boto.ec2
conn = boto.ec2.connect_to_region("ap-northeast-1")
reservations = conn.get_all_instances()
'''
import codecs
import csv

# 保存到CSV文件中
class MyspiderPipeline(object):

    def __init__(self):
        self.file = codecs.open('a.csv', 'w', encoding='utf_8_sig')

    def process_item(self, item, spider):
        fieldnames = ['title', 'img_url', 'download_http']
        w = csv.DictWriter(self.file, fieldnames=fieldnames)
        w.writerow(item)
        return item

    def close_spider(self, spider):
        self.file.close()
'''
import pymysql
 
 
# 用于数据库存储
class DBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='localhost',
            port=3306,
            db='edu_demo',
            user='root',
            passwd='123456',
            charset='utf8',
            use_unicode=True)
 
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();
 
    def process_item(self, item, spider):
        try:
            # 查重处理
            self.cursor.execute(
                """select * from a_scenic where ctrip_url = %s""",
                item['scenic_url'])
            # 是否有重复数据
            repetition = self.cursor.fetchone()
 
            # 重复
            if repetition:
                pass
 
            else:
                # 插入数据
                self.cursor.execute(
                    """insert into a_scenic(code,province, city, county, name ,description, ctrip_url,image_url,address,type)
                    value (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (item['code'],
                     item['province'],
                     item['city'],
                     item['county'],
                     item['name'],
                     item['descript'],
                     item['scenic_url'],
                     item['image_url'],
                     item['address'], '1'))
 
            # 提交sql语句
            self.connect.commit()
 
        except Exception as error:
            # 出现错误时打印错误日志
            print(error)
        return item
'''
