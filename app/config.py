from pathlib import Path

import yaml

CONFIG_FILE = Path(__file__).parent.parent / "config" / "settings.yaml"

with open(CONFIG_FILE) as f:
    CONFIG = yaml.safe_load(f)
