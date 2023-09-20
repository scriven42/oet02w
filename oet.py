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

def ui1_click_callback():
    logprint("UI_1 Button Clicked!")

def ui2_click_callback():
    logprint("UI_2 Button Clicked!")

def brm_click_callback():
    logprint("BR- Button Clicked!")

def brp_click_callback():
    logprint("BR+ Button Clicked!")

oet = OET_Buttons(ui1_click_callback, ui2_click_callback, brm_click_callback, brp_click_callback)
oet.start_loop_thread()
logprint('OET Button Loop Thread started')

