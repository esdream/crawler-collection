"""Supermarket Crawler

Crawl the locations of supermarkets in 26 cities.
"""

import codecs
import requests

def supermarket_crawler():
    """Supermarket Crawler
    """

    cities = ['上海', '南京', '无锡', '常州', '苏州', '南通', '盐城', '扬州', '镇江', '泰州', '杭州', '宁波', '嘉兴', '湖州', '绍兴', '金华', '舟山', '台州', '合肥', '芜湖', '马鞍山', '铜陵', '安庆', '滁州', '池州', '宣城']
    supermarkets = ['苏果', '家乐福', '世界联华', '沃尔玛', '欧尚', '大润发', '金润发', '卜蜂莲花', '华润万家', '永辉', '金鹰', '八佰伴', '华联', '好又多', '麦德龙']

    # test_cities = ['上海', '南京']
    # test_supermarkets = ['苏果', '家乐福']
    page_size = 20

    # 要实现写入时编码为UTF-8，应使用codecs模块的open
    with codecs.open('supermarkets.txt', 'w', encoding='utf-8') as market_file:

        for city in cities:
            for supermarket_name in supermarkets:
                url_total = 'http://api.map.baidu.com/place/v2/search?q={0}&region={1}&page_size={2}&output=json&ak=olMgKDcNVqnRUpCMalhGzljcafrlFFwt'.format(supermarket_name, city, page_size)
                try:
                    supermarket_num = requests.get(url_total).json()['total']
                    print(url_total)

                    page_total = supermarket_num // 20 + 1
                    
                    for page_num in range(page_total):
                        url = 'http://api.map.baidu.com/place/v2/search?q={0}&region={1}&page_size={2}&page_num={3}&output=json&ak=olMgKDcNVqnRUpCMalhGzljcafrlFFwt'.format(supermarket_name, city, page_size, page_num)
                        print(url)
                        supermarket_json = requests.get(url).json()

                        rest_size = page_size
                        if(page_num == page_total - 1):
                            rest_size = supermarket_num - page_num * page_size
                        for supermarket_num in range(rest_size):
                            try:
                                supermarket = supermarket_json['results'][supermarket_num]
                                print(city, supermarket_name)
                                market_file.write('{0} {1} {2} {3}\n'.format(supermarket['name'], supermarket['location']['lat'], supermarket['location']['lng'], supermarket['address']))

                            except Exception as crawl_error:
                                pass

                except Exception as crawl_error:
                    pass

if(__name__ == '__main__'):
    supermarket_crawler()
