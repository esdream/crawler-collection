import time
import json
import random
import getpass
from urllib import request, parse

def auto_login(username, password):
    if(username and password):

        while True:
            url = 'http://p.nju.edu.cn/portal_io/login'
            value = {
                'username': username,
                'password': password
            }

            user_data = parse.urlencode(value).encode('ascii')
            req = request.Request(url, data=user_data)

            with request.urlopen(req) as res:
                encoding = res.headers.get_content_charset()
                res_info = json.loads(res.read().decode(encoding))
                
                result_code = int(res_info['reply_code'])

                if(result_code in (1, 6)):
                    user_id = res_info['userinfo']['username']
                    user_fullname = res_info['userinfo']['fullname']
                    balance = res_info['userinfo']['balance'] / 100

                    if(result_code in (1, )):
                        print('\r用户: [{0}, {1}] 登录成功! 余额: {2}元'.format(user_id, user_fullname, balance), end='')
                    else:
                        print('\r用户: [{0}, {1}] 已经登录! 余额: {2}元'.format(user_id, user_fullname, balance), end='')

                elif(result_code == 3):
                    print('密码错误! 请输入正确的用户名与密码!')
                    return

                elif(result_code == 8):
                    print('用户名或密码名为空!')
                    return
                
                else:
                    print(result_code)
                    print('其他未知错误，请联系网络管理员!')
                    return

            # 时间间隔为3600s 至 3720s 之间随机
            sleep_time = random.randint(3600, 3720)
            time.sleep(sleep_time)

    else:
        print('请输入用户名与密码')

def main():
    username = input('请输入您的用户名:')
    password = getpass.getpass('请输入您的密码:')

    auto_login(username, password)

if(__name__ =='__main__'):
    main()
