import re
import os
# import spider
from PIL import Image
import deg2num


def scan():
    pic_number_list = []
    for name in os.listdir():
        pic_number_list.append(re.findall(r'\d+', name))
    x_list = []
    y_list = []
    z_list = []
    for item in pic_number_list:
        x_list.append(item[0])
        y_list.append(item[1])
        z_list.append(item[2])

    if max(z_list) == min(z_list):
        x_max = max(x_list)
        x_min = min(x_list)
        y_max = max(y_list)
        y_min = min(y_list)
        return x_min, x_max, y_min, y_max, z_list[0]
    else:
        print("Fonlder has pic of else zoom. Delete orthers you don't need.")


def input_num():
    # x1 = int(input())
    # x2 = int(input())
    # y1 = int(input())
    # y2 = int(input())
    # z = int(input())

    x1 = 832
    x2 = 836
    y1 = 405
    y2 = 408
    z = 10
    # x1, x2 = spider.switch_big2small(x1, x2)
    # y1, y2 = spider.switch_big2small(y1, y2)
    return x1, x2, y1, y2, z


def merge(x_small, x_large, y_small, y_large, z):
    image_name = "{}_{}_{}.jpg"
    x_size = x_large - x_small + 1
    y_size = y_large - y_small + 1
    merge_pic = Image.new('RGB', (x_size * 256, y_size * 256))
    for x in range(x_size):
        for y in range(y_size):
            pic = Image.open(image_name.format(x + x_small, y + y_small, z))
            merge_pic.paste(pic, (x * 256, y * 256))
    merge_pic.save('Merge_{}.jpg'.format(z))
    print("Merge Success.")
    lat_top, lon_left = deg2num.num2deg(x_small, y_large, z)
    lat_bottom, lon_right = deg2num.num2deg(x_large + 1, y_small + 1, z)
    print("左上坐标：{:.2f} N, {:.2f} E".format(lat_top, lon_left))
    print("右上坐标：{:.2f} N, {:.2f} E".format(lat_top, lon_right))
    print("左下坐标：{:.2f} N, {:.2f} E".format(lat_bottom, lon_left))
    print("右下坐标：{:.2f} N, {:.2f} E".format(lat_bottom, lon_left))


def main():
    os.chdir('temp')
    x_small, x_large, y_small, y_large, z = input_num()

    # title_stack = spider.stack_system(x_small, x_large, y_small, y_large, z)
    merge(x_small, x_large, y_small, y_large, z)


if __name__ == "__main__":
    main()
