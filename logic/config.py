# -*- coding: utf-8 -*-
import sys
from pathlib import Path
import yaml


class Config:
    """
    Extracts the data from the configuration file given
    """
    def __init__(self, path):
        with open(path, 'r') as f:
            contents = f.read()
            self.options = yaml.safe_load(contents)


path_to_config = Path(__file__).parent.parent.joinpath('config', 'lotti_config.yaml')

if not path_to_config.exists():
    # handle a case when pyinstaller compile everything in one executable file
    path_to_config = Path(sys.argv[0]).parent.joinpath('config', 'lotti_config.yaml')
config = Config(path_to_config)
