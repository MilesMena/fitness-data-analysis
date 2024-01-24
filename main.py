import pandas as pd
from strava_api import StravaAPI
from data_manager import ClusterData
from statistics import Statistics
from plotting import strava_line_metrics_over_time, scatter_plot_kudos_factors,scatter_3d_plot_cluster
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN 



if __name__ == "__main__":

    ################# PULL STRAVA DATA FROM API #######################
        # init the api with the access token
    strava = StravaAPI()
    
    strava_data_pulls = []
    # through trial and error I know I have about 8 pages of data. We could probably automate this but for now this is fine
    page_nums = 8
    # iterate through each page on strava and request the data
    for page_num in range(page_nums):
        strava_data_pulls.append(pd.json_normalize(strava.get_dataset(page_num = page_num + 1)))
        # I don't want to overload my API limits, so I'll give it some time in between requests
        #time.sleep(.5)
    strava_data = pd.concat(strava_data_pulls, ignore_index = True)

    ################# INSERT DATATIME VALUE #######################
    
    strava_data['datetime'] = pd.to_datetime(strava_data['start_date_local'])
    
    ################# SCATTER PLOT OF FACTORS AFFECTING KUDOS #######################

    print(scatter_plot_kudos_factors(strava_data))

    ################# LINE PLOT OF METRICS OVER TIME #######################
    
    print(strava_line_metrics_over_time(strava_data))

    ################# CLUSTER DATA AND PLOT 3D SCATTER #######################


    # build the cluster data
    cluster_cols = ['distance','elev_high','average_heartrate']
    strava_stats = Statistics(strava_data)
    kneedles = strava_stats.get_kneedles(cluster_cols)
    labels = []
    cluster_kneedles =  kneedles[1::8] 
    if kneedles[-1] not in cluster_kneedles:
        cluster_kneedles.append(kneedles[-1])
    
    df = strava_data[strava_data['sport_type'] == 'Run'][cluster_cols].fillna(0).reset_index()
    
    for knee in cluster_kneedles:
        cluster = ClusterData(scaler_name = 'scaler', 
                              scaler = StandardScaler(), cluster_name = 'dbscan', 
                              cluster_method = DBSCAN(eps = knee, min_samples=2*len(cluster_cols)))
        
        labels.append(cluster.get_cluster_lables(df))
    
    eps_labels_df = pd.DataFrame(labels).T
    df = pd.concat([df.reset_index(),eps_labels_df], axis = 1)
    df.rename(columns = {col_num:'Clusters of %.2f'%cluster_kneedles[col_num] for col_num in eps_labels_df.columns}, inplace = True)
    
    print(scatter_3d_plot_cluster(df, cluster_cols, kneedles = cluster_kneedles))

    