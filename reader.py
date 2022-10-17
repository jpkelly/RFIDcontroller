#! /usr/bin/python3

import mercury
import argparse
import time
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client
from signal import signal, SIGINT
from sys import exit
import systemd_stopper

SEND_IP = "10.39.54.240"
SEND_PORT = 7000
OFFSET = 0 # Antenna number offset to get position with multiple readers
TAGVALS = ["0", "0", "0", "0",]
READCB = [0, 0, 0, 0,]
READCBOLD = [0, 0, 0, 0,]
POWER = [850, 850, 850, 850]
ENABLED = [1, 1, 1, 1]
RSSITHRESH = -50

reader = mercury.Reader("llrp://x.x.x.x") # Reader IP address
reader.set_read_plan([1,2,3,4], "GEN2", read_power=1000)
# set_read_powers = reader.set_read_powers([(1, 1100), (2, 1100), (3, 1100), (4, 1100)])

print("Connected Ports: " + str(reader.get_connected_ports()))
print("Supported Regions: " + str(reader.get_supported_regions()))
print("Power Range: " + str(reader.get_power_range()))
print("Antennae: " + str(reader.get_antennas()))
print("Model: " + reader.get_model())
print("Read Powers: " + "1-" + str(POWER[0]) + " 2-" + str(POWER[1]) + " 3-" + str(POWER[2]) + " 4-" + str(POWER[3]))

# OSC CLIENT
parser_client = argparse.ArgumentParser()
parser_client.add_argument("--ip", default=SEND_IP, help="The ip of the OSC server")
parser_client.add_argument("--port", type=int, default=SEND_PORT, help="The port the OSC server is listening on")
args_client = parser_client.parse_args()
client = udp_client.SimpleUDPClient(args_client.ip, args_client.port)

def handler(signal_received, frame):
	print('SIGINT or CTRL-C detected. Exiting gracefully')
	# reader.stop_reading()
	exit(0)

def do_read(antenna):
	reader.set_read_plan([antenna], "GEN2", read_power=POWER[antenna - 1])
	tag = reader.read(timeout=250)
	# print(tag, len(tag))
	length = len(tag)

	if length >= 1:
		for i in range(length):
			tagstr = tag[i].epc.decode('ascii')
			# print(i, tagstr, tag[i].antenna, tag[i].rssi)
			print("POS" + str(tag[i].antenna + OFFSET), tagstr, "Read Count: " + str(tag[i].read_count), "Strength: " + str(tag[i].rssi))
			if tag[i].rssi >= RSSITHRESH:
				client.send_message("/healthcare/pos"+str(antenna + OFFSET), tagstr)
	else:
		print("POS" + str(antenna + OFFSET) + " 0")
		client.send_message("/healthcare/pos"+str(antenna + OFFSET), "0")

def send_states():
	for i, val in enumerate(TAGVALS):
		print(i, val)


while __name__ == '__main__':
	stopper = systemd_stopper.install()
	signal(SIGINT, handler)
	while stopper.run:
		for i in range(1, 5):
			if ENABLED[i - 1] == 1:
				do_read(i)
		print()
		for i, val in enumerate(TAGVALS):
			if READCB[i] == 1:
				# print(i, val)
				TAGVALS[i] = "0"
			READCB[i] == 0
			# send_states()
		# time.sleep(1)
	print('Stopped by systemd_stopper. Exiting gracefully')


