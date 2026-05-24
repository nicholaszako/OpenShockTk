import sys
import configparser
import tomllib
from tkinter import Tk
from pathlib import Path

from gui.view import View
from api import Api

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
    
    with open(config_path, 'rb') as f:
        config = tomllib.load(f)
    
    token = config['API']['token']
    user_agent = config['API']['user_agent']

    if f'"{token}"' == api_defaults['token'] or token == '':
        print('API token not set! Exiting...')
        return 1

    # Tkinter setup
    root = Tk()
    api_client = Api(token, user_agent)
    View(root, api_client)
    root.mainloop()

    return 0

if __name__ == '__main__':
    sys.exit(main())