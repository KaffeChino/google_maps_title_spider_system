import requests
from PIL import Image
from io import BytesIO
# from random import random
import time
import math
import os
import merge
import deg2num


class stack_system():
    """A list-based stack implementation."""
    """一个基于列表的栈的实现."""

    def __init__(self, x_small, x_large, y_small, y_large, zoom):
        """
        _items is a list.
        _size is length of the list.
        You may ask, why not use list(_items)?
        No. In fact, I'm using space exchaging time.
        _items是一个列表。
        _size是这个列表的长度。
        你可能会问，为什么不使用list(_items)?
        不，事实上，我在使用空间换取时间。
        """
        self._items = []
        self._size = 0

        for x in range(x_small, x_large + 1):
            for y in range(y_small, y_large + 1):
                self.push(x, y, zoom)

    def isEmpty(self):
        """
        Check whether the stack is Empty.
        YOU MUST CHECK IT BEFORE YOU USE POP METHOD
        or complete the imlementation in pop()
        DON'T FORGET! OR YOU MAY GET A KEYERROR!
        检查栈是否为空。
        你必须在使用pop()方法之间检查它。
        或者在pop()里实现.
        别忘记了！否则你会得到一个KEY ERROR错误！
        """
        # if len(self) == 0:
        if self._size == 0:
            return True
        else:
            return False

    def __len__(self):
        """
        Return the length of the stack.
        返回栈的长度。
        """
        return self._size

    def push(self, x, y, z):
        """
        Inserts items at top the stack
        -- and in fact that is the end of the list.
        将数据压入栈的顶端
        ——事实上也是列表的尾部。
        """
        self._items.append([x, y, z])
        self._size += 1

    def pop(self):
        """
        Removes and returns the item at top the stack.
        When we push a New item into the stack,
        The item append at the end of the list,
        when use pop method, it will return the end as the same.
        so I used list.pop().
        It will return the last item of the list and delete it.
        移除栈的顶部的数据项并返回该项的值。
        当我们向栈内压入一个新的数据线时，
        新的数据项会被添加到列表的尾端，
        当使用pop()方法时，也会返回列表尾端
        所以我使用了列表的pop()方法。
        它会返回列表的最后一项的数据项然后删除它。
        """
        if self.isEmpty():
            raise KeyError
        x, y, z = self._items.pop()
        self._size -= 1
        return x, y, z

    def peek(self):
        """
        An Interface left for continued development in the future.
        peek() method will return the item at the top of the stack while not delete it.
        一个为未来持续开发留下的接口。
        peek()方法会返回栈的顶部的数据项而不会删除它。
        """
        if self.isEmpty():
            raise KeyError
        x, y, z = self._items[len(self) - 1]
        return x, y, z


class spider_system():
    # @staticmethod
    def __init__(self):
        # self.url = url
        self.url = 'http://www.google.cn/maps/vt?lyrs=s@821&gl=cn&x={x}&y={y}&z={z}'
        self.header = {
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
        self.cookie = requests.get("http://google.cn/maps",
                                   headers=self.header).cookies

    # @classmethod
    def run(self, title_stack):
        # 更改当前文件夹
        os.chdir('temp')
        # count = 0
        success = 0
        while title_stack.isEmpty() is False:
            # count += 1
            x, y, z = title_stack.pop()
            pic_url = self.url.format(x=x, y=y, z=z)
            r = self.spider_core(pic_url)
            if r.status_code == 200:
                self.image_save(r, x, y, z)
                print("Success: {}_{}_{}. Left {}."
                      .format(x, y, z, len(title_stack)))
                success += 1
            elif r.status_code == 404:
                print("Error: Not Exist: {}_{}_{}."
                      .format(x, y, z))
            else:
                print("Error: Donload Failed: {}_{}_{}."
                      .format(x, y, z))

            r.close()

        return success

    def spider_core(self, url):
        r = requests.get(url, headers=self.header, cookies=self.cookie)
        return r

    @staticmethod
    def image_save(data, x, y, zoom):
        image = Image.open(BytesIO(data.content))
        image.save('{}_{}_{}.jpg'.format(x, y, zoom), 'jpeg', quality=100)
        image.close()


class switch_deg_num():
    @staticmethod
    def deg2num(lat_deg, lon_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + (
                     1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return xtile, ytile

    def num2deg(xtile, ytile, zoom):
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return lat_deg, lon_deg


def switch_big2small(a, b):
    if a > b:
        return b, a
    else:
        return a, b


def main():

    lat1 = float(34.967)
    lat2 = float(24.25)
    lon1 = float(112.7)
    lon2 = float(114.2)
    zoom = int(10)

    # lat1 = float(input("输入纬度1："))
    # lat2 = float(input("输入纬度2："))
    # lon1 = float(input("输入经度1："))
    # lon2 = float(input("输入经度2："))
    # zoom = int(input("输入缩放倍率（0-23）："))

    start_time = time.perf_counter()

    lat1, lat2 = switch_big2small(lat1, lat2)
    lon1, lon2 = switch_big2small(lon1, lon2)

    x_small, y_small = deg2num.deg2num(lat2, lon1, zoom)
    x_large, y_large = deg2num.deg2num(lat1, lon2, zoom)

    total = int((x_large - x_small + 1) * (y_large - y_small + 1))

    title_stack = stack_system(x_small, x_large, y_small, y_large, zoom)

    spider = spider_system()
    success = spider.run(title_stack)

    end_time = time.perf_counter()

    print("Total cost {:.2f} seconds.".format(end_time - start_time))
    print("Download Over. {} item(s) secceed and {} failed."
          .format(success, total - success))

    anwer = input('Do you want to merge these pictures? Y/N')
    if anwer == 'Y' or 'y':
        merge.merge(x_small, x_large, y_small, y_large, zoom)
    else:
        exit()


if __name__ == "__main__":
    main()
