import messaging as Messaging
from messaging import MSG_TO_SERVER_KEYS

import threading

import argparse
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", help="source for data ('kinect', 'stanford' or 'cornell', default is cornell)")
parser.add_argument('--data', help='name of sample data file (including file extension)')
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()


# Sample data
sample_tracking_data = []

path = './data'
if args.source is not None:
    if args.source.lower() == 'stanford':
        path += '/sample-stanford/'
        if args.data is None:
            path += 'squatData.txt'
        else:
            path += args.data
    elif args.source.lower() == 'cornell':
        path += '/sample-cornell/'
        if args.data is None:
            path += 'sample.txt'
        else:
            path += args.data
else:
    path += '/sample-kinect/'
    if args.data is None:
        path += 'sample.txt'
    else:
        path += args.data

sample_tracking_data = open(path).read().splitlines()


# Initiate Messaging
Messaging.init(args.verbose)

# Simulation Thread
thread = threading.Thread(target=Messaging.start_sending)
thread.daemon = True
thread.start()

stop_simulating = threading.Event()
stop_simulating.set()


# Simulate tracking
def simulate_tracking():
    while True:
        for tracking_data_item in sample_tracking_data:
            while stop_simulating.is_set():
                pass
            Messaging.send(MSG_TO_SERVER_KEYS.TRACKING_DATA.name, tracking_data_item)
            time.sleep(.09)


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
            print('Started tracking')
            Messaging.send(MSG_TO_SERVER_KEYS.TRACKING_STARTED.name, '')
            stop_simulating.clear()
    else:
        continue
