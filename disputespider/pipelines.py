# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from disputespider.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD, MYSQL_CHARSET
from pymysql import *
import logging
import json


class DisputespiderPipeline(object):

    def __init__(self):
        self.conn = connect(host=MYSQL_HOST,
                            port=MYSQL_PORT,
                            database=MYSQL_DB,
                            user=MYSQL_USER,
                            password=MYSQL_PASSWORD,
                            charset=MYSQL_CHARSET
                            )
        self.cs1 = self.conn.cursor()

    def process_item(self, item, spider):
        print(item)
        # item = dict(item)
        insert_sql = 'insert ignore into table_paypal_case (dispute_id,create_time,update_time,reason,status,dispute_state,' \
                     'currency_code,total_price,url,buyer_transaction_id,buyer,invoice_code,seller,dispute_life_cycle_stage,' \
                     'dispute_channel,messages,extensions,evidences,links,disputed_transactions,offer,stamp)' \
                     ' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.conn.ping(reconnect=True)
        item['stamp'] = str(item['stamp'])
        self.cs1.execute(insert_sql,
                         (item['dispute_id'], item['create_time'], item['update_time'], item['reason'], item['status'],
                          item['dispute_state'], item['currency_code'], item['total_price'], item['url'],
                          item['buyer_transaction_id'],
                          item['buyer'], item['invoice_code'], str(item['seller']), item['dispute_life_cycle_stage'],
                          item['dispute_channel'], str(item['messages']),
                          str(item['extensions']), str(item['evidences']), str(item['links']),
                          str(item['disputed_transactions']),
                          str(item['offer']),
                          item['stamp']))
        self.conn.commit()
        logging.debug('插入数据库成功')
        return item

    def close_spider(self, spider):
        self.cs1.close()
        self.conn.close()
