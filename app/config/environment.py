from dotenv import load_dotenv
from pathlib import Path
import os
from app.utils.validate import validate


INITIAL_ENV = dict(os.environ)


class Environment:
    def __init__(self) -> None:
        self.PROJECT_DIR = Path(os.getcwd())
        self.load_env_files()
        for k, v in os.environ.items():
            if k not in INITIAL_ENV.keys():
                setattr(self, k, validate(v))
        self.PROJECT_DIR = os.getcwd()

    def get_env_files(self):
        return [file for file in self.PROJECT_DIR.rglob("*.env")]

    def load_env_files(self):
        for env_file in self.get_env_files():
            load_dotenv(env_file, override=True)
            print(f"Loaded configuration from {env_file}")
