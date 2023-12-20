#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import os
import subprocess
from PIL import Image, ImageFont
_picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')

import datetime
import socket
import urllib.request
import docker

from hurry.filesize import size

def init_fonts(police: str = 'Font.ttc'):
	fontSet = {}
	fontSet['9'] = ImageFont.truetype(os.path.join(_picdir, police), 9)
	fontSet['11'] = ImageFont.truetype(os.path.join(_picdir, police), 11)
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
	iconSet['security_updates'] = Image.open(os.path.join(_picdir, 'security-updates2.png'))
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
	return str(datetime.timedelta(seconds=int(float(open('/proc/uptime').read().split()[0]))))

def get_update_count():
	upgrades = subprocess.run(['apt', 'list', '--upgradable'], stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)
	return len(list(filter(None,upgrades.stdout.decode('utf-8').split('\n')[1:])))

def get_docker_containers_count():
	docker_containers = docker.from_env().containers
	return len(docker_containers.list(filters={'status':'running'}))