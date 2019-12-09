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
import pandas as pd
import argparse
import threading

from IPython.display import HTML
from PIL import Image

parser = argparse.ArgumentParser(description="Script to split frames")

parser.add_argument("--video_dir", help="Path to the videos dir")
parser.add_argument("--dest_dir", help="Path to the destination dir")
parser.add_argument("--metadata_csv", help="Path to the csv")

arguments = parser.parse_args()

video_dir = arguments.video_dir
dest_dir = arguments.dest_dir
metadata_csv = arguments.metadata_csv

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def saveFrames(video_path, dest_path, video_id, all_frames=True):
    cap = cv2.VideoCapture(video_path)
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
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

def parsedf(df):
    train_dir = video_dir
    data_path = video_dir
    dest_path = dest_dir
    os.makedirs(dest_path, exist_ok=True)
    d = 0
    for index, row in df.iterrows():
        d += 1
        video_id = row["ID"]
        video_path = os.path.join(data_path, video_id + ".mp4")
        saveFrames(video_path, dest_path, video_id, all_frames=False)
        if d%5000 == 0:
            print(d)      
          

        
file_df = pd.read_csv(metadata_csv)
thread_count = 50
file_split_list = np.array_split(file_df, thread_count)

t = []
for x in range(thread_count):
    t.append(threading.Thread(target=parsedf, args=(file_split_list[x],)))

for x in range(thread_count):
    t[x].start()

for x in range(thread_count):
    t[x].join()
