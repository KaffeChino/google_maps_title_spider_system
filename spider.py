import requests
from PIL import Image
from io import BytesIO
import time
import math


class spider_system():

    def run(x_small, x_large, y_small, y_large, zoom):
        url = 'http://www.google.cn/maps/vt?lyrs=s@821&gl=cn&x={x}&y={y}&z={z}'
        header = {
            'user_agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                           AppleWebKit/537.36 (KHTML, like Gecko) \
                           Chrome/71.0.3578.98 Safari/537.36"}
        # self.arg = [x_small, x_large, y_small, y_large, zoom]
        # total = int((arg[1] - args[0] + 1) * (args[3] - args[2] + 1))
        total = int((x_large - x_small + 1) * (y_large - y_small + 1))
        count = 0
        # zoom = int(args[4])
        success = 0

        for i in (x_small, x_large):
        # for i in (args[0], args[1]):
            for j in (y_small, y_large):
            # for j in (args[2], args[3]):
                try:
                    count += 1
                    r = requests.get(url.format(x=i, y=j, z=zoom),
                                     headers=header)
                    image_save(r, i, j, zoom)
                    r.close()
                except OSError:
                    print("Location {}_{}_{} is not exist.".format(i, j, zoom))
                    continue
                else:
                    success += 1
                    print("No.", count, "download successfully. Left", total - count)

        return success, total - success


class switch_deg_num():

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
        a, b = b, a


def image_save(data, i, j, zoom):
    image = Image.open(BytesIO(data.content))
    image.save('{}_{}_{}.jpg'.format(i, j, zoom), 'jpeg')
    image.close()


def main():
    lat1 = float(input("输入纬度1："))
    lat2 = float(input("输入纬度2："))
    lon1 = float(input("输入经度1："))
    lon2 = float(input("输入经度2："))
    zoom = int(input("输入缩放倍率（0-23）："))

    # switch_big2small(lat1, lat2)
    # switch_big2small(lon1, lon2)

    x_small, y_small = switch_deg_num.deg2num(lat2, lon1, zoom)
    x_large, y_large = switch_deg_num.deg2num(lat1, lon2, zoom)

    switch_big2small(x_small, x_large)
    switch_big2small(y_small, y_large)

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
