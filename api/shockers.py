# This module is for v1 "Shockers" API
# https://api.openshock.app/scalar/viewer/#version-1/tag/shockers

import requests

class Shockers:
    
    def __init__(self, token, user_agent):
        self.token = token
        self.user_agent = user_agent

    def get_shockers(self) -> list:
        headers = {
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Open-Shock-Token': self.token
        }

        res = requests.get('https://api.openshock.app/1/shockers/own', 
                     headers=headers)

        # Raise exception for any non-ok response before trying to parse body
        if not res.ok:
            res.raise_for_status()

        print(f'Got list of shockers. Got status {res.status_code}.')

        res_data = res.json()['data'][0]    # First hub json
        shocker_list = res_data['shockers']
        return shocker_list   
