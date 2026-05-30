import sys
import os
import configparser
import tomllib
from tkinter import Tk
from pathlib import Path

from gui.view import View
from api import Api
from utils import pattern


def main() -> int:
    print('Starting OpenShockTk')
    # Setup and load config
    config = configparser.ConfigParser()
    config_path = Path('config.toml')
    api_defaults = {
        'token': '"your_token_here"',
        'user_agent': '"OpenShockTk/0.1"'
    }
    # Create config from defaults if none exists
    if not config_path.exists():
        print('No config found. Attempting to create one.')
        config['API'] = api_defaults
        with open(config_path, 'w') as f:
            config.write(f)
    else:
        print('Config found.')
    # Open as toml
    with open(config_path, 'rb') as f:
        config = tomllib.load(f)
    # Parse config
    token = config['API']['token']
    user_agent = config['API']['user_agent']
    if f'"{token}"' == api_defaults['token'] or token == '':
        print('API token not set! Exiting...')
        return 1
    api_client = Api(token, user_agent)

    PATTERNS_PATH = Path('patterns')
    if not PATTERNS_PATH.exists():
        os.mkdir(PATTERNS_PATH)
    pattern_files = [pf for pf in PATTERNS_PATH.iterdir()]
    patterns = [pattern.get_pattern_from_file(pf, api_client, True) 
                for pf in pattern_files]
    
    # Tkinter setup
    root = Tk()
    View(root, api_client, patterns)
    root.mainloop()

    return 0


if __name__ == '__main__':
    sys.exit(main())