# !/usr/bin/python
# coding:utf-8

import sys
import cv2
import os, random, glob
from preprocessing_helper import draw_single_char, CANVAS_SIZE, CHAR_SIZE, draw_example_src_only, draw_single_char_by_font
from PIL import Image, ImageEnhance, ImageFont
import numpy as np
from char_info import get_component


img_folder = r"D:\code\calligraphy synthesis\dataset\calliGAN-dataset"  # img_folder: crawler
dst_folder_all = "img_all"  # img_all_cns
dst_folder_cns = "img_all_cns"
src_font = "SimSun.ttf"

def get_char(folder_name):
    char_list = []
    for filename in os.listdir(folder_name):
        if '.gif' in filename:
            char = filename[0]
            char_list.append(char)
    return char_list


def get_union_and_intersect(img_folder, folder_list):
    list0 = get_char(os.path.join(img_folder, folder_list[0]))
    list1 = get_char(os.path.join(img_folder, folder_list[1]))
    list2 = get_char(os.path.join(img_folder, folder_list[2]))
    list3 = get_char(os.path.join(img_folder, folder_list[3]))
    list4 = get_char(os.path.join(img_folder, folder_list[4]))
    list5 = get_char(os.path.join(img_folder, folder_list[5]))
    list6 = get_char(os.path.join(img_folder, folder_list[6]))
    union_list = list(set(list0) | set(list1) | set(list2) | set(list3) | set(list4) | set(list5) | set(list6))
    intersect_list = list(set(list0) & set(list1) & set(list2) & set(list3) & set(list4) & set(list5) & set(list6))
    return union_list, intersect_list


"""
def getSharedCharacter(folder_list, img_folder):
    charDict = dict()
    sharedChar = []
    tmpChar = []
    unionChar = []
    intersectChar = []
    # filenameList = []
    for idx, folder in enumerate(folder_list):
        for filename in os.listdir(os.path.join(img_folder, folder)):
            if '.png' in filename:
                char = filename[0]
                tmpChar.append(char)

                if idx == 0 and char not in charDict:
                    charDict[char] = 1
                elif idx != 0 and char in charDict:
                    charDict[char] += 1
                else:
                    continue

    for idx, (key, value) in enumerate(charDict.items()):
        if value == 7:
            sharedChar.append(key)
    return sharedChar
"""


def select_test_character(intersect_list):
    return random.sample(intersect_list, 1000)


# output image file name: [category]_[count].jpg
def generatePairImg(selectedTestChar, save_folder_all, save_folder_cns, folder_list, img_folder):
    train = save_folder_all + '/train/'
    test = save_folder_all + '/test/'
    train_cns = save_folder_cns + '/train/'
    test_cns = save_folder_cns + '/test/'
    if not os.path.exists(train):
        os.makedirs(train)
    if not os.path.exists(test):
        os.makedirs(test)
    if not os.path.exists(train_cns):
        os.makedirs(train_cns)
    if not os.path.exists(test_cns):
        os.makedirs(test_cns)

    font = ImageFont.truetype(src_font, CHAR_SIZE)
    count_test = 1
    count_train = 1

    for idx, folder in enumerate(folder_list):
        src_folder = os.path.join(img_folder, folder)
        print(src_folder)
        for path in glob.glob(os.path.join(src_folder, '*.gif')):
            filename = path[len(src_folder) + 1:]
            substr = str(filename[0])
            component = get_component(substr)  # this part is for cns code
            if(component == None):
                continue

            try:
                image = Image.open(path)
                # read calligraphy image and modify size
                calli_img = draw_single_char(image, canvas_size=CANVAS_SIZE, char_size=CHAR_SIZE)
                # Add contrast
                contrast = ImageEnhance.Contrast(calli_img)
                calli_img = contrast.enhance(2.)
                # Add brightness
                brightness = ImageEnhance.Brightness(calli_img)
                calli_img = brightness.enhance(2.)

                # get corresponding font image
                # font_img = draw_single_char_by_font(substr, font, CANVAS_SIZE, CHAR_SIZE)
                # im_AB = np.concatenate([font_img, char_img], 1)
                together = draw_example_src_only(substr, font, calli_img, CANVAS_SIZE, CHAR_SIZE)

                if substr in selectedTestChar:
                    together.save(os.path.join(test, "%d_%d.jpg" % (idx, count_test)))
                    together.save(os.path.join(test_cns, "%s_%d_%d.jpg" % (component, idx, count_test)))
                    count_test += 1
                else:
                    together.save(os.path.join(train, "%d_%d.jpg" % (idx, count_train)))
                    together.save(os.path.join(train_cns, "%s_%d_%d.jpg" % (component, idx, count_train)))
                    count_train += 1

            except OSError:
                with open(save_folder_all + '/error_msg.txt', 'a') as f:
                    f.write("cannot open image file %s \n" % (filename))
            except IOError:
                with open(save_folder_all + '/error_msg.txt', 'a') as f:
                    f.write("cannot open image file %s \n" % (filename))

folder_list = ['欧阳询九成宫', '欧阳询皇甫诞', '虞世南', '褚遂良', '柳公权', '颜真卿多宝塔体', '颜真卿颜勤礼碑']
# union_list, intersect_list = get_union_and_intersect(img_folder, folder_list)
# 获取字符的cns码
# f = open("char.txt", "w")
# f.writelines(union_list)
# f.close()

# 获取全部风格都包含的字体
# sharedChar = getSharedCharacter(folder_list, img_folder)
# print(len(sharedChar))
# f = open("sharedChar.txt", "w")
# f.writelines(sharedChar)
# f.close()
# 获取不重复的字符的数据code，选择1000个字符用作test
union_list, intersect_list = get_union_and_intersect(img_folder, folder_list)
print("union_list len: ", len(union_list))
# union_list len:  6548
print("intersect_list len: ", len(intersect_list))
# intersect_list len:  5560

# sharedChar = getSharedCharacter(folder_list, img_folder)
# print(len(sharedChar)) 3857
generatePairImg(selectedTestChar=select_test_character(intersect_list), save_folder_all=dst_folder_all, save_folder_cns=dst_folder_cns, folder_list=folder_list, img_folder=img_folder)

