import logging
import os
import sys

try:
    from .environment import Environment
    env = Environment()
except Exception as e:
    logging.error(f"Failed to import Environment: {e}")
    sys.exit(1)

try:
    from .config import Config
    conf = Config(env)
except Exception as e:
    logging.error(f"Failed to bootstrap Config: {e}")
    sys.exit(1)
