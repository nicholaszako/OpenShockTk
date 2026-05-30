import json
import time
from pathlib import Path
from threading import Thread, Event

from api import Api


class Pattern:
    def __init__(self, pattern_json, api_client, name=None):
        self.pattern_json = pattern_json
        self.api = api_client
        self.name = name
        self.thread = None
        self._stop_event = Event()
        if not self.validate():
            raise Exception('Invalid pattern')
        
    def validate(self):
        # STUB
        return True
    
    def start(self):
        if self.thread:
            self.stop()
        self._stop_event.clear()
        self.thread = Thread(target=self._send)
        self.thread.start()

    def stop(self):
        self._stop_event.set()
    
    # Returns true iff entire pattern was sent successfully
    def _send(self):
        c = self.api.control
        for msg in self.pattern_json:
            if self._stop_event.is_set():
                # Stop before attempting to send message
                return False
            request_args = msg['request']
            sleep_s = msg['sleep']/1000
            prepped = c.get_prepared_req(**request_args)
            c.send(prepped)
            time.sleep(sleep_s)
        return True
            

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
