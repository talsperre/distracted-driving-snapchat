curl -X POST -H 'Content-type: application/json' --data '{"text":"ASLI Begin"}' https://hooks.slack.com/services/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

/home/shashanks/Projects/torchenv/bin/python /home/shashanks/Projects/Independent-Project/deploy/manual_pipeline/download_videos.py --csv /home/shashanks/final_dataset/csv_logs/csvs/2019_03_17.csv --dest_dir /home/shashanks/final_dataset/videos/

/home/shashanks/Projects/torchenv/bin/python /home/shashanks/Projects/Independent-Project/deploy/manual_pipeline/tar_folder.py --video_dir /home/shashanks/final_dataset/videos/ --output_dir /home/shashanks/final_dataset/tar/
if [ $? -eq 0 ]; then
    echo OK
else
    curl -X POST -H 'Content-type: application/json' --data '{"text":"Building tar encountered an error"}' https://hooks.slack.com/services/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
fi

/home/shashanks/Projects/torchenv/bin/python /home/shashanks/Projects/Independent-Project/deploy/manual_pipeline/gdrive_scripts/test_upload.py --tar_dir /home/shashanks/final_dataset/tar/
if [ $? -eq 0 ]; then
    echo OK
else
    curl -X POST -H 'Content-type: application/json' --data '{"text":"Uploading tar encountered an error"}' https://hooks.slack.com/services/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
fi

/home/shashanks/Projects/torchenv/bin/python ~/Projects/Independent-Project/deploy/manual_pipeline/cleanup.py
if [ $? -eq 0 ]; then
    echo OK
else
    curl -X POST -H 'Content-type: application/json' --data '{"text":"Cleaning up failed"}' https://hooks.slack.com/services/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
fi

curl -X POST -H 'Content-type: application/json' --data '{"text":"ASLI End"}' https://hooks.slack.com/services/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
