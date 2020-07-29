import json
from datetime import date

import requests

from utils import config


def get_lol_version():
    """ Get current League of Legends version """
    versions = json.loads(requests.get(
        "https://ddragon.leagueoflegends.com/api/versions.json").text)
    # reformats from 10.14.5 to 10.14
    latest = ".".join(versions[0].split(".")[:2])
    return latest


def check_source_version(source, lol_version):
    """ Compares and prints current source version to LoL version and local imported source version """

    source_version = source.get_version()
    source_outdated = ""
    try:
        if float(lol_version) > float(source_version):
            source_outdated = " (Not updated to new patch yet)"
    except:
        # source_verson is not a number
        pass

    local_version = config.get(source.name)
    local_outdated = ""
    try:
        if float(source_version) > float(local_version):
            local_outdated = " (outdated!)"
    except:
        # source_verson is not a number
        pass

    print(
        f"{source.name.capitalize()} version: {source_version}{source_outdated}, imported version: {local_version}{local_outdated}")
