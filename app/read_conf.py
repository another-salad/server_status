"""Reads the json conf file"""

from pathlib import Path
from collections import namedtuple
from json import load


def get_servers():
    """Returns the servers in the server_conf.json file"""
    full_path = Path(__file__).parent.absolute()
    with open(Path(full_path, "server_conf.json"), "r") as conf:
        return load(conf, object_hook=lambda d: namedtuple('config', d.keys())(*d.values()))
