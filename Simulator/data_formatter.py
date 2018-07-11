from enum import Enum
import json
import numpy as np


# ------ KINECT REFERENCE -----
class KINECT_JOINTS(Enum):
    SpineBase = 0
    SpineMid = 1
    Neck = 2
    Head = 3
    ShoulderLeft = 4
    ElbowLeft = 5
    WristLeft = 6
    HandLeft = 7
    ShoulderRight = 8
    ElbowRight = 9
    WristRight = 10
    HandRight = 11
    HipLeft = 12
    KneeLeft = 13
    AnkleLeft = 14
    FootLeft = 15
    HipRight = 16
    KneeRight = 17
    AnkleRight = 18
    FootRight = 19
    SpineShoulder = 20
    HandTipLeft = 21
    ThumbLeft = 22
    HandTipRight = 23
    ThumbRight = 24


KINECT_JOINT_PARENTS = {
    'SpineBase': 'SpineBase',
    'SpineMid': 'SpineBase',
    'SpineShoulder': 'SpineMid',
    'Neck': 'SpineShoulder',
    'Head': 'Neck',
    'ShoulderLeft': 'SpineShoulder',
    'ElbowLeft': 'ShoulderLeft',
    'WristLeft': 'ElbowLeft',
    'HandLeft': 'WristLeft',
    'ShoulderRight': 'SpineShoulder',
    'ElbowRight': 'ShoulderRight',
    'WristRight': 'ElbowRight',
    'HandRight': 'WristRight',
    'HipLeft': 'SpineBase',
    'KneeLeft': 'HipLeft',
    'AnkleLeft': 'KneeLeft',
    'FootLeft': 'AnkleLeft',
    'HipRight': 'SpineBase',
    'KneeRight': 'HipRight',
    'AnkleRight': 'KneeRight',
    'FootRight': 'AnkleRight',
    'HandTipLeft': 'HandLeft',
    'ThumbLeft': 'HandLeft',
    'HandTipRight': 'HandRight',
    'ThumbRight': 'HandRight'
}


# ------- CORNELL -------

class CORNELL_JOINTS(Enum):
    Head = 1
    Neck = 2
    Torso = 3
    LeftShoulder = 4
    LeftElbow = 5
    RightShoulder = 6
    RightElbow = 7
    LeftHip = 8
    LeftKnee = 9
    RightHip = 10
    RightKnee = 11
    LeftHand = 12
    RightHand = 13
    LeftFoot = 14
    RightFoot = 15


CORNELL_JOINT_PARENTS = {
    'Head': 'Neck',
    'Neck': 'Torso',
    'Torso': 'Torso',
    'LeftShoulder': 'Neck',
    'LeftElbow': 'LeftShoulder',
    'RightShoulder': 'Neck',
    'RightElbow': 'RightShoulder',
    'LeftHip': 'Torso',
    'LeftKnee': 'LeftHip',
    'RightHip': 'Torso',
    'RightKnee': 'RightHip',
    'LeftHand': 'LeftElbow',
    'RightHand': 'RightElbow',
    'LeftFoot': 'LeftKnee',
    'RightFoot': 'RightKnee'
}


def format_cornell(str):
    result = {}
    data = str.split(",")

    # Create joints data-structure
    j = 1
    if len(data) != 172:
        print("[DATA FORMATTER][error] len of skeleton data is {} (it should be 172) discarding".format(len(data)))
        return ""

    for i in range(11, 154, 14):
        x = float(data[i])
        y = float(data[i+1])
        z = float(data[i+2])

        result[CORNELL_JOINTS(j).name] = [x, y, z]
        j += 1
    for i in range(155, 168, 4):
        x = float(data[i])
        y = float(data[i+1])
        z = float(data[i+2])

        result[CORNELL_JOINTS(j).name] = [z, y, z]
        j += 1

    return json.dumps(result)


# ------- STANFORD -------

def format_stanford(str):
    result = {}
    data = str.split(",")
    data = np.array(data)           # turn into floats
    data = [float(x) for x in data]
    data = [x * 5 for x in data]

    # Create joints data-structure
    j = 0
    for i in range(0, len(data), 3):
        try:
            x = float(data[i]) - 1500 # move the data more to the center
            y = -float(data[i+1])
            z = -float(data[i+2])
        except IndexError:
            print("[Kinect][DataFormatter] Incomplete item, not sending")
            return ""

        result[KINECT_JOINTS(j).name] = [ x, y, z ]
        j += 1

    if (j == 25):   # only return if data complete
        return json.dumps(result)
    else:
        print("[Kinect][DataFormatter] Incomplete item, not sending")
        return ""
