import scrapy
import re
from HupuSpider.items import HupuItem


class Hupu(scrapy.Spider):
    name = 'hupu'
    allowed_domains = ['hupu.com']
    start_urls = ['https://nba.hupu.com/players/rockets']

    def parse(self, response):
        url_list = response.xpath('//span[@class="team_name"]/a/@href').extract()
        playerteam_list = response.xpath('//span[@class="team_name"]/a/text()').extract()
        for url, playerteam in zip(url_list, playerteam_list):
            team_url = url
            yield scrapy.Request(url=team_url, meta={'playerteam': playerteam}, callback=self.parse_detail)

    def parse_detail(self, response):
        print("开始下载...")
        item = HupuItem()
        # 球队
        item['playerteam'] = response.meta['playerteam']
        # 球员照片
        player_img_list = response.xpath('//td[@class="td_padding"]//img/@src').extract()
        # 球员姓名
        player_name_list = response.xpath('//td[@class="left"][1]//a/text()').extract()
        # 球员号码
        player_number_list = response.xpath('//tr[not(@class)]/td[3]/text()').extract()
        # 球员位置
        player_job_list = response.xpath('//tr[not(@class)]/td[4]/text()').extract()
        # 球员身高
        player_tall_list = response.xpath('//tr[not(@class)]/td[5]/text()').extract()
        # 球员体重
        player_weight_list = response.xpath('//tr[not(@class)]/td[6]/text()').extract()
        # 球员生日
        player_birthday_list = response.xpath('//tr[not(@class)]/td[7]/text()').extract()
        # 球员合同
        player_cont_list = response.xpath('//td[@class="left"][2]/text()').extract()
        # 球员年薪
        player_sal_list = response.xpath('//td[@class="left"][2]/b/text()').extract()
        zz = zip(player_img_list, player_name_list, player_number_list, player_job_list, player_tall_list,
                 player_weight_list, player_birthday_list, player_cont_list, player_sal_list)
        for player_img, player_name, player_number, player_job, player_tall, player_weight, player_birthday, player_cont, player_sal in zz:
            item["playerimg"] = player_img
            item['playername'] = player_name
            item['playernumber'] = player_number
            item['playerjob'] = player_job
            item['playertall'] = player_tall
            item['playerweight'] = player_weight
            item['playerbirthday'] = player_birthday
            if player_cont:
                item['playercont'] = player_cont
            else:
                item['playercont'] = 'NULL'
            item['playersal'] = player_sal

            yield item
