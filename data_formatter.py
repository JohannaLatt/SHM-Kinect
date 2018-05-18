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
    result = {"joint_data": {}}
    joint_data = result["joint_data"]
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

        joint_data[CORNELL_JOINTS(j).name] = {"joint_position": {"x": x, "y": y, "z": z}, "joint_parent": CORNELL_JOINT_PARENTS[CORNELL_JOINTS(j).name]}
        j += 1
    for i in range(155, 168, 4):
        x = float(data[i])
        y = float(data[i+1])
        z = float(data[i+2])

        joint_data[CORNELL_JOINTS(j).name] = {"joint_position": {"x": x, "y": y, "z": z}, "joint_parent": CORNELL_JOINT_PARENTS[CORNELL_JOINTS(j).name]}
        j += 1

    return json.dumps(result)




# ------- IDAHO -------

class IDAHO_JOINTS(Enum):
    SPINE_BASE = 1          # aka waist
    SPINE_MID = 2           # middle between spine and chest
    SPINE_SHOULDER = 3      # aka Neck
    Neck = 4                # aka Head
    Head = 5                # aka Head tip
    COLLAR_LEFT = 6
    SHOULDER_LEFT = 7       # aka left upper arm
    ELBOW_LEFT = 8          # aka left forearm
    WRIST_LEFT = 9          # aka left hand
    COLLAR_RIGHT = 10
    SHOULDER_RIGHT = 11
    ELBOW_RIGHT = 12
    WRIST_RIGHT = 13
    HIP_LEFT = 14           # aka left upper lef
    KNEE_LEFT = 15          # aka left lower leg
    ANKLE_LEFT = 16         # aka left foot
    FOOT_LEFT = 17          # aka left leg toes
    HIP_RIGHT = 18
    KNEE_RIGHT = 19
    ANKLE_RIGHT = 20
    FOOT_RIGHT = 21


IDAHO_JOINT_PARENTS = {
    'SPINE_BASE': 'SPINE_BASE',
    'SPINE_MID': 'SPINE_BASE',
    'SPINE_SHOULDER': 'SPINE_MID',
    'Neck': 'SPINE_SHOULDER',
    'Head': 'Neck',
    'COLLAR_LEFT': 'SPINE_SHOULDER',
    'SHOULDER_LEFT': 'COLLAR_LEFT',
    'ELBOW_LEFT': 'SHOULDER_LEFT',
    'WRIST_LEFT': 'ELBOW_LEFT',
    'COLLAR_RIGHT': 'SPINE_SHOULDER',
    'SHOULDER_RIGHT': 'COLLAR_RIGHT',
    'ELBOW_RIGHT': 'SHOULDER_RIGHT',
    'WRIST_RIGHT': 'ELBOW_RIGHT',
    'HIP_LEFT': 'SPINE_BASE',
    'KNEE_LEFT': 'HIP_LEFT',
    'ANKLE_LEFT': 'KNEE_LEFT',
    'FOOT_LEFT': 'ANKLE_LEFT',
    'HIP_RIGHT': 'SPINE_BASE',
    'KNEE_RIGHT': 'HIP_RIGHT',
    'ANKLE_RIGHT': 'KNEE_RIGHT',
    'FOOT_RIGHT': 'ANKLE_RIGHT'
}


def format_idaho(str):
    result = {"joint_data": {}}
    joint_data = result["joint_data"]
    data = str.split("  ")
    print(data)
    data = np.array(data)          # turn into floats
    data = [float(x) for x in data]
    data = [x * 10 for x in data]

    # Create joints data-structure
    # SpineBase aka Waist (absolute)
    spine_x = data[0]
    spine_y = data[1]
    spine_z = data[2]
    joint_data[IDAHO_JOINTS(1).name] = {"joint_position": {"x": spine_x, "y": spine_y, "z": spine_z}, "joint_parent": IDAHO_JOINT_PARENTS[IDAHO_JOINTS(1).name]}

    # Spine Mid (9)avg of Spine and Chest)
    x = ((data[3] + data[6]) / 2) + spine_x
    y = ((data[4] + data[7]) / 2) + spine_y
    z = ((data[5] + data[8]) / 2) + spine_z
    joint_data[IDAHO_JOINTS(2).name] = {"joint_position": {"x": x, "y": y, "z": z}, "joint_parent": IDAHO_JOINT_PARENTS[IDAHO_JOINTS(2).name]}

    # All other joints
    j = 3
    for i in range(9, len(data) - 1, 3):     # -1 since we averaged two the parent joint
        # Get the parent position (parent is always already in the joint_data)
        par_pos = joint_data[IDAHO_JOINT_PARENTS[IDAHO_JOINTS(j).name]]["joint_position"]

        # Get the current joint's absolute position
        x = float(data[i] + par_pos["x"])      # in meters and removing relativity to the parent joint
        y = float(data[i+1] + par_pos["y"])    # in meters and removing relativity to the parent joint
        z = float(data[i+2] + par_pos["z"])    # in meters and removing relativity to the parent joint

        joint_data[IDAHO_JOINTS(j).name] = {"joint_position": {"x": x, "y": y, "z": z}, "joint_parent": IDAHO_JOINT_PARENTS[IDAHO_JOINTS(j).name]}
        j += 1

    print(json.dumps(result))
    return json.dumps(result)


# ------- STANFORD -------

def format_stanford(str):
    result = {"joint_data": {}}
    joint_data = result["joint_data"]
    data = str.split(",")
    data = np.array(data)           # turn into floats
    data = [float(x) for x in data]
    data = [x * 5 for x in data]

    # Create joints data-structure
    j = 0
    for i in range(0, len(data), 3):
        try:
            x = -float(data[i])
            y = -float(data[i+1])
            z = -float(data[i+2])
        except IndexError:
            print("[Kinect][DataFormatter] Incomplete item, not sending")
            return ""

        joint_data[KINECT_JOINTS(j).name] = {"joint_position": {"x": x, "y": y, "z": z}, "joint_parent": KINECT_JOINT_PARENTS[KINECT_JOINTS(j).name]}
        j += 1

    if (j == 25):   # only return if data complete
        return json.dumps(result)
    else:
        print("[Kinect][DataFormatter] Incomplete item, not sending")
        return ""
