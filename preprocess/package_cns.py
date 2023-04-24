# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

import argparse
import glob
import os
import _pickle as pickle
import random


def pickle_examples(paths, train_path, val_path, train_val_split=0.1):
    """
    Compile a list of examples into pickled format, so during
    the training, all io will happen in memory
    """
    with open(train_path, 'wb') as ft:
        with open(val_path, 'wb') as fv:
            for p in paths:
                cns_code = os.path.basename(p).split("_")[0]
                label = int(os.path.basename(p).split("_")[1])
                with open(p, 'rb') as f:
                    if cns_code == 'None':
                        print("None alert! ")
                        continue

                    print("img %s" % p, label)
                    print("cns code: ", cns_code)
                    img_bytes = f.read()
                    r = random.random()
                    example = (cns_code, label, img_bytes)
                    if r < train_val_split:
                        pickle.dump(example, fv)
                    else:
                        pickle.dump(example, ft)


parser = argparse.ArgumentParser(description='Compile list of images into a pickled object for training')
parser.add_argument('--dir', dest='dir', default=r"D:\code\calligraphy synthesis\CalliGAN\preprocess\img_all_cns\train",help='path of examples')
parser.add_argument('--save_dir', dest='save_dir',default="D:\code\calligraphy synthesis\CalliGAN\output\data",  help='path to save pickled files')
parser.add_argument('--split_ratio', type=float, default=0.1, dest='split_ratio',
                    help='split ratio between train and val')
args = parser.parse_args()

'''''
从数据文件夹中，导入图片进行train和test区分，同时提取cns_code、label、img
'''''
if __name__ == "__main__":
    if not os.path.isdir(args.save_dir):
        os.mkdir(args.save_dir)
    train_path = os.path.join(args.save_dir, "cns_train.obj")
    val_path = os.path.join(args.save_dir, "cns_test.obj")
    pickle_examples(sorted(glob.glob(os.path.join(args.dir, "*.jpg"))), train_path=train_path, val_path=val_path,
                    train_val_split=args.split_ratio)
