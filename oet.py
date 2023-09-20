#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#


import time,datetime
import logging
import configparser
import json
from oet_buttons import OET_Buttons


# Load Config
config = configparser.ConfigParser()
config.read('oet.ini')


# Setup variables
counter               = 0
sleep                 = 1.0
if config.has_option('Default','sleep'):
    sleep             = float(config.get('Default','sleep'))

timestamp_format      = "%Y%m%d_%H%M%S.%f%z"
if config.has_option('Default','timestamp_format'):
    timestamp_format  = config.get('Default','timestamp_format')

timedisplay_format    = "%Y-%m-%d %H:%M:%S %z"
if config.has_option('Default','timedisplay_format'):
    timedisplay_format = config.get('Default','timedisplay_format')


# Setup some functions and logging
def get_timestamp():
    now = datetime.datetime.now()
    return str(now.strftime(timestamp_format))


def get_timedisplay():
    now = datetime.datetime.now()
    return str(now.strftime(timedisplay_format))


logging.basicConfig(filename='oet_'+get_timestamp()+'.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
logging.debug('Logging started')


def logprint(lp_text):
    logging.info(lp_text)
    print(lp_text)

oet = OET_Buttons()
oet.start_loop_thread()
logging.debug('OET Button Loop Thread started')

