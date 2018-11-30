#!/usr/bin/python3

import json
from pprint import pprint
import requests
import configparser

# read the status for this device
def pull_status(url, device, key):
    headers = {
        'Content-type': 'application/json',
        'x-api-key': key
    }
    r = requests.get("{0}/{1}".format(url, device), headers=headers)
    return r.json()

# read config
config_file="hush.conf"
cfg = configparser.RawConfigParser()
cfg_list = cfg.read(config_file)
if len(cfg_list) != 1:
    print("ERROR: failed to open config file: {0}".format(config_file))
    exit(1)
if not cfg.has_section('hush'):
    print("ERROR: config section 'hush' missing")
    exit(1)
url = cfg.get('hush', 'url')
device = cfg.get('hush', 'device')
key = cfg.get('hush', 'key')

d=pull_status(url, device, key)
pprint(d)
