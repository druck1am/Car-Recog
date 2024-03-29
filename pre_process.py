# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import os
import pickle
import random

import cv2 as cv
import numpy as np
import scipy.io
from tqdm import tqdm

from config import im_size


def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def save_train_data(fnames, labels, bboxes):
    src_folder = 'C:/Users/druck/OneDrive/Desktop/Car-Recognition-PyTorch/devkit/cars_train'
    num_samples = len(fnames)

    train_split = 0.8
    num_train = int(round(num_samples * train_split))
    train_indexes = random.sample(range(num_samples), num_train)

    train = []
    valid = []
    print('Save train data...')
    for i in tqdm(range(num_samples)):
        fname = fnames[i]
        label = labels[i]
        (x1, y1, x2, y2) = bboxes[i]

        src_path = os.path.join(src_folder, fname)
        src_image = cv.imread(src_path)
        height, width = src_image.shape[:2]
        # margins of 16 pixels
        margin = 16
        x1 = max(0, x1 - margin)
        y1 = max(0, y1 - margin)
        x2 = min(x2 + margin, width)
        y2 = min(y2 + margin, height)
        # print("{} -> {}".format(fname, label))

        if i in train_indexes:
            dst_folder = 'C:/Users/druck/OneDrive/Desktop/dataTrain'
        else:
            dst_folder = 'C:/Users/druck/OneDrive/Desktop/dataValid'

        dst_path = os.path.join(dst_folder, label)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        dst_path = os.path.join(dst_path, fname)

        crop_image = src_image[y1:y2, x1:x2]
        dst_img = cv.resize(src=crop_image, dsize=(im_size, im_size))
        cv.imwrite(dst_path, dst_img)

        if i in train_indexes:
            train.append({'full_path': dst_path, 'label': (int(label) - 1)})
        else:
            valid.append({'full_path': dst_path, 'label': (int(label) - 1)})

    print('num_train: ' + str(len(train)))
    with open('C:/Users/druck/OneDrive/Desktop/dataTrain.pkl', 'wb') as fp:
        pickle.dump(train, fp)

    print('num_valid: ' + str(len(valid)))
    with open('C:/Users/druck/OneDrive/Desktop/dataValid.pkl', 'wb') as fp:
        pickle.dump(valid, fp)


def save_test_data(fnames, bboxes):
    src_folder = 'C:/Users/druck/OneDrive/Desktop/Car-Recognition-PyTorch/devkit/cars_test'
    dst_folder = 'C:/Users/druck/OneDrive/Desktop/dataTest'
    num_samples = len(fnames)

    print('Save test data...')
    for i in tqdm(range(num_samples)):
        fname = fnames[i]
        (x1, y1, x2, y2) = bboxes[i]
        src_path = os.path.join(src_folder, fname)
        src_image = cv.imread(src_path)
        height, width = src_image.shape[:2]
        # margins of 16 pixels
        margin = 16
        x1 = max(0, x1 - margin)
        y1 = max(0, y1 - margin)
        x2 = min(x2 + margin, width)
        y2 = min(y2 + margin, height)

        dst_path = os.path.join(dst_folder, fname)
        crop_image = src_image[y1:y2, x1:x2]
        dst_img = cv.resize(src=crop_image, dsize=(im_size, im_size))
        cv.imwrite(dst_path, dst_img)


def process_train_data():
    print("Processing train data...")
    cars_annos = scipy.io.loadmat('C:/Users/druck/OneDrive/Desktop/Car-Recognition-PyTorch/devkit/cars_train_annos')
    annotations = cars_annos['annotations']
    annotations = np.transpose(annotations)

    fnames = []
    class_ids = []
    bboxes = []
    labels = []

    for annotation in annotations:
        bbox_x1 = annotation[0][0][0][0]
        bbox_y1 = annotation[0][1][0][0]
        bbox_x2 = annotation[0][2][0][0]
        bbox_y2 = annotation[0][3][0][0]
        class_id = annotation[0][4][0][0]
        labels.append('%04d' % (class_id,))
        fname = annotation[0][5][0]
        bboxes.append((bbox_x1, bbox_y1, bbox_x2, bbox_y2))
        class_ids.append(class_id)
        fnames.append(fname)

    labels_count = np.unique(class_ids).shape[0]
    print(np.unique(class_ids))
    print('The number of different cars is %d' % labels_count)

    save_train_data(fnames, labels, bboxes)


def process_test_data():
    print("Processing test data...")
    cars_annos = scipy.io.loadmat('C:/Users/druck/OneDrive/Desktop/Car-Recognition-PyTorch/devkit/cars_test_annos')
    annotations = cars_annos['annotations']
    annotations = np.transpose(annotations)

    fnames = []
    bboxes = []

    for annotation in annotations:
        bbox_x1 = annotation[0][0][0][0]
        bbox_y1 = annotation[0][1][0][0]
        bbox_x2 = annotation[0][2][0][0]
        bbox_y2 = annotation[0][3][0][0]
        fname = annotation[0][5][0]
        bboxes.append((bbox_x1, bbox_y1, bbox_x2, bbox_y2))
        fnames.append(fname)

    save_test_data(fnames, bboxes)


#if __name__ == '__main__':
    #cars_meta = scipy.io.loadmat('C:/Users/druck/OneDrive/Desktop/Car-Recognition-PyTorch/devkit/cars_meta')
    #class_names = cars_meta['class_names']  # shape=(1, 196)
    #class_names = np.transpose(class_names)
    #print('class_names.shape: ' + str(class_names.shape))
    #print('Sample class_name: [{}]'.format(class_names[8][0][0]))


    #ensure_folder('C:/Users/druck/OneDrive/Desktop/dataTrain')
    #ensure_folder('C:/Users/druck/OneDrive/Desktop/dataValid')
    #ensure_folder('C:/Users/druck/OneDrive/Desktop/dataTest')

    #process_train_data()
    #process_test_data()

    # clean up
    # shutil.rmtree('data/cars_train')
    # shutil.rmtree('data/cars_test')
    # shutil.rmtree('devkit')

    #with open('C:/Users/druck/OneDrive/Desktop/dataTrain.pkl', 'rb') as fp:
        #train = pickle.load(fp)

    #print(train[:10])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
