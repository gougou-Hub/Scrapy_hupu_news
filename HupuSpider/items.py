# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
# 项目的目标文件
import scrapy


class HupuspiderItem(scrapy.Item):
    # 球队名称
    teamname = scrapy.Field()
    # 球队url
    teamurl = scrapy.Field()
    # 新闻标题
    newstitle = scrapy.Field()
    # 新闻链接
    newsurl = scrapy.Field()
    # 新闻内容
    content = scrapy.Field()
    # 新闻配图url
    imageurl = scrapy.Field()


class HupuItem(scrapy.Item):

    # 球队
    playerteam = scrapy.Field()

    # 球员照片
    playerimg = scrapy.Field()

    # 球员姓名
    playername = scrapy.Field()

    # 球员号码
    playernumber = scrapy.Field()

    # 球员位置
    playerjob = scrapy.Field()

    # 球员身高
    playertall = scrapy.Field()

    # 球员体重
    playerweight = scrapy.Field()

    # 球员生日
    playerbirthday = scrapy.Field()

    # 球员合同
    playercont = scrapy.Field()

    # 球员年薪
    playersal = scrapy.Field()
