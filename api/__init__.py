from api.control import Control
from api.shockers import Shockers

class Api:
    def __init__(self, token: str, user_agent: str):
        self.control = Control(token, user_agent)
        self.shockers = Shockers(token, user_agent)
