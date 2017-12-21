'''Debuging

创建该文件用于断点调试

调试时请保证vscode或pycharm在项目根目录打开
'''

from scrapy import cmdline

name = 'douban250'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())