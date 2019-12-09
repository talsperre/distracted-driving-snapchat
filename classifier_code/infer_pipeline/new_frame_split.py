import os
import argparse
import time
import datetime
import json
import subprocess
import cv2
import random
import threading
import pandas as pd
import numpy as np

from pprint import pprint

parser = argparse.ArgumentParser(description="Script to Automate Classification Process")

parser.add_argument("--csv", help="Path to the metadatadir")
parser.add_argument("--dest_dir", help="Path to the destination dir")

arguments = parser.parse_args()

csv_file = arguments.csv
dest_dir = arguments.dest_dir

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def saveFrames(video_path, dest_path, video_id, all_frames=False):
    cap = cv2.VideoCapture(video_path)
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print ("Number of frames: ", video_length)
    start_time = time.time()
    count = 0
    actual_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        out_path = os.path.join(dest_path, video_id + "_%#05d.jpg" % (count + 1))
        if all_frames:
            cv2.imwrite(out_path, frame)
            actual_count += 1
        else:
            if count % 29 == 0:
                cv2.imwrite(out_path, frame)
                actual_count += 1
        count = count + 1
        if (count > (video_length-1)):
            end_time = time.time()
            cap.release()
            print ("Done extracting frames.\n%d frames extracted" % actual_count)
            print ("It took %d seconds for conversion." % (end_time - start_time))
            break

def downloadVideos(df):
    for i, row in df.iterrows():
        try:
            print(i, row)
            url = row['url'] + "media.mp4"
            scraped_date = "missing_videos"
            new_video_dir = os.path.join(dest_dir, scraped_date, "video")
            new_one_frame_dir = os.path.join(dest_dir, scraped_date, "one_frame_per_sec")

            os.makedirs(new_video_dir, exist_ok=True)
            os.makedirs(new_one_frame_dir, exist_ok=True)

            download_path = os.path.join(new_video_dir, row["id"] + ".mp4")

            subprocess.run(["wget", url, "-O", download_path])
            saveFrames(download_path, new_one_frame_dir, row["id"], all_frames=False)

        except Exception as e:
            print("Exception e: ", str(e))


file_df = pd.read_csv(csv_file)

# random.shuffle(file_list)
thread_count = 40
# file_split_list = list(split(file_list, thread_count))
file_split_list = np.array_split(file_df, thread_count)
print(len(file_split_list))

t = []
for x in range(thread_count):
    print("-"*100)
    # print(file_split_list[x])
    t.append(threading.Thread(target=downloadVideos, args=(file_split_list[x],)))

for x in range(thread_count):
    t[x].start()

for x in range(thread_count):
    t[x].join()

# both threads completely executed
print("Done!")
