import os
import re
import time
import random
import requests

def migration_crawler(flow_filename):
    with open(flow_filename, mode='w', encoding='utf-8') as f_flow:

        f_flow.write('date,direction,center_city,flow_city,pop,per_car,per_train,per_plane\n')

        # 城市编码，见citycode.csv
        citycode = '320100'
        center_city = '南京'
        # 迁移方式，1汽车 2火车 3飞机 6全部
        mig_type = '6'

        for day in range(1, 19):
            
            if(day < 10):
                day = '0' + str(day)
            # 日期，年月日
            date = '201712{0}'.format(str(day))

            # 迁移方向，0迁入 1迁出
            for direction in range(2):

                url = 'https://lbs.gtimg.com/maplbs/qianxi/{0}/{1}{2}{3}.js'.format(date, citycode, direction, mig_type)
                headers = {
                    'authority': 'lbs.gtimg.com',
                    'method': 'GET',
                    'scheme': 'https',
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'referer': 'https://heat.qq.com/qianxi/index.html',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
                }

                timeout = 2
                while(timeout > 0):
                    
                    time.sleep(random.uniform(1, 2))

                    timeout -= 1
                
                    try:
                        data_src = requests.get(url, headers=headers).text
                        citys = re.findall(r'\[("\S+?)\]', data_src)
                        for city in citys:
                            flow_city, pop, per_car, per_train, per_plane = city.split(',')
                            f_flow.write(
                                '{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(date, direction, center_city, flow_city, int(pop), float(per_car), float(per_train), float(per_plane)))
                        print('date:{0}, direction:{1} crawl succeed!'.format(date, direction))
                        break
                    except Exception as err:
                        print('date:{0}, direction:{1} crawl error!'.format(
                            date, direction))
                        print(err)

def main():
    flow_filename = 'flow.csv'
    migration_crawler(flow_filename)

if(__name__ == '__main__'):
    main()
