#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import signal
from threading import Event
import logging

import os
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
	sys.path.append(libdir)
from waveshare_epd import epd3in52
from PIL import Image,ImageDraw
import time

from e_paper_utils import *
from red_reactor import verify_RedReactor_requirements, RedReactor

logging.basicConfig(
	filename="/opt/e-Paper/e-paper.log",
	encoding="utf8",
	format='[%(asctime)s][%(levelname)-7s] - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
exit_event = Event()
verify_RedReactor_requirements()
fonts = init_fonts()
cursiveFonts = init_fonts('Cursif.ttf')
icons = init_icon_set()
report_interval = 30
signal_num = -1

def update_display(epd, image: Image, draw: ImageDraw, rr: RedReactor):
	# draw table layout
	draw.line((240, 0, 240, 240), fill = 0)
	draw.line((0, 90, 360, 90), fill = 0)
	draw.line((120, 90, 120, 240), fill = 0)
	image.paste(icons['home'], (10, 3))
	draw.text((54, 12), get_interal_ip(), font = fonts['20'], fill = 0)
	
	image.paste(icons['web'], (10, 48))
	draw.text((54, 55), get_external_ip(), font = fonts['20'], fill = 0)

	battery_icon = None
	match rr.battery_status:
		case "CHARGING":
			battery_icon = icons['battery_charging']
		case "FULL":
			battery_icon = icons['battery_charged']
		case _:
			if rr.battery_charge > 95:
				battery_icon = icons['battery_100']
			elif rr.battery_charge >= 75:
				battery_icon = icons['battery_75']
			elif rr.battery_charge >= 50:
				battery_icon = icons['battery_50']
			elif rr.battery_charge >= 25:
				battery_icon = icons['battery_25']
			else :
				battery_icon = icons['battery_0']
	image.paste(battery_icon, (267, 10))
	charge = "{:4} %".format(rr.battery_charge)
	draw.text((254, 50), charge, font = fonts['30'], fill = 0)

	image.paste(icons['uptime'], (15, 95))
	draw.text((50, 100), get_uptime(), font = fonts['18'], fill = 0)
	
	image.paste(icons['memory'], (15, 134))
	total_ram, ram_used, percent_ram = get_ram_info()
	draw.text((50, 132), "{:3} %".format(percent_ram), font = fonts['18'], fill = 0)
	draw.text((50, 150), "({}B/{}B)".format(ram_used, total_ram), font = fonts['11'], fill = 0)
	
	image.paste(icons['cpu'], (15, 172))
	draw.text((50, 175), "{:3} %".format(get_cpu_usage()), font = fonts['18'], fill = 0)
	
	image.paste(icons['disk'], (18, 209))
	disk_total, disk_used, disk_percent = get_disk_usage()
	draw.text((50, 206), "{:3} %".format(disk_percent), font = fonts['18'], fill = 0)
	draw.text((50, 224), "({}B/{}B)".format(disk_used, disk_total), font = fonts['11'], fill = 0)
	
	image.paste(icons['security_updates'], (145, 105))
	draw.text((158, 185), "{:3}".format(get_update_count()), font = fonts['30'], fill = 0)
	draw.text((150, 215), "updates", font = fonts['18'], fill = 0)
	
	image.paste(icons['docker'], (260, 110))
	draw.text((285, 185), "{:2}".format(get_docker_containers_count()), font = fonts['30'], fill = 0)
	draw.text((260, 215), "containers", font = fonts['18'], fill = 0)

	epd.display(epd.getbuffer(image))


def quit(signum, _frame):
	global signal_num
	logging.warning("Interrupted by %d, shutting down" % signum)
	signal.signal(signum, signal.SIG_DFL)
	exit_event.set()
	signal_num = signum

if __name__ == '__main__':
	signal.signal(signal.SIGINT, quit)
	signal.signal(signal.SIGHUP, quit)
	signal.signal(signal.SIGTERM, quit)
	
	if len(sys.argv) >= 2:
		report_interval = int(sys.argv[1])
		logging.info("Measuring every {} seconds".format(report_interval))


	# Initialise RedReactor and set measurement interval
	rr = RedReactor(report_interval)

	# Initialise EPD
	epd = epd3in52.EPD()
	epd.init()
	epd.display_NUM(epd.WHITE)
	# epd.lut_GC()
	# epd.refresh()

	epd.send_command(0x50)
	epd.send_data(0x17)

	while not exit_event.is_set():
		image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
		draw = ImageDraw.Draw(image)
		update_display(epd, image, draw ,rr)
		
		epd.display(epd.getbuffer(image.transpose(Image.Transpose.ROTATE_180)))
		epd.lut_GC()
		epd.refresh()
		
		exit_event.wait(10)

	logging.info("Shutting down...")

	image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
	draw = ImageDraw.Draw(image)
	draw.text((20, 35), 'Good Bye', font = cursiveFonts['64'], fill = 0)
	epd.display(epd.getbuffer(image.transpose(Image.Transpose.ROTATE_180)))
	epd.lut_GC()
	epd.refresh()

	epd3in52.epdconfig.module_exit()
	os.kill(os.getpid(), signal_num)