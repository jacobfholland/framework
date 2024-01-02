import os
from app.config.environment import Environment
from app.utils.printable import Printable

from app.utils.validate import validate


class Config(Printable):

    def __init__(self):
        # TODO: Fix config. Always defaulting to these init values
        self.env = Environment()
        self.LOG_LEVEL = "DEBUG"
        self.APP_NAME = "Framework"

        self.LOG_PATH = "logs"
        self.DATABASE = False
        self.AUTH = False
        self.bind_environment_variables()

    def bind_environment_variables(self):
        for k, v in self.env.__dict__.items():
            setattr(self, k, validate(v))
