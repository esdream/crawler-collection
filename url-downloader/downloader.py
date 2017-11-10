#!/usr/bin/env python3

import requests
from contextlib import closing

class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0, unit='', sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.sep = sep

    def __get_info(self):
        # [名称] 状态 进度 单位 分割线 宗师 单位
        _info = self.info % (self.title, self.status, self.count/self.chunk_size, self.unit, self.sep, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None
        self.status = status or self.status
        # 在python3中，print()方法的默认结束符为end='\n'，当调用完后，光标自动切换到下一行。因此在这里将结束符修改为'\r'，输出完成后光标回到行首而不换行，此时再次调用print()方法就能更新这一行输出
        end_str = '\r'
        if(self.count >= self.total):
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)

def main():

    url = 'http://www.consortium.ri.cmu.edu/data/ck/CK+/Landmarks.zip'
    file_name = 'Landmarks.zip'

    session = requests.Session()
    session.auth = (
        '80e9e7eb5d76bfd5715491fee388e4765429b249030857adb2788d2bd72a8c1bHlUnyZjv6OzeymRWJ4cMKloz3w8', 'ber+nYA9Nt64Ta/SJlaZa21owM4')

    # 设置get请求的stream参数为Ture，这样会推迟下载响应体直到访问Reponse.content属性
    with closing(session.get(url, stream=True)) as response:
        chunk_size = 1024 # 单次请求最大值
        content_size = int(response.headers['content-length']) # 内容体总大小
        progress = ProgressBar(file_name, total=content_size, unit="KB",
                               chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
        with open(file_name, 'wb') as f_downlaod:
            for data in response.iter_content(chunk_size=chunk_size):
                f_downlaod.write(data)
                progress.refresh(count=len(data))

if(__name__ == '__main__'):
    main()
