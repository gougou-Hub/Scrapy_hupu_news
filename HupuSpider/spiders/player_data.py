# 爬取NBA中文网近20年的球员数据
# 因为NBA中文网球员数据是通过json异步加载的，所以需要抓包实现
import time
import requests
import json
import csv


# 获取json文件里面的内容并提取信息
def get_json_content(url):
    # r_content=requests.get(url).content.decode('utf-8')

    r_content = requests.get(url).text

    # 将json文件里的内容转化为json格式，结构化方便提取数据
    r_json = json.loads(r_content)
    # 球员数据所在赛季
    season = r_json.get('payload')['season']['statsSeasonYearDisplay']

    for i in range(0, 50):
        # 用一个字典保存球员数据所在的赛季
        data = {}
        data['赛季'] = season
        player = r_json.get('payload')['players'][i]
        data['球员姓名'] = player['playerProfile']['displayName']
        data['国家'] = player['playerProfile']['country']
        data['球队'] = player['teamProfile']['displayAbbr']
        data['身高'] = player['playerProfile']['height']
        data['体重'] = player['playerProfile']['weight']
        data['位置'] = player['playerProfile']['position']
        data['上场时间'] = player['statAverage']['minsPg']
        data['场均得分'] = player['statAverage']['pointsPg']
        data['篮板'] = player['statAverage']['rebsPg']
        data['助攻'] = player['statAverage']['assistsPg']
        data['盖帽'] = player['statAverage']['blocksPg']
        data['防守'] = player['statAverage']['defRebsPg']
        data['效率'] = player['statAverage']['efficiency']
        data['命中率'] = player['statAverage']['fgpct']

        print('第' + str(i + 1) + '个球员数据信息已经爬取完成')
        print(data)
        # 引用全局变量文件路径
        global path
        with open(path, 'a') as f:
            # 得到一个CSV写入对象
            writer = csv.writer(f, dialect=my_dialect)
            # 向CSV文件中写入一行数据
            writer.writerow((data['赛季'], data['球员姓名'], data['国家'], data['球队'], data['身高'], data['体重'], data['位置'],
                             data['上场时间'], data['场均得分'], data['篮板'], data['助攻'], data['盖帽'], data['防守'], data['效率'],
                             data['命中率']))


if __name__ == '__main__':
    # 数据保存路径
    path = 'E://NBA_data.csv'


    # 自定义一个CSV文件内容分隔形式
    class my_dialect(csv.Dialect):
        lineterminator = '\n'
        delimiter = ','
        quotechar = '"'
        quoting = csv.QUOTE_MINIMAL


    with open(path, 'w') as f:
        writer = csv.writer(f, dialect=my_dialect)
        writer.writerow(('赛季', '球员姓名', '国家', '球队', '身高', '体重', '位置', '上场时间',
                         '场均得分', '篮板', '助攻', '盖帽', '防守', '效率', '命中率'))

    # 球员数据的json包链接
    url1 = 'http://china.nba.com/static/data/league/playerstats_All_All_All_0_All_false_'
    url2 = '_4_All_Team_points_All_perGame.json'
    for i in range(1996, 2017):
        if (i != 2004):
            i = str(i)
            url = url1 + i + url2
            get_json_content(url)
            time.sleep(3)
