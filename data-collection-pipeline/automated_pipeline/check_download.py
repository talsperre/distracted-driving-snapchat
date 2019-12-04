import os
import argparse
import pandas as pd
from copy import deepcopy
from datetime import datetime, timedelta
import subprocess

video_list = os.listdir()

yesterday_date = (datetime.now() - timedelta(1)).strftime('%Y_%m_%d')
yesterday_date_rev = (datetime.now() - timedelta(1)).strftime('%d_%m_%Y')
parser = argparse.ArgumentParser(description="Script to check which videos are corrupt/missing")

parser.add_argument("--video_dir", help="Path to the video dir")
parser.add_argument("--csv_dir", help="Path to the csv dir")
parser.add_argument("--output_dir", help="Path to the output csv dir")

arguments = parser.parse_args()

video_dir = arguments.video_dir
csv_dir = arguments.csv_dir
output_dir = arguments.output_dir

csv_file = os.path.join(csv_dir, yesterday_date + ".csv")
metadata_df = pd.read_csv(csv_file)
missing_df = deepcopy(metadata_df)
missing_df.drop(missing_df.index, inplace=True)

video_dir = os.path.join(video_dir, yesterday_date_rev + "/video")
# video_dir = "/home/shashanks/final_dataset/videos/01_03_2019/video"

video_list = os.listdir(video_dir)
# print(video_list[-1])
count = 0
for index, row in metadata_df.iterrows():
    # print(row['c1'], row['c2'])
    video_id = row["ID"]
    video_path = os.path.join(video_dir, video_id + ".mp4").split("/")[-1]
    # print(video_path)
    if video_path in video_list:
        print(video_path)
        file_output = subprocess.check_output(["file", video_path]).decode("utf-8")
        if "MP4" not in file_output:
            missing_df.loc[count] = metadata_df.loc[index]
            count += 1

output_file = os.path.join(output_dir, yesterday_date + ".csv")

missing_df.to_csv(output_file, encoding='utf-8', index=False)

