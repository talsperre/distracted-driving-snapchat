import os
from datetime import datetime, timedelta
import shutil
import requests

yesterday_date = (datetime.now() - timedelta(1)).strftime('%d_%m_%Y')

headers = {
    'Content-type': 'application/json'
}

tarfile = "/home/shashanks/final_dataset/tar/17_03_2019.tar"
video_dir = "/home/shashanks/final_dataset/videos/17_03_2019"

# tarfile = os.path.join("/home/shashanks/final_dataset/tar", yesterday_date + ".tar")
# video_dir = os.path.join("/home/shashanks/final_dataset/videos", yesterday_date)

try:
    os.remove(tarfile)
except:
    print("Tar file doesn't exist")

try:
    shutil.rmtree(video_dir)
except:
    print("Video directory doesn't exist")

data = {"text":"All operations for yesterday are done, cleanup also complete."}
response = requests.post('https://hooks.slack.com/services/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', headers=headers, data=str(data))
