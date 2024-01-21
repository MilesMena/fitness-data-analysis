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
            button = dict(
                label=column,
                method='update',
                args=[{'y': [df[column]]}]
            )
            buttons.append(button)
        
    fig.update_layout(yaxis={'title': None, 'showticklabels': True}, margin=dict(l=0, r=0, t=40, b=0),width = 1000, height=400,
                     updatemenus= [
                dict(type = 'dropdown', x = -.02, y = 1, buttons= buttons)]) 
    #fig.show()
    link =  py.plot(fig, filename = 'strava-line-metrics-over-time', auto_open=False)
    return link