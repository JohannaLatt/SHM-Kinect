import pika
from enum import Enum
import configparser
import queue


class MSG_TO_SERVER_KEYS(Enum):
    TRACKING_STARTED = 1
    TRACKING_DATA = 2
    TRACKING_LOST = 3


def init(verbose):
    global v
    v = verbose

    # Save the queue
    global queue
    queue = queue.Queue()

    # Create a local messaging connection
    Config = configparser.ConfigParser()
    Config.read('./config/kinect_config.ini')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.get('General', 'messaging_ip')))

    global __channel
    __channel = connection.channel()

    # Create an exchange for the mirror-messages - type is direct so we can distinguish the different messages
    __channel.exchange_declare(exchange='from-kinect', exchange_type='direct')


def start_sending():
    while True:
        item = queue.get()
        if item is None:
            continue
        try:
            __channel.basic_publish(exchange='from-kinect',
                              routing_key=item['key'],
                              body=item['body'])
            if v:
                print("[info] Sent {}: {}".format(item['key'], item['body'][0:50]))
        except pika.exceptions.ConnectionClosed as cce:
            print('[error] %r' % cce)
        queue.task_done()


def send(key, body):
    if __channel is None:
        init()

    if key not in MSG_TO_SERVER_KEYS.__members__:
        print("[error] %r is not a valid message key to send to the server" % key)
    else:
        queue.put({'key': key, 'body': body})
