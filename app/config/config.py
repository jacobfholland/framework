import os

from app.utils.validate import validate


class Config:

    def __init__(self, env):
        self.APP_NAME = "Framework"
        self.LOG_LEVEL = "INFO"
        self.LOG_PATH = "logs"
        self.DATABASE = False
        self.AUTH = False
        self.bind_environment_variables(env)

    def bind_environment_variables(self, env):
        for k, v in env.__dict__.items():
            setattr(self, k, validate(v))
