"""Reads the json conf file"""

from pathlib import Path
from collections import namedtuple
from json import load


def get_conf(filen="server_conf"):
    """Returns the stuff in that json file innit"""
    full_path = Path(__file__).parent.absolute()
    with open(Path(full_path, f"{filen}.json"), "r") as conf:
        return load(conf, object_hook=lambda d: namedtuple('config', d.keys())(*d.values()))
