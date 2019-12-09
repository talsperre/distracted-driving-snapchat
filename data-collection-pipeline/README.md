# Data collection pipeline

The scraper collects code from over 170 cities all over the world and, as a result, an average of 180GB of data is collected daily. 

The scripts in this folder aim to streamline the process of data collection by providing methods/code for:
1. Downloading videos
2. Checking for completeness
3. Uploading to Google drive

### Running the pipeline

To run the data collection code:

```
bash pipeline.sh
```

### Slack Updates

In order to get daily updates about the data scraped, we create webhooks to slack and post information about data collection to a private slack channel. In order to do the same, one just needs to change the slack webhook url in the `pipeline.sh` file. 

Replace the below url with your own unique url.
```
https://hooks.slack.com/services/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
```

In order to create new webhooks / slack apps, please follow the tutorial mentioned [here](https://api.slack.com/messaging/webhooks).

### Google Drive Scripts

The data collected faily via the scraper is around 180GB in size when converted to a `.tar` file. Thus, it is difficult to store the data on the server. We thus, create scripts to upload and download data from a google drive account. 

The only requirement for using the google-drive scripts is that the user is required to create a new application and provide the `client_secrets.json` file in the `gdrive_scripts` folder. Instructions for creating the API key and `client_secrets.json` file are given [here](https://developers.google.com/adwords/api/docs/guides/authentication). Apart from creating an app and corresponding keys, you must also enable googledrive API for the particular app. 

There are two scripts provided in the `gdrive_scripts` folder: `test_upload.py` and `test_download.py` that can upload/download content from google drive respectively. 
