from enum import Enum
import json
import numpy as np


# ------ KINECT REFERENCE -----
class KINECT_JOINTS(Enum):
    SPINE_BASE = 0
    SPINE_MID = 1
    NECK = 2
    HEAD = 3
    SHOULDER_LEFT = 4
    ELBOW_LEFT = 5
    WRIST_LEFT = 6
    HAND_LEFT = 7
    SHOULDER_RIGHT = 8
    ELBOW_RIGHT = 9
    WRIST_RIGHT = 10
    HAND_RIGHT = 11
    HIP_LEFT = 12
    KNEE_LEFT = 13
    ANKLE_LEFT = 14
    FOOT_LEFT = 15
    HIP_RIGHT = 16
    KNEE_RIGHT = 17
    ANKLE_RIGHT = 18
    FOOT_RIGHT = 19
    SPINE_SHOULDER = 20
    HAND_TIP_LEFT = 21
    THUMB_LEFT = 22
    HAND_TIP_RIGHT = 23
    THUMB_RIGHT = 24


KINECT_JOINT_PARENTS = {
    'SPINE_BASE': 'SPINE_BASE',
    'SPINE_MID': 'SPINE_BASE',
    'NECK': 'SPINE_MID',
    'HEAD': 'NECK',
    'SHOULDER_LEFT': 'NECK',
    'ELBOW_LEFT': 'SHOULDER_LEFT',
    'WRIST_LEFT': 'ELBOW_LEFT',
    'HAND_LEFT': 'WRIST_LEFT',
    'SHOULDER_RIGHT': 'NECK',
    'ELBOW_RIGHT': 'SHOULDER_RIGHT',
    'WRIST_RIGHT': 'ELBOW_RIGHT',
    'HAND_RIGHT': 'WRIST_RIGHT',
    'HIP_LEFT': 'SPINE_BASE',
    'KNEE_LEFT': 'HIP_LEFT',
    'ANKLE_LEFT': 'KNEE_LEFT',
    'FOOT_LEFT': 'ANKLE_LEFT',
    'HIP_RIGHT': 'SPINE_BASE',
    'KNEE_RIGHT': 'HIP_RIGHT',
    'ANKLE_RIGHT': 'KNEE_RIGHT',
    'FOOT_RIGHT': 'ANKLE_RIGHT',
    'SPINE_SHOULDER': 'SPINE_MID',
    'HAND_TIP_LEFT': 'HAND_LEFT',
    'THUMB_LEFT': 'HAND_LEFT',
    'HAND_TIP_RIGHT': 'HAND_RIGHT',
    'THUMB_RIGHT': 'HAND_RIGHT'
}


# ------- CORNELL -------

class CORNELL_JOINTS(Enum):
    HEAD = 1
    NECK = 2
    TORSO = 3
    LEFT_SHOULDER = 4
    LEFT_ELBOW = 5
    RIGHT_SHOULDER = 6
    RIGHT_ELBOW = 7
    LEFT_HIP = 8
    LEFT_KNEE = 9
    RIGHT_HIP = 10
    RIGHT_KNEE = 11
    LEFT_HAND = 12
    RIGHT_HAND = 13
    LEFT_FOOT = 14
    RIGHT_FOOT = 15


CORNELL_JOINT_PARENTS = {
    'HEAD': 'NECK',
    'NECK': 'TORSO',
    'TORSO': 'TORSO',
    'LEFT_SHOULDER': 'NECK',
    'LEFT_ELBOW': 'LEFT_SHOULDER',
    'RIGHT_SHOULDER': 'NECK',
    'RIGHT_ELBOW': 'RIGHT_SHOULDER',
    'LEFT_HIP': 'TORSO',
    'LEFT_KNEE': 'LEFT_HIP',
    'RIGHT_HIP': 'TORSO',
    'RIGHT_KNEE': 'RIGHT_HIP',
    'LEFT_HAND': 'LEFT_ELBOW',
    'RIGHT_HAND': 'RIGHT_ELBOW',
    'LEFT_FOOT': 'LEFT_KNEE',
    'RIGHT_FOOT': 'RIGHT_KNEE'
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
    SPINE_SHOULDER = 3      # aka neck
    NECK = 4                # aka head
    HEAD = 5                # aka head tip
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
    'NECK': 'SPINE_SHOULDER',
    'HEAD': 'NECK',
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
            return json.dumps(result)

        joint_data[KINECT_JOINTS(j).name] = {"joint_position": {"x": x, "y": y, "z": z}, "joint_parent": KINECT_JOINT_PARENTS[KINECT_JOINTS(j).name]}
        j += 1

    return json.dumps(result)
