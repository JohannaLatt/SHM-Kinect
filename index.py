import _thread
import threading
import messaging as Messaging
from messaging import MSG_TO_SERVER_KEYS
import time
import sys


Messaging.init()
_thread.start_new_thread(Messaging.start_sending, ())


# Simulate tracking
def simulate_tracking():
    while True:
        for tracking_data_item in sample_tracking_data:
            while stop_simulating.is_set():
                pass
            Messaging.send(MSG_TO_SERVER_KEYS.TRACKING_DATA.name, tracking_data_item)
            #time.sleep(.1)

# Sample data
stop_simulating = threading.Event()
stop_simulating.set()

sample_tracking_data = open('./data/sample_teeth.txt').read().splitlines()

simulation_thread = threading.Thread(target=simulate_tracking)
simulation_thread.start()

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
