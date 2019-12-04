import csv
import sys
from videos.models import Video

def fill_database(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            row_split = row[0].split("/")
            id = row_split[2][:-4] 
            path=row[0]
            try:
                Video.objects.create(VideoID=id[:-4], path = path)
            except:
                print("Duplicate Entry")
