#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import numpy as np
import matplotlib.pyplot as plt


logging.basicConfig(
	filename="/opt/e-Paper/e-paper.log",
	encoding="utf8",
	format='[%(asctime)s][%(levelname)-7s] - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
history_limit = 30
history_volts = []
history_milli = []
history_temp = []

	
def rr_plots(y1: list, y2: list):
	"""Plots graphs to image file for RR_WebMonitor
	:param
	y1 = list of voltage samples
	y2 = list of current samples

	All lists assumed to be the same length (= number of elements)
	"""

	logging.info("RR_Plotgraphs : Plotting size: %d", len(y1))
	x1data = np.arange(len(y1))
	y1data = np.array(y1)
	y2data = np.array(y2)

	# Create Plot space
	fig, (ax1, ax3) = plt.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [2, 1]})

	# Main Title
	ax1.set_title('RedReactor Battery Monitor Status', fontdict={'fontweight': 'bold'})

	# Main plot for voltage and current
	ax1.set_xlabel('Time (samples)')
	ax1.set_ylabel('Voltage (V)', color='black')
	# -o to plot marker and line
	line1 = ax1.plot(x1data, y1data, '-o', color='red', label='Volts (V)')

	ax1.tick_params(axis='y', labelcolor='black')

	# Set up 2nd y-axis
	ax2 = ax1.twinx()
	ax2.set_ylabel('Current (mA)', color='blue')
	# -o to plot marker and line
	line2 = ax2.plot(x1data, y2data, '-o', color='blue', label='Current (mA)')
	ax2.tick_params(axis='y', labelcolor='blue')

	# Set x-axis tick interval to scale with dataset
	ax1.set_xticks(np.arange(min(x1data), max(x1data) + int(max(x1data)/10)+1,
							 int((max(x1data)/10)+1) if max(x1data) > 10 else 1))

	# Set y1-axis limits for fixed sized graph
	ax1.set_ylim([2.4, 4.3])
	# For current, set y2-axis max scale according to simple usage models
	if min(y2data) < 0:
		y_min = min(y2data)//500*500
	else:
		y_min = 0
	if max(y2data) < 500:
		y_max = 500
	else:
		y_max = max(y2data)//1000*1000+1000
	ax2.set_ylim([y_min, y_max])

	# Combine labels, lower left is best overall
	lines = line1 + line2
	labels = [lab.get_label() for lab in lines]
	plt.legend(lines, labels, loc='lower left', fontsize='small', fancybox=True, framealpha=1, shadow=True, borderpad=1)

	# Tidy up display of graphs (ensure they fit and have spacing between)
	fig.set_size_inches(5, 6)
	fig.tight_layout()

	# Save (and Show plot for testing) (order important)
	plt.savefig('RR_Status.png', bbox_inches='tight', dpi=50)

	# Allow it to be garbage collected
	plt.close(fig)
