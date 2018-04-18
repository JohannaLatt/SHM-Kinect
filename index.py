import messaging as Messaging
from messaging import MSG_TO_SERVER_KEYS

import _thread
import threading

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--data', help='path to file to use as sample data')
args = parser.parse_args()

# Sample data
sample_tracking_data = []
if args.data is None:
    sample_tracking_data = open('./data/sample_teeth.txt').read().splitlines()
else:
    sample_tracking_data = open(args.data).read().splitlines()


# Initiate Messaging
Messaging.init()

# Simulation Thread
_thread.start_new_thread(Messaging.start_sending, ())

stop_simulating = threading.Event()
stop_simulating.set()


# Simulate tracking
def simulate_tracking():
    while True:
        for tracking_data_item in sample_tracking_data:
            while stop_simulating.is_set():
                pass
            Messaging.send(MSG_TO_SERVER_KEYS.TRACKING_DATA.name, tracking_data_item)


simulation_thread = threading.Thread(target=simulate_tracking)
simulation_thread.start()

# Run the program from the terminal
while(True):
    input_key = input("Press q to quit, t to start the tracking simulation and p to pause the simulation...\n").strip()
    if input_key == "q":
        stop_simulating.set()
        Messaging.send(MSG_TO_SERVER_KEYS.TRACKING_LOST.name, '')
        print('Exiting..')
        sys.exit()
    elif input_key == "p":
        stop_simulating.set()
        Messaging.send(MSG_TO_SERVER_KEYS.TRACKING_LOST.name, '')
    elif input_key == "t":
        if stop_simulating is not None:
            Messaging.send(MSG_TO_SERVER_KEYS.TRACKING_STARTED.name, '')
            stop_simulating.clear()
    else:
        continue
