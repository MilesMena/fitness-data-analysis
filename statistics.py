import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from kneed import KneeLocator

class Statistics:
    # write so that this works on the strava and garmin data
    def __init__(self,data):
        self.data = data
        self.numeric_data = self.data.select_dtypes(include = np.number)
        
        self.describe = self.numeric_data.describe()
        
    def get_numeric(self):
        return self.numeric_data
        
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

    def get_correlation(self, method = 'pearson'):
        return self.numeric_data.corr(method)

    def get_autocorrelation(self, lag = 1):
        # how much is the series related to its shifted self
        auto = {}
        for col in self.numeric_data:
           auto[col] = self.numeric_data[col].autocorr(lag)
        return auto

    
    def get_kneedles(self, cluster_cols, activity_type = 'Run', plot = False ):
        # filter the data
        df = self.data[self.data['sport_type'] == activity_type][cluster_cols].fillna(0)
        

        # scale the data 
        df_scaled= StandardScaler().fit_transform(df)

        # get k nearest neighbors
        neighbors = NearestNeighbors(n_neighbors=2* df.shape[1]) #minPts recommended to be 2 * dim
        neighbors_fit = neighbors.fit(df_scaled)
        neigh_dist, neigh_ind  = neighbors_fit.kneighbors(df_scaled)

        # sort the neighbor distances (lengths to points) in ascending order
        # axis = 0 represents sort along first axis i.e. sort along row
        sort_neigh_dist = np.sort(neigh_dist, axis = 0)

        
        k_dist =sort_neigh_dist[:,2 * df_scaled.shape[1]- 1]

        #kneedle = KneeLocator(x = indices, y = , S = 1.0, curve = "concave", direction = "increasing", online=True)
        kneedle = KneeLocator(x = range(1, len(neigh_dist)+1), y = k_dist, S = 1, 
                              curve = "concave", direction = "increasing", online=True)

        if plot:
             kneedle.plot_knee()
            # Show the plot
            #plt.show()
        
        return kneedle.all_knees_y
   
        
       




