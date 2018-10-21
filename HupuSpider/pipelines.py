# -*- coding: utf-8 -*-

import pymysql
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
import scrapy
import os
import json
import codecs


class HupuspiderPipeline(object):
    def process_item(self, item, spider):
        # 新闻标题作为文件夹名字
        filename = item['newstitle']
        filename += ".txt"

        # 每条新闻放到对应的球队文件夹中
        savepath = '../虎扑新闻/' + item['teamname'] + '/' + item['newstitle'] + '/' + filename
        with open(savepath, 'w', encoding='utf-8') as fp:
            fp.write(item['content'])
            fp.close()
        return item


class HupuImagesPipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")

    def get_media_requests(self, item, info):
        image_url = item["imageurl"]
        yield scrapy.Request(image_url[0])

    def item_completed(self, results, item, info):
        # 固定写法，获取图片路径，同时判断这个路径是否正确，如果正确，
        # 就放到 image_path里，ImagesPipeline源码剖析可见
        image_path = [x["path"] for ok, x in results if ok]

        # 每张新闻配图放到对应的球队文件夹中
        os.rename(self.IMAGES_STORE + "/" + image_path[0],
                  self.IMAGES_STORE + "/" + item["teamname"] + "/" + item["newstitle"] + "/" + item[
                      "newstitle"] + ".jpg")

        return item

    # get_media_requests的作用就是为每一个图片链接生成一个Request对象，
    # 这个方法的输出将作为item_completed的输入中的results，
    # results是一个元组，每个元组包括(success, imageinfoorfailure)。
    # 如果success=true，imageinfoor_failure是一个字典，
    # 包括url/path/checksum三个key。


####注意一定要导入配置，因为数据库的一些连接信息写在settings文件里的
# 此类是把信息写入文档，写入时末尾都加了一个逗号，是为了数据的观看与直观性
# 也方便以后用mysql语言直接导入数据
'''
class GamerankPipeline(object):
    def process_item(self, item, spider):
        with open(r'F:\pycharm\puthon项目\HupuSpider\text1.txt', 'a', encoding='utf-8') as f:
            #f.write(item['teamname'])
            #f.write('\n')
            f.write(item['teamurl'])
            f.write('\n')
            #f.write(item['newstitle'])
            #f.write('\n')
            f.write(item['newsurl'])
            f.write('\n')
            #f.write(item['content'])
            #Imageurl = ''.join(item['imageurl']).replace('.png', '.jpg')
            #f.write(Imageurl)
            #f.write('\n')
'''


class mysqlPipeline(object):
    def process_item(self, item, spider):
        # 将item里的数据拿出来
        teamname = item['teamname']
        teamurl = item['teamurl']
        newstitle = item['newstitle']
        newsurl = item['newsurl']
        content = item['content']
        Imageurl = ''.join(item['imageurl']).replace('.png', '.jpg')

        # 和本地的newsDB数据库建立连接
        db = pymysql.connect(
            host='localhost',  # 连接的是本地数据库
            user='root',  # 自己的mysql用户名
            passwd='123456',  # 自己的密码
            db='hupu',  # 数据库的名字
            charset='utf8',  # 默认的编码方式：
            cursorclass=pymysql.cursors.DictCursor)
        try:
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
            # SQL 插入语句
            sql = "INSERT INTO information(teamname,teamurl,newstitle,newsurl,content,Imageurl) \
                  VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
                teamname, teamurl, newstitle, newsurl, content, Imageurl)
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            db.commit()
        finally:
            # 关闭连接
            db.close()
        return item


class JsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('player.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class mysqlplayerPipeline(object):
    def process_item(self, item, spider):
        # 将item里的数据拿出来
        playerteam = item['playerteam']
        player_img = item['playerimg']
        playername = item['playername']
        playernumber = item['playernumber']
        playerjob = item['playerjob']
        playertall = item['playertall']
        playerweight = item['playerweight']
        playerbirthday = item['playerbirthday']
        playercont = item['playercont']
        playersal = item['playersal']
        # 和本地的newsDB数据库建立连接
        db = pymysql.connect(
            host='localhost',  # 连接的是本地数据库
            user='root',  # 自己的mysql用户名
            passwd='123456',  # 自己的密码
            db='hupu',  # 数据库的名字
            charset='utf8',  # 默认的编码方式：
            cursorclass=pymysql.cursors.DictCursor)
        try:
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
            # SQL 插入语句
            sql = "INSERT INTO player(playerteam,player_img,playername,playernumber,playerjob,playertall,playerweight,playerbirthday,playercont,playersal) \
                  VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                playerteam, player_img, playername, playernumber, playerjob, playertall, playerweight, playerbirthday,
                playercont, playersal)
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            db.commit()
        finally:
            # 关闭连接
            db.close()
        return item
