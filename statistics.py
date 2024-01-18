import pandas as pd
import numpy as np

class SimpleStatistics:
    # write so that this works on the strava and garmin data
    def __init__(self,data):
        self.data = data
        self.numeric_data = self.data.select_dtypes(include = np.number)
        self.describe = self.numeric_data.describe()

    def get_summary_stats(self):
        return self.describe
        
    def get_max_vals(self, return_only_max_vals = False):
        # returns the activities that resulted in a max val, or a list of all the maximum vales
        # the maximum values
        max_vals = self.describe.loc['max'].astype(int)
        # return a dataframe of the activities that resulted in a maximum
        max_activities = self.data.iloc[self.numeric_data.idxmax()]
        max_activities.insert(0,'Max Value', max_vals.values)
        max_activities.insert(0,'Max Value Type', max_vals.index)
        if return_only_max_vals:
            return max_vals
        else:
            return max_activities

    def get_mean_vals(self):
        return self.describe.loc['mean']

    def get_std_vals(self):
        return self.describe.loc['std']

    def get_min_vals(self):
        return self.describe.loc['min']

    def get_median_vals(self):
        return self.describe.loc['50%']

    def get_kurtosis_vals(self):
        return self.numeric_data.kurtosis()
        
    # return the average of all the numeric values