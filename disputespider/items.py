# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DisputespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    dispute_id = scrapy.Field()  # Paypal Case Id
    create_time = scrapy.Field()  # 创建时间
    update_time = scrapy.Field()  # 创建时间
    reason = scrapy.Field()  # 原因
    status = scrapy.Field()  # 状态
    dispute_state = scrapy.Field()  # 处理状态
    currency_code = scrapy.Field()  # 货币
    total_price = scrapy.Field()  # 订单金额
    url = scrapy.Field()  # 详情链接
    buyer_transaction_id = scrapy.Field()  # 买家交易ID
    buyer = scrapy.Field()  # 客户姓名
    invoice_code = scrapy.Field()  # 账单号提取
    seller = scrapy.Field()  # 卖家账号
    dispute_life_cycle_stage = scrapy.Field()  # 争议阶段
    dispute_channel = scrapy.Field()  # 争议渠道
    messages = scrapy.Field()  # 留言信息
    extensions = scrapy.Field()  # 补充信息
    evidences = scrapy.Field()  # 证据
    links = scrapy.Field()  # 补充信息
    disputed_transactions = scrapy.Field()  # 交易细节
    offer = scrapy.Field()  # 客户需求
    stamp = scrapy.Field()  # 爬取时间戳


