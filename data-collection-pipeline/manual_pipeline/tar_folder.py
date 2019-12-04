import tarfile
import os
import argparse
import time
import requests
from datetime import datetime, timedelta
import subprocess

headers = {
    'Content-type': 'application/json'
}

parser = argparse.ArgumentParser(description="Script to tar a folder")

parser.add_argument("--video_dir", help="Path to the video tar file")
parser.add_argument("--output_dir", help="Path to the output dir")

arguments = parser.parse_args()

video_dir = arguments.video_dir
output_dir = arguments.output_dir


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

filename = "/home/shashanks/final_dataset/tar/17_03_2019.tar"
input_file = "/home/shashanks/final_dataset/videos/17_03_2019/video"

# data = {"text":"Currently tarring videos from " + yesterday_date}
data = {"text":"Now testing the tarring process. Currently tarring 17-03-2019"}
response = requests.post('https://hooks.slack.com/services/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', headers=headers, data=str(data))

make_tarfile(filename, input_file)

# data = {"text":"Completed tarring videos from " + yesterday_date}
data = {"text":"Tarring test complete. Note timestamps"}
response = requests.post('https://hooks.slack.com/services/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', headers=headers, data=str(data))

md5sum = subprocess.check_output(["md5sum", filename]).decode("utf-8")

with open("/home/shashanks/final_dataset/md5_log.txt", "a") as myfile:
    myfile.write(md5sum)
