# -*- coding: utf-8 -*-
import scrapy
from disputespider.items import DisputespiderItem
import json
import time
import logging
from copy import deepcopy
from disputespider.accesstoken import get_access_token


class DisputeSpider(scrapy.Spider):
    name = 'dispute'
    allowed_domains = ["paypal.com"]
    start_urls = ['https://api.paypal.com/v1/customer/disputes']
    access_token = get_access_token()  # 获取access_token
    # access_token = 'A21AAEZ2Xadmq2GrNBw8h2Qfi8Qjh6jDsE4FVCozuVPbyX6nDUHZM4zB7O0Fo5ZdD5VFtFCrXWncDEGQmWfTdp-9YKB_8RzkA'
    logging.debug('成功获取access_token')
    # print(access_token)

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Authorization": "bearer " + access_token,
            'Content-Type': 'application/json',
        }
    }

    def parse(self, response):
        try:
            data = response.body.decode()
            data = json.loads(data)
            # print(data)
            info = data['items']
            for i in info:
                # print(i)
                item = DisputespiderItem()
                item['dispute_id'] = i['dispute_id']
                item['create_time'] = i['create_time']
                item['update_time'] = i['update_time']
                item['reason'] = i['reason']
                item['status'] = i['status']
                item['dispute_state'] = i['dispute_state']
                item['currency_code'] = i['dispute_amount']['currency_code']
                item['total_price'] = i['dispute_amount']['value']
                item['url'] = i['links'][0]['href']
                detail_link = i['links'][0]['href']
                # print(detail_link)
                if detail_link:
                    yield scrapy.Request(detail_link, callback=self.parse_detail, meta={'item': deepcopy(item)},
                                         dont_filter=True)
        except Exception as e:
            logging.debug('api可能有改变---{}'.format(e))

    def parse_detail(self, response):
        try:
            item = response.meta['item']
            print(response.url)
            body = response.body.decode()
            body = json.loads(body)
            item['buyer_transaction_id'] = body['disputed_transactions'][0]['buyer_transaction_id']
            item['invoice_code'] = body['disputed_transactions'][0]['invoice_number']
            item['buyer'] = body['disputed_transactions'][0]['buyer']['name']
            item['seller'] = body['disputed_transactions'][0]['seller']['email']
            item['dispute_life_cycle_stage'] = body['dispute_life_cycle_stage']
            item['dispute_channel'] = body['dispute_channel']
            try:
                item['messages'] = body['messages'][0]
            except Exception as e:
                item['messages'] = ''
                logging.debug('messages不存在,将其设置为空---{}'.format(e))
            try:
                item['extensions'] = body['extensions']
            except Exception as e:
                item['extensions'] = ''
                logging.debug('extensions不存在,将其设置为空---{}'.format(e))
            try:
                item['evidences'] = body['evidences']
            except Exception as e:
                item['evidences'] = ''
                logging.debug('evidence不存在,将其设置为空---{}'.format(e))
            item['links'] = body['links']
            item['disputed_transactions'] = body['disputed_transactions']
            try:
                item['offer'] = body['offer']
            except Exception as e:
                item['offer'] = ''
                logging.debug('offer不存在,将其设置为空---{}'.format(e))
            item['stamp'] = int(time.time())

            yield item
        except Exception as e:
            logging.debug('详情页数据出现问题---{}'.format(e))
