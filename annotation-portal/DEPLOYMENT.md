# Deployment

## Installation of Required Packages:
- First install ```python3``` and ```virtualenv```
```
virtualenv -p python3 portalenv
source portalenv/bin/activate
pip install -r requirements.txt
```

## Flushing the Previous Database:
```
cd code/annotation-portal/backend/
python manage.py flush
rm -rf db.sqlite3
```

## Migration of the Database:
```
cd code/annotation-portal/backend/
python manage.py migrate
```

## Adding data to the Database:
- The data, i.e. the links to the videos are given in a csv file in the same directory
```
python manage.py shell
```
- A shell prompt would be opened on the terminal
- Now write the commands given below in that prompt
```
Python 3.6.4 |Anaconda, Inc.| (default, Jan 16 2018, 18:10:19) 
[GCC 7.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from upload_videos import fill_database
>>> fill_database("path.csv")
```

## Testing the deployment:
```
python manage.py runserver
```