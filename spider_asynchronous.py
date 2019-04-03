import requests
from PIL import Image
from io import BytesIO
import aiohttp
import asyncio
import math

class aio_spider():
    def __init__(self, *args, **kwargs):

        self.url = 'http://www.google.cn/maps/vt?lyrs=s@821&gl=cn&x={}&y={}&z={}'
        self.headers = {
            # 'X-Requested-With': 'XMLHttpRequest',
            'user_agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                           AppleWebKit/537.36 (KHTML, like Gecko) \
                           Chrome/71.0.3578.98 Safari/537.36"}
        # self.arg = [x_small, x_large, y_small, y_large, zoom]
        self.total = (args[1] - args[0])*(args[3] - args[2])
        self.count = 0

    async def run(self, url):
        pass



class switch_deg_num():

    def deg2num(self, lat_deg, lon_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) +
                                    (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return (xtile, ytile)

    def num2deg(self, xtile, ytile, zoom):
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return (lat_deg, lon_deg)


def main():
    lat1 = input("")
    lat2 = input("")
    lon1 = input("")
    lon2 = input("")
    zoom = input("")
    if lat1 > lat2:
        lat1, lat2 = lat2, lat1
    if lon1 > lon2:
        lon1, lon2 = lon2, lon1
    x_small, y_small = switch_deg_num.deg2num(lat1, lon1, zoom)
    x_large, y_large = switch_deg_num.deg2num(lat2, lon2, zoom)
    arglist = [x_small, x_large, y_small, y_large, zoom]
    # spider_system.run(self, arglist)


if __name__ == "__main__":
    main()
