# !/usr/bin/python
# coding:utf-8

import sys
import cv2
import os, random, glob
from preprocessing_helper import draw_single_char, CANVAS_SIZE, CHAR_SIZE, draw_example_src_only, \
    draw_single_char_by_font
from PIL import Image, ImageEnhance, ImageFont
import numpy as np
from char_info import get_component

def get_char(folder_name):
    char_list = []
    for filename in os.listdir(folder_name):
        if '.png' in filename:
            char = filename[0]
            char_list.append(char)
    return char_list

def get_union(img_folder, folder_list):
    # 获取数据字符
    list0 = get_char(os.path.join(img_folder, folder_list[0]))
    list1 = get_char(os.path.join(img_folder, folder_list[1]))
    list2 = get_char(os.path.join(img_folder, folder_list[2]))
    list3 = get_char(os.path.join(img_folder, folder_list[3]))
    list4 = get_char(os.path.join(img_folder, folder_list[4]))
    list5 = get_char(os.path.join(img_folder, folder_list[5]))
    list6 = get_char(os.path.join(img_folder, folder_list[6]))
    union_list = list(set(list0) | set(list1) | set(list2) | set(list3) | set(list4) | set(list5) | set(list6))

    return union_list


# img_folder = r"D:\code\calligraphy synthesis\CalliGAN\crawler"  # img_folder: crawler
# dst_folder_all = "img_data"  # img_all
# dst_folder_cns = "cns_data"  # img_all_cns
# folder_list = ['歐陽詢-九成宮', '歐陽詢-皇甫誕', '虞世南', '褚遂良', '柳公權', '顏真卿-多寶塔體', '颜真卿-顏勤禮碑']
# union_list = get_union(img_folder, folder_list)
# f = open("char.txt", "w")
# f.writelines(union_list)
# f.close()
# print(len(union_list))
# print(union_list)

f = open("char.txt", "r",encoding='utf-8')
try:
    all_char = f.read()
finally:
    f.close()

# 把网站生成的文件见进行解析
f = open("cns.txt","r")
try:
    all_the_text = f.read()
finally:
    f.close()

# all_the_text = all_the_text.replace('</page><code>', '')
all_the_text = all_the_text.replace('<page>', '')
all_the_text = all_the_text.split('</code>')

f = open("cns_char.txt","w",encoding='utf-8')
i = 0
for cns in all_the_text:
    page = int(cns.split("</page><code>")[0])

    code = cns.split("</page><code>")[1]
    char = all_char[i]
    i = i + 1
    f.writelines(str(page)+'-'+code+'\t'+char+'\n')

f.close()
