import re
import os
import requests
import urllib
import time


class BaiduSpider():

    def __init__(self):
        self.keyword = input('欢迎使用百度图片下载器\n请输入搜索关键词：') 
        self.siteURL = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + str(
            self.keyword) + '&ct=201326592&v=flip'

    def getSource(self):
        url = self.siteURL
        result = requests.get(url).text
        return result

    def getItem(self):
        result = self.getSource()
        pattern1 = re.compile('"objURL":"(.*?)",', re.S)
        items = re.findall(pattern1, result)
        return items

    def saveImage(self, item, name):
        picture = urllib.request.urlopen(item)
        fileName = name + '.jpg'
        string = 'D:\Cloud\%s\%s' % (self.path, fileName)
        E = os.path.exists(string)
        if not E:
            f = open(string, 'wb')
            f.write(picture.read())
            f.close()
        else:
            print('图片已经存在，跳过！')
            return False


    def makeDir(self, path):
        self.path = path.strip()
        E = os.path.exists(os.path.join('D:\Cloud', self.path))
        if not E: 
            os.makedirs(os.path.join('D:\Cloud', self.path))
            os.chdir(os.path.join('D:\Cloud', self.path))
            print('成功创建名为', self.path, '的文件夹')
            return self.path
        else:
            print('名为', self.path, '的文件夹已经存在...')
            return False

    def savePicture(self):
        i = 0
        items = self.getItem()
        print ('找到关键词:'+self.keyword+'的图片，现在开始下载图片...')
        self.makeDir(path=self.keyword)
        for item in items:
            print ('正在下载第'+str(i+1)+'张图片，图片地址:'+str(item))
            try:
                pic = requests.get(item, timeout=10)
            except requests.exceptions.ConnectionError:
                print ('【错误】当前图片无法下载')
                continue
            self.saveImage(item, name=self.keyword+'_' + str(i))
            i += 1

if __name__ == '__main__':
    spider = BaiduSpider()
    spider.savePicture()
