#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import cv2
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import copy
import random
import numpy as np
import seaborn as sns
import csv

from IPython.display import HTML
from PIL import Image


# In[2]:


def saveFrames(video_path, dest_path, video_id, all_frames=True):
    cap = cv2.VideoCapture(video_path)
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
#     print ("Number of frames: ", video_length)
    start_time = time.time()
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        out_path = os.path.join(dest_path, video_id + "_%#05d.jpg" % (count + 1))
        if all_frames:
            cv2.imwrite(out_path, frame)
        else:
            if count % 29 == 0:
                cv2.imwrite(out_path, frame)
        count = count + 1
        if (count > (video_length-1)):
            end_time = time.time()
            cap.release()
            break

print("Generating test set")
test_dir = "insert_testset_directory_here"
dest_dir = "insert_output_directory_here"
d = 0
for dir_name in os.listdir(test_dir):
    print("test")
    data_path = os.path.join(test_dir, dir_name)
    if os.path.isdir(data_path):
        for video_name in os.listdir(data_path):
            d += 1
            video_id = video_name[:-4]
            video_path = os.path.join(data_path, video_name)
            dest_path = os.path.join(dest_dir, dir_name)
            os.makedirs(dest_path, exist_ok=True)
            saveFrames(video_path, dest_path, video_id, all_frames=False)
            print(d)


# In[6]:


train_list = []
dest_dir = "insert_output_directory_here"
for dir_name in os.listdir(dest_dir):
    data_path = os.path.join(dest_dir, dir_name)
    if os.path.isdir(data_path):
        for image_name in os.listdir(data_path):
            im_id = image_name[:-4]
            if dir_name == "dangerous":
                train_list.append([im_id, "dangerous"])
            else:
                train_list.append([im_id, "non-dangerous"])


# In[7]:


random.shuffle(train_list)
train_list.insert(0, ["id", "category"])


# In[8]:


train_path = "dir/train.csv"
with open(train_path, "w") as f:
    wr = csv.writer(f, delimiter=",")
    wr.writerows(train_list)


# In[9]:


test_list = []
dest_dir = "insert_test_directory_here"
for dir_name in os.listdir(dest_dir):
    data_path = os.path.join(dest_dir, dir_name)
    if os.path.isdir(data_path):
        for image_name in os.listdir(data_path):
            im_id = image_name[:-4]
            if dir_name == "dangerous":
                test_list.append([im_id, "dangerous"])
            else:
                test_list.append([im_id, "non-dangerous"])


# In[10]:


random.shuffle(test_list)
test_list.insert(0, ["id", "category"])


# In[11]:


test_path = "dir/test-gt.csv"
with open(test_path, "w") as f:
    wr = csv.writer(f, delimiter=",")
    wr.writerows(test_list)


# In[12]:


l1 = []
dest_dir = "insert_train_directory_here"
for image_name in os.listdir(dest_dir):
    im_id = image_name[:-10]
    l1.append(im_id)

myset = set(l1)
print(len(myset))


# In[13]:


l1 = []
dest_dir = "insert_test_directory_here"
for image_name in os.listdir(dest_dir):
    im_id = image_name[:-10]
    l1.append(im_id)

myset = set(l1)
print(len(myset))


# In[ ]:
