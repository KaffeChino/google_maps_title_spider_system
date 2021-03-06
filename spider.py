import requests
from PIL import Image
from io import BytesIO
# from random import random
import time
import deg2num
import os


class spider_system():

    def run(x_small, x_large, y_small, y_large, zoom):

        # 定义Cookies， header， 下载计数器count，
        # 总成功下载数success，计算总图块数量total
        cookie = requests.get("http://google.cn/maps").cookies
        url = 'http://www.google.cn/maps/vt?lyrs=s@821&gl=cn&x={x}&y={y}&z={z}'
        header = {
            'Host': "www.google.cn",
            'Connection': "keep-alive",
            'Origin': "http://www.google.cn",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                           AppleWebKit/537.36 (KHTML, like Gecko) \
                           Chrome/71.0.3578.98 Safari/537.36",
            'Accept': "image/webp,image/apng,image/*,*/*;q=0.8",
            'Referer': "http://www.google.cn/",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9,zh-TW;q=0.8"}
        total = int((x_large - x_small + 1) * (y_large - y_small + 1))
        count = 0
        success = 0

        # 更改当前文件夹
        os.chdir('temp')

        for i in range(x_small, x_large + 1):
            for j in range(y_small, y_large + 1):

                count += 1
                r = requests.get(url.format(x=i, y=j, z=zoom),
                                 headers=header, cookies=cookie)
                print(r.status_code)
                if 'html' not in str(r):
                    image_save(r, i, j, zoom)
                    print("Location {}_{}_{} download successfully. Left {}"
                          .format(i, j, zoom, total - count))
                    success += 1
                else:
                    print("Location {}_{}_{} is not exist."
                          .format(i, j, zoom))
                r.close()

        return success, total - success


def switch_big2small(a, b):
    if a > b:
        return b, a
    else:
        return a, b


def image_save(data, i, j, zoom):
    image = Image.open(BytesIO(data.content))
    image.save('{}_{}_{}.jpg'.format(i, j, zoom), 'jpeg', quality=100)
    image.close()


def main():

    # 输入经纬度坐标
    lat1 = float(input("输入纬度1："))
    lat2 = float(input("输入纬度2："))
    lon1 = float(input("输入经度1："))
    lon2 = float(input("输入经度2："))
    zoom = int(input("输入缩放倍率（0-21）："))

    # lat1 = float(34.967)
    # lat2 = float(24.25)
    # lon1 = float(112.7)
    # lon2 = float(114.2)
    # zoom = int(6)
    start_time = time.perf_counter()

    x_small, y_small = deg2num.deg2num(lat_large, lon_small, zoom)
    x_large, y_large = deg2num.deg2num(lat_samll, lon_large, zoom)

    x1, y1 = switch_big2small(lat2, lon1, zoom)
    x2, y2 = switch_big2small(lat1, lon2, zoom)

    x_small, x_large = switch_big2small(x1, x2)
    y_small, y_large = switch_big2small(y1, y2)

    # arglist = [x_small, x_large, y_small, y_large, zoom]

    # 记录爬虫程序开始时间


    # success, fail = spider_system.run(spider_system, arglist)
    # 将5个数值传递给爬虫程序开始运行，返回的是成功数和失败数
    success, fail = spider_system.run(
        x_small, x_large, y_small, y_large, zoom)

    # 记录爬虫程序运行结束时间
    end_time = time.perf_counter()

    print("总共耗时{:.2f}秒.".format(end_time - start_time))
    print("下载完成。 {} 个文件下载成功，{}个失败."
          .format(success, fail))


if __name__ == "__main__":
    main()
