import requests
import urllib3
import config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class StravaAPI:
    # define global vars
    auth_url = "https://www.strava.com/oauth/token"
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    
    def __init__(self):
        # request a non-stale access token with our refresh token
        self.access_token = self.request_token()

    def request_token(self):
        print("Requesting Token...\n")
        # we pull our api info from config.py
        payload = {
            'client_id': config.client_id,
            'client_secret': config.client_secret,
            'refresh_token': config.refresh_token,
            'grant_type': "refresh_token",
            'f': 'json'
            }
        res = requests.post(self.auth_url, data=payload, verify=False)
        access_token = res.json()['access_token']
        return access_token
        
    def get_dataset(self):
        header = {'Authorization': 'Bearer ' + self.access_token}
        param = {'per_page': 200, 'page': 1}
        my_dataset = requests.get(self.activites_url, headers=header, params=param).json()
        return my_dataset
        
