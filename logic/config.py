# -*- coding: utf-8 -*-
import yaml
import sys
from pathlib import Path


class Config:
    """
    Extracts the data from the configuration file given
    """
    def __init__(self, path):
        with open(path, 'r') as f:
            contents = f.read()
            self.options = yaml.load(contents, Loader=yaml.FullLoader)


path_to_config = Path(__file__).parent.parent.joinpath('config', 'lotti_config.yaml')

if not path_to_config.exists():
    # handle a case when pyinstaller compile everything in one executable file
    path_to_config = Path(sys.argv[0]).parent.joinpath('config', 'lotti_config.yaml')
config = Config(path_to_config)
