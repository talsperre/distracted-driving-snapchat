from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import time
import argparse
import requests
from datetime import datetime, timedelta

yesterday_date = (datetime.now() - timedelta(1)).strftime('%d_%m_%Y')

headers = {
    'Content-type': 'application/json'
}

parser = argparse.ArgumentParser(description="Script to upload a tar file to Google Drive")

parser.add_argument("--tar_dir", help="Path to the tar dir")

arguments = parser.parse_args()

tar_dir = arguments.tar_dir

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("/home/shashanks/Projects/Independent-Project/deploy/gdrive_scripts/mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    # gauth.LocalWebserverAuth()
    gauth.CommandLineAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("/home/shashanks/Projects/Independent-Project/deploy/gdrive_scripts/mycreds.txt")

drive = GoogleDrive(gauth)

PARENT_ID = "1M3iQyYNqmeMZPkngDQM_8Y9J3mE1g8zJ"
f = os.path.join(tar_dir, yesterday_date + ".tar")
# f = "/home/shashanks/final_dataset/tar/07_03_2019.tar"

start_time = time.time()
print("start_time: ", time.strftime("%Y_%m_%d_%H_%M"))
print("File transferred: ", f)

data = {"text":"Currently uploading videos from " + yesterday_date + " to the Drive folder"}
# data = {"text":"Now testing the Drive upload process. Currently uploading 07-03-2019"}
response = requests.post('https://hooks.slack.com/services/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', headers=headers, data=str(data))

# new_file = drive.CreateFile({"parents": [{"id": PARENT_ID}], "mimeType":"text/plain"})
new_file = drive.CreateFile({"parents": [{"id": PARENT_ID}], "mimeType":'application/tar'})
new_file.SetContentFile(f)
new_file.Upload()

data = {"text":"Done uploading videos from " + yesterday_date}
# data = {"text":"Done uploading videos from 07-03-2019. Note the timestamps"}
response = requests.post('https://hooks.slack.com/services/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', headers=headers, data=str(data))

