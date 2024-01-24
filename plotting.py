import plotly.express as px
import pandas as pd
import chart_studio.plotly as py


# Strava plotting
def strava_line_metrics_over_time(data):
    strava_cols = ['distance', 'moving_time', 'elapsed_time',
           'total_elevation_gain', 'achievement_count', 'kudos_count', 'comment_count', 
             'average_speed', 'max_speed', 'average_cadence',
           'average_temp', 'average_heartrate', 'max_heartrate', 'elev_high',
           'elev_low', 'pr_count'] + ['datetime']
    
    df = data[data['sport_type'] == 'Run'][strava_cols]
    
    fig = px.line(df, x = 'datetime', y = 'distance', title = '%s Metrics over Time'%('Run')) #, color = 'Weekday')
    
    buttons = []
    for column in df.columns:
        if column != 'datetime':
            button = dict(label=column, method='update', args=[{'y': [df[column]]}])
            buttons.append(button)
        
    fig.update_layout(yaxis={'title': None, 'showticklabels': True}, margin=dict(l=0, r=0, t=40, b=0),width = 1000, height=400,
                     updatemenus= [
                dict(type = 'dropdown', x = -.02, y = 1, buttons= buttons)]) 
    
    link =  py.plot(fig, filename = 'strava-line-metrics-over-time', auto_open=False)
    return link


# Garmin Plotting 
def garmin_line_metrics_over_time(data):
    activity_type,var = 'Running', 'Distance'
    garmin_cols = ['Distance', 'Calories', 'Time', 'Avg HR', 'Max HR', 'Avg Pace',
           'Best Pace', 'Total Ascent', 'Total Descent', 'Avg Stride Length',
           'Avg Vertical Ratio', 'Avg Vertical Oscillation',
           'Avg Ground Contact Time', 'Training Stress Score®', 'Avg Power',
           'Max Power', 'Grit', 'Flow', 'Avg. Swolf', 'Avg Stroke Rate',
           'Min Temp', 'Best Lap Time', 'Number of Laps', 'Max Temp',
           'Moving Time', 'Elapsed Time', 'Min Elevation', 'Max Elevation', 'Hour',
           'Minute', 'Weekday'] + ['Calendar Date']
    
    df = data[data['Activity Type'] == 'Running'][garmin_cols]
    
    fig = px.line(df, x = 'Calendar Date', y = 'Distance', title = '%s Metrics over Time'%(activity_type)) #, color = 'Weekday')
    
    buttons = []
    for column in garmin_cols:
        if column != 'Calendar Date':
            button = dict(label=column, method='update', args=[{'y': [df[column]]}]
            )
            buttons.append(button)
        
    fig.update_layout(yaxis={'title': None, 'showticklabels': True},margin=dict(l=0, r=0, t=40, b=0),width = 1000, height=400,
                     updatemenus= [
                dict(type = 'dropdown', x = -.02, y = 1, buttons= buttons)]) 
    
    #
    
    link = py.plot(fig, filename = 'garmin-line-metrics-over-time', auto_open=False)
    #fig.show()
    
    return link


def scatter_plot_kudos_factors(data):
    scatter_cols = ['distance', 'moving_time', 'elapsed_time','total_elevation_gain', 'achievement_count',
            'comment_count', 'athlete_count','average_temp', 'average_heartrate','max_heartrate', 'elev_high',
            'pr_count', 'total_photo_count','elev_low']
    
    activity_type = 'Run'
    
    df = data[data['sport_type'] == activity_type]
    
    fig = px.scatter(df,y = 'kudos_count',x = 'distance',color =  'total_elevation_gain' , hover_name = 'name') 
    
    x_buttons = []
    for column in scatter_cols: 
        button = dict(label=column,method='update',args=[{ 'x': [df[column]]}, {'xaxis': {'title': column}}])
        x_buttons.append(button)
    
    color_buttons = []
    for column in scatter_cols: 
        button = dict(label=column, method='update',
            args=[{'marker.color': [df[column]], 'coloraxis.colorscale': 'Viridis'},
                {'coloraxis': {'cmin': df[column].min(), 'cmax': df[column].max(),'colorbar': {'title': {'text': column}}}}
            ]
        )
        color_buttons.append(button)
    
    size_buttons = []
    for column in scatter_cols: #ss_strava.get_numeric().columns:
        button = dict(label=column,method='update',
            args=[{'marker.size': [df[column]], 'marker.sizemode': 'area', 'marker.sizeref': df[column].max() / 1000 } ])
        size_buttons.append(button)
        
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0),width = 800, height=400,
                title=dict(text="Factors in Kudos ", x=0.5, y=0.95, xanchor="center", yanchor="top"),
                      
                     updatemenus= [
                dict(type = 'dropdown',x = -.15,y = .99,buttons= x_buttons  ),
                dict(type = 'dropdown',x = -.16,y = .79,buttons= color_buttons  ),
                dict(type = 'dropdown',x = -.15,y = .59,buttons= size_buttons  )],
                      
        annotations=[
            dict(text="Select X-Axis:",showarrow=False,x=-.5,y=1,xref="paper",yref="paper",xanchor="left",yanchor="bottom",font=dict(size=14)),
            dict(text="Select Color:",showarrow=False,x=-.5,y=.8,xref="paper",yref="paper",xanchor="left",yanchor="bottom",font=dict(size=14)),
            dict(text="Select Size:",showarrow=False,x=-.5,y=.6,xref="paper",yref="paper",xanchor="left",yanchor="bottom",font=dict(size=14))]
                    ) 
    
    link = py.plot(fig, filename = 'scatter-plot-kudos-factors', auto_open=False)
    
    return link 


def scatter_3d_plot_cluster(df, cluster_cols, kneedles = None):

    fig = px.scatter_3d(df, x = cluster_cols[0],  y = cluster_cols[1],  z = cluster_cols[2], color = 'Clusters of %.2f'%kneedles[-1] )
    
    # Slider for updating color
    color_sliders = []
    for knee in kneedles[::-1]:
        column = 'Clusters of %.2f'%knee
        slider = dict(label=column,method="update",args=[{'marker.color': [df[column]], 'coloraxis.colorscale': 'Viridis'},
                                                    {'coloraxis': {'cmin': df[column].min(), 'cmax': df[column].max(),'colorbar': {'title': {'text': column}}}}])
        color_sliders.append(slider)
        
    
    fig.update_layout(yaxis={'title': None, 'showticklabels': True}, margin=dict(l=0, r=0, t=40, b=0),width = 800, height=400,
                title=dict(text="Clusterting Similar Runs with DBSCAN", x=0.55, y=0.95, xanchor="center", yanchor="top"),
                     updatemenus= [ 
                dict(type = 'dropdown', x = -.15, y = .98, buttons= color_sliders,showactive = True)], 
                     annotations=[
                dict(text=" Epsilon (Clustering Difference Value):",showarrow=False,x=-.40,y=.99,xref="paper",yref="paper",xanchor="left",yanchor="bottom",font=dict(size=14))],
                     )
    
    link = py.plot(fig, filename = 'scatter-3d-plot-clusters', auto_open=False)

    return link


