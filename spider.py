import requests
from PIL import Image
from io import BytesIO
# from random import random
import time
import math
import os


class spider_system():

    def run(x_small, x_large, y_small, y_large, zoom):

        # 定义Cookies， header， 下载计数器count，总成功下载数success
        # 计算总图块数量total
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
        # self.arg = [x_small, x_large, y_small, y_large, zoom]
        # total = int((arg[1] - args[0] + 1) * (args[3] - args[2] + 1))
        total = int((x_large - x_small + 1) * (y_large - y_small + 1))
        count = 0
        # zoom = int(args[4])
        success = 0

        # 更改当前文件夹
        os.chdir('temp')

        for i in range(x_small, x_large + 1):
            # for i in (args[0], args[1]):
            for j in range(y_small, y_large + 1):
                # for j in (args[2], args[3]):

                # sleep_random = random() * 10
                # print("Sleep {:.2f} second(s).".format(sleep_random))
                # time.sleep(sleep_random)

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
                    print("Location {}_{}_{} is not exist.".format(i, j, zoom))
                r.close()

        return success, total - success


class switch_deg_num():
    @staticmethod
    def deg2num(lat_deg, lon_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(
            math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return (xtile, ytile)

    def num2deg(xtile, ytile, zoom):
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return (lat_deg, lon_deg)


def switch_big2small(a, b):
    if a > b:
        return b, a
    else:
        return a, b


def image_save(data, i, j, zoom):
    image = Image.open(BytesIO(data.content))
    image.save('{}_{}_{}.jpg'.format(i, j, zoom), 'jpeg')
    image.close()


def main():
    # lat1 = float(input("输入纬度1："))
    # lat2 = float(input("输入纬度2："))
    # lon1 = float(input("输入经度1："))
    # lon2 = float(input("输入经度2："))
    # zoom = int(input("输入缩放倍率（0-23）："))

    lat1 = float(34.967)
    lat2 = float(24.25)
    lon1 = float(112.7)
    lon2 = float(114.2)
    zoom = int(5)

    lat1, lat2 = switch_big2small(lat1, lat2)
    lon1, lon2 = switch_big2small(lon1, lon2)

    x_small, y_small = switch_deg_num.deg2num(lat2, lon1, zoom)
    x_large, y_large = switch_deg_num.deg2num(lat1, lon2, zoom)

    # arglist = [x_small, x_large, y_small, y_large, zoom]

    start_time = time.perf_counter()

    # success, fail = spider_system.run(spider_system, arglist)
    success, fail = spider_system.run(
        x_small, x_large, y_small, y_large, zoom)

    end_time = time.perf_counter()

    print("Total cost {:.2f} seconds.".format(end_time - start_time))
    print("Download Over. {} item(s) secceed and {} failed.".format(success, fail))


if __name__ == "__main__":
    main()
