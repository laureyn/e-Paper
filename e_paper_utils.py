#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import os
import subprocess
from PIL import Image, ImageFont
_picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')

from string import Formatter
import datetime
import socket
import urllib.request
import docker

from hurry.filesize import size

def init_fonts(police: str = 'Font.ttc'):
	fontSet = {}
	fontSet['9'] = ImageFont.truetype(os.path.join(_picdir, police), 9)
	fontSet['11'] = ImageFont.truetype(os.path.join(_picdir, police), 11)
	fontSet['12'] = ImageFont.truetype(os.path.join(_picdir, police), 12)
	fontSet['14'] = ImageFont.truetype(os.path.join(_picdir, police), 14)
	fontSet['16'] = ImageFont.truetype(os.path.join(_picdir, police), 16)
	fontSet['18'] = ImageFont.truetype(os.path.join(_picdir, police), 18)
	fontSet['20'] = ImageFont.truetype(os.path.join(_picdir, police), 20)
	fontSet['24'] = ImageFont.truetype(os.path.join(_picdir, police), 24)
	fontSet['26'] = ImageFont.truetype(os.path.join(_picdir, police), 26)
	fontSet['28'] = ImageFont.truetype(os.path.join(_picdir, police), 28)
	fontSet['30'] = ImageFont.truetype(os.path.join(_picdir, police), 30)
	fontSet['40'] = ImageFont.truetype(os.path.join(_picdir, police), 40)
	fontSet['50'] = ImageFont.truetype(os.path.join(_picdir, police), 50)
	fontSet['64'] = ImageFont.truetype(os.path.join(_picdir, police), 64)

	return fontSet

def init_icon_set():
	iconSet = {}
	iconSet['home'] = Image.open(os.path.join(_picdir, 'home.png'))
	iconSet['web'] = Image.open(os.path.join(_picdir, 'web.png'))
	iconSet['disk'] = Image.open(os.path.join(_picdir, 'disk.png'))
	iconSet['cpu'] = Image.open(os.path.join(_picdir, 'cpu.png'))
	iconSet['memory'] = Image.open(os.path.join(_picdir, 'memory.png'))
	iconSet['uptime'] = Image.open(os.path.join(_picdir, 'uptime.png'))
	iconSet['security_updates'] = Image.open(os.path.join(_picdir, 'security-updates.png'))
	iconSet['docker'] = Image.open(os.path.join(_picdir, 'docker.png'))
	iconSet['battery_charging'] = Image.open(os.path.join(_picdir, 'battery-charging.png'))
	iconSet['battery_charged'] = Image.open(os.path.join(_picdir, 'battery-charged.png'))
	iconSet['battery_0'] = Image.open(os.path.join(_picdir, 'battery-0%.png'))
	iconSet['battery_25'] = Image.open(os.path.join(_picdir, 'battery-25%.png'))
	iconSet['battery_50'] = Image.open(os.path.join(_picdir, 'battery-50%.png'))
	iconSet['battery_75'] = Image.open(os.path.join(_picdir, 'battery-75%.png'))
	iconSet['battery_100'] = Image.open(os.path.join(_picdir, 'battery-100%.png'))

	return iconSet

def get_ram_info():
    ram = psutil.virtual_memory()

    total_ram = ram.total # Total RAM installed
    used_ram = ram.used # RAM used by processes
    percent_used = ram.percent # Percentage of RAM used

    return size(total_ram), size(used_ram), percent_used

def get_cpu_usage():
	return psutil.cpu_percent(interval=1)

def get_disk_usage():
	disk_usage = psutil.disk_usage('/')
	return size(disk_usage.total), size(disk_usage.used), disk_usage.percent

def get_interal_ip():
	# Top-left corner info
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	internal_ip = s.getsockname()[0]
	s.close()
	return internal_ip

def get_external_ip():
	return urllib.request.urlopen('https://ident.me').read().decode('utf8')

def get_uptime():
	uptime = int(float(open('/proc/uptime').read().split()[0]))
	split_time = strfdelta(uptime, '{W}w {D}d {H}:{M:02}:{S:02}', 's').split(' ')
	return ' '.join(split_time[0:2]), split_time[2]

def get_update_count():
	upgrades = subprocess.run(['apt', 'list', '--upgradable'], stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)
	return len(list(filter(None,upgrades.stdout.decode('utf-8').split('\n')[1:])))

def get_docker_containers_count():
	docker_containers = docker.from_env().containers
	return len(docker_containers.list(filters={'status':'running'}))

def strfdelta(tdelta, fmt='{D:02}d {H:02}h {M:02}m {S:02}s', inputtype='timedelta'):
    """Convert a datetime.timedelta object or a regular number to a custom-
    formatted string, just like the stftime() method does for datetime.datetime
    objects.

    The fmt argument allows custom formatting to be specified.  Fields can 
    include seconds, minutes, hours, days, and weeks.  Each field is optional.

    Some examples:
        '{D:02}d {H:02}h {M:02}m {S:02}s' --> '05d 08h 04m 02s' (default)
        '{W}w {D}d {H}:{M:02}:{S:02}'     --> '4w 5d 8:04:02'
        '{D:2}d {H:2}:{M:02}:{S:02}'      --> ' 5d  8:04:02'
        '{H}h {S}s'                       --> '72h 800s'

    The inputtype argument allows tdelta to be a regular number instead of the  
    default, which is a datetime.timedelta object.  Valid inputtype strings: 
        's', 'seconds', 
        'm', 'minutes', 
        'h', 'hours', 
        'd', 'days', 
        'w', 'weeks'
    """

    # Convert tdelta to integer seconds.
    if inputtype == 'timedelta':
        remainder = int(tdelta.total_seconds())
    elif inputtype in ['s', 'seconds']:
        remainder = int(tdelta)
    elif inputtype in ['m', 'minutes']:
        remainder = int(tdelta)*60
    elif inputtype in ['h', 'hours']:
        remainder = int(tdelta)*3600
    elif inputtype in ['d', 'days']:
        remainder = int(tdelta)*86400
    elif inputtype in ['w', 'weeks']:
        remainder = int(tdelta)*604800

    f = Formatter()
    desired_fields = [field_tuple[1] for field_tuple in f.parse(fmt)]
    possible_fields = ('W', 'D', 'H', 'M', 'S')
    constants = {'W': 604800, 'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
    values = {}
    for field in possible_fields:
        if field in desired_fields and field in constants:
            values[field], remainder = divmod(remainder, constants[field])
    return f.format(fmt, **values)