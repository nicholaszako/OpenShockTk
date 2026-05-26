import json
import time
from pathlib import Path

from api import Api


class Pattern:
    def __init__(self, pattern_json, api_client, name=None):
        self.pattern_json = pattern_json
        self.api = api_client
        self.name = name
        if not self.validate():
            raise Exception('Invalid pattern')
        
    def validate(self):
        # STUB
        return True
    
    # Bear in mind this is (currently) not asynchronous
    def start(self):
        c = self.api.control
        for step in self.pattern_json:
            request_args = step['request']
            sleep_s = step['sleep']/1000
            prepped = c.get_prepared_req(**request_args)
            c.send(prepped)
            time.sleep(sleep_s)
            

def get_pattern_from_file(path: Path, api_client: Api, 
                          use_filename: bool=True):
    pattern_json = None
    with open(path, 'r') as f:
        pattern_json = json.load(f)
    if (use_filename):
        fname = path.stem
        return Pattern(pattern_json, api_client, fname)
    else:
        return Pattern(pattern_json, api_client)
