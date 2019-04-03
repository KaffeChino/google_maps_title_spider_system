import requests
from PIL import Image
from io import BytesIO
import threading
import multiprocessing


class spider_multithreading(self, spider_system, threading.Thread, arg):
    def __init__(self):
        t = threadng.Thread(target=spider_system.run, args=(spider_system))


class spider_multiprocessing(self, spider_system):
    p = multiprocessing.Process(target=spider_system, args=(arg))


class spider_system():

    def __init__(self, args):

        self.url = 'http://www.google.cn/maps/vt?lyrs=s@821&gl=cn&x={}&y={}&z={}'
        self.headers = {
            'user_agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                           AppleWebKit/537.36 (KHTML, like Gecko) \
                           Chrome/71.0.3578.98 Safari/537.36"}
        # self.arg = [x_small, x_large, y_small, y_large, zoom]
        self.total = (args[1] - args[0])*(args[3] - args[2])
        self.count = 0

    def run(self, args):
        z = args[4]
        # for i in (x_small, x_large):
        for i in (args[0], args[1]):
            # for j in (y_small, y_large):
            for j in (args[2], args[3]):
                try:
                    r = requests.get(url.format(i, j, z),
                                     headers=self.header)
                    
                    image = Image.open(BytesIO(r.content))
                    image.save('{}_{}_{}.jpg'.format(i, j, zoom), 'jpeg')
                except OSError:
                    print("Location {}_{}_{} is not exist.".format(i, j, z))
                    continue
                except:
                    pass
                else:
                    image.close()
                    print("No.", count, "download successfully. Left",
                          total-count, '.')
                finally:
                    r.close()
                    count += 1


class switch_deg_num():

    def deg2num(lat_deg, lon_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) +
                                    (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return (xtile, ytile)

    def num2deg(xtile, ytile, zoom):
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return (lat_deg, lon_deg)


def main():
    lat1 = input("输入纬度1：")
    lat2 = input("输入纬度2：")
    lon1 = input("输入经度1：")
    lon2 = input("输入经度2：")
    zoom = input("输入缩放倍率（0-23）：")
    if lat1 > lat2:
        lat1, lat2 = lat2, lat1
    if lon1 > lon2:
        lon1, lon2 = lon2, lon1
    x_small, y_small = switch_deg_num.deg2num(lat1, lon1, zoom)
    x_large, y_large = switch_deg_num.deg2num(lat2, lon2, zoom)
    arglist = [x_small, x_large, y_small, y_large, zoom]
    spider_system.run(self, arglist)


if __name__ == "__main__":
    main()
