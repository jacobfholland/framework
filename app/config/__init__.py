import os
import sys

try:
    from .environment import Environment
    env = Environment()
except Exception as e:
    print(f"Failed to import Environment: {e}")
    sys.exit(1)

try:
    from .config import Config
    conf = Config(env)
except Exception as e:
    print(f"Failed to bootstrap Config: {e}")
    sys.exit(1)
