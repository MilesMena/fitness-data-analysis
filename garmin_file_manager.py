import pandas as pd
import re

class GarminDataManager:
    # Implement reading in multiple files from the directory
    def __init__(self, data):
        self.data = data


class CleanData:
    # Implement data cleaning logic 

    # specifying the columns that run into this issue won't work, but it varies by who the athlete is
    comma_cols = ['Calories','Total Ascent','Total Descent', 'Min Elevation', 'Max Elevation']
    dashed_cols = ['Total Ascent', 'Total Descent', 'Min Elevation',  'Max Elevation','Avg Pace', 'Best Pace', 'Calories']
    
    def __init__(self, data, activity_types = ['Running']):
    # Call the constructor
        self.data = data
        # drop rows with all missing values
        self.data = self.data.dropna(how = 'all').reset_index().drop('index', axis = 1) 
        # keep data that is of an activitiy type
        self.data = self.data[self.data['Activity Type'].isin(activity_types)]
        # convert columns to datetime
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        # remove '--' from columns that have it (run before cleaning others)
        for col in self.data:
        # print(dash_col)
            self.data[col] = self.data[col].replace('--','0') 
        for col in self.comma_cols:
            #print(col)
            self.data[col] = self.data[col].apply(lambda x: int(re.sub(',', '', x)))
            
        # reset index
        self.data = self.data.reset_index(drop = True)
        
            
    # I don't think we are going to need these function, but let's keep them for now  
    def drop_rows_with_missing_values(self):
        # drop rows with all missing values
        return self.data.dropna(how = 'all').reset_index().drop('index', axis = 1)
    def keep_activities(self, activity_types):
        # keep data that is of an activitiy type
        return self.data[self.data['Activity Type'].isin(activity_types)]
    def remove_duplicate_entries(self):
        # remove duplicate entries
        return self.data.drop_duplicates(subset=None, keep='first', inplace=False)
    def convert_columns_to_datetime(self):
        # convert columns to datetime
        return pd.to_datetime(self.data['Date'])
    def remove_commas(self, var):
        # remove commas
        return self.data[var].apply(lambda x: int(re.sub(',', '', x))) 
    def remove_dashes(self,var):
        # remove dashes --
        return self.data[var].replace('--','0')
        
class WrangleData:
    time_cols = [ 'Time', 'Best Lap Time','Moving Time', 'Elapsed Time']
    pace_cols = ['Avg Pace','Best Pace']
    # Implement data wrangling logic 
    def __init__(self, data):
        # Call the constructor of the parent class
        self.data = data
        # convert time columns to seconds
        for col in self.time_cols:
            self.data[col] = self.data[col].apply(self.split_time)
        for col in self.pace_cols:
            self.data[col] = self.data[col].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]) if x.count(':') == 1 else int(x.split('.')[0])) 
        # create more columns from date columns (day, hour, minute, etc...)
        self.data['Day'] = self.data['Date'].dt.day_name()
        self.data['Hour'] = self.data['Date'].dt.hour
        self.data['Minute'] = self.data['Date'].dt.minute  # splitting the minute and hour might confuse the ML model. That's a question for Dr. Al-Khassaweneh
        self.data['Weekday'] = self.data['Date'].dt.weekday
        self.data['Calendar Date'] = self.data['Date'].dt.date


    
    def split_time(self,x):
        # Split Time by the formats used 00:00:00, 00:00.0, 00:00.00.0, 00:00:00.00.0    01:06:37.99.9
        if x.count('.') == 1:
            time = x.split(':')
            return float(time[0]) * 60 + float(time[1])
        elif  x.count('.') == 2:
            if x.count(':') == 1:
                time = x.split(':')[1].split('.')
                return float(time[0]) * 60 + float(time[1])
            elif x.count('.') == 2:
                time = x.split(':')
                mins = time[-1].split('.')
                return float(time[0]) * 24 * 60 * 60 + float(time[1]) * 60 * 60 + float(mins[0]) * 60 + float(mins[1])
        else:
            time = x.split(':')
            return float(time[0]) * 60 **2 + float(time[1]) * 60 + float(time[2]) 

    # convert seconds columns to time
    # feature engineering
        