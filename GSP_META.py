import exifread
import json
import pandas as pd
from tqdm import tqdm
from datetime import datetime, date

f = open('IMG_1545.CR2', 'rb')

# Return Exif tags
tags = exifread.process_file(f)

dic = {
    'Image DateTime': tags['Image DateTime'],
    'Image GPSInfo': tags['Image GPSInfo'],
    'GPS GPSVersionID': tags['GPS GPSVersionID'],
    'EXIF DateTimeOriginal': tags['EXIF DateTimeOriginal'],
    'img_GPSLatitudeRef': tags['GPS GPSLatitudeRef'],
    'img_GPSLatitude': tags['GPS GPSLatitude'],
    'img_GPSLongitudeRef': tags['GPS GPSLongitudeRef'],
    'img_GPSLongitude': tags['GPS GPSLongitude'],
    'img_GPSTimeStamp': tags['GPS GPSTimeStamp'],
    'img_GPSMapDatum': tags['GPS GPSMapDatum']
}


# for keys, values in dic.items():
#    print(keys, ' ', values)

class GoogleMaps:
    def __init__(self):
        self.data_locations = ''
        self.dt = pd.DataFrame()



    def import_jason(self,file_name):
        with open(file_name) as json_file:
            data = json.load(json_file)
            self.data_locations = data['locations']
        return self.data_locations


    def to_pandas(self,date_start, date_end, output):
        start_date = datetime.strptime(date_start, '%Y-%m-%d')
        end_date = datetime.strptime(date_end, '%Y-%m-%d')
        for i in tqdm(self.data_locations, desc='Creating database'):
            date_maps = datetime.fromtimestamp(int(i['timestampMs']) / 1000)
            if start_date <= date_maps <= end_date:
                temp_df = pd.DataFrame(i)
                self.dt = self.dt.append(temp_df, ignore_index=True)
        print(temp_df.head())
        print(self.dt.head())

        self.dt['datetime'] = pd.to_numeric(self.dt['timestampMs'], errors='coerce')
        for i in tqdm(range(self.dt.shape[0]), desc='Converting Date'):
            try:
                self.dt['datetime'][i] = datetime.fromtimestamp(float(self.dt['datetime'][i]) / 1000).strftime('%d-%m-%Y %H:%M:%S')
            except:
                self.dt['datetime'][i] = datetime.strptime('9999-12-31', '%d-%m-%Y %H:%M:%S')
        dt = self.dt[['altitude', 'latitudeE7', 'longitudeE7', 'datetime']]
        print(self.dt.head())
        self.dt.to_csv(output, sep=';')
        return self.dt


if __name__ == '__main__':
    base = GoogleMaps()
    base.import_jason('LOC.json')
    base.to_pandas('2019-03-17', '2019-03-17', 'out.csv')
