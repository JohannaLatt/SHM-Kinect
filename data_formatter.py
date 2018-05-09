from enum import Enum
import json

# ------ KINECT REFERENCE -----
class JOINTS(Enum):
    SPINE_BASE = 0
    SPINE_MID = 1
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
    NONE = 25


JOINT_PARENTS = {
    JOINTS.SPINE_BASE: JOINTS.NONE,
    JOINTS.SPINE_MID: JOINTS.SPINE_BASE,
    JOINTS.HEAD: JOINTS.SPINE_MID,
    JOINTS.SHOULDER_LEFT: JOINTS.SPINE_SHOULDER,
    JOINTS.ELBOW_LEFT: JOINTS.SHOULDER_LEFT,
    JOINTS.WRIST_LEFT: JOINTS.ELBOW_LEFT,
    JOINTS.HAND_LEFT: JOINTS.WRIST_LEFT,
    JOINTS.SHOULDER_RIGHT: JOINTS.SPINE_SHOULDER,
    JOINTS.ELBOW_RIGHT: JOINTS.SHOULDER_RIGHT,
    JOINTS.WRIST_RIGHT: JOINTS.ELBOW_RIGHT,
    JOINTS.HAND_RIGHT: JOINTS.WRIST_RIGHT,
    JOINTS.HIP_LEFT: JOINTS.SPINE_BASE,
    JOINTS.KNEE_LEFT: JOINTS.HIP_LEFT,
    JOINTS.ANKLE_LEFT: JOINTS.KNEE_LEFT,
    JOINTS.FOOT_LEFT: JOINTS.ANKLE_LEFT,
    JOINTS.HIP_RIGHT: JOINTS.SPINE_BASE,
    JOINTS.KNEE_RIGHT: JOINTS.HIP_RIGHT,
    JOINTS.ANKLE_RIGHT: JOINTS.KNEE_RIGHT,
    JOINTS.FOOT_RIGHT: JOINTS.ANKLE_RIGHT,
    JOINTS.SPINE_SHOULDER: JOINTS.SPINE_MID,
    JOINTS.HAND_TIP_LEFT: JOINTS.HAND_LEFT,
    JOINTS.THUMB_LEFT: JOINTS.HAND_LEFT,
    JOINTS.HAND_TIP_RIGHT: JOINTS.HAND_RIGHT,
    JOINTS.THUMB_RIGHT: JOINTS.HAND_RIGHT,
    JOINTS.NONE: JOINTS.NONE
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
        x = float(data[i])      # in meters
        y = float(data[i+1])    # in meters
        z = float(data[i+2])    # in meters

        joint_data[CORNELL_JOINTS(j).name] = {"joint_position": {"x": x, "y": y, "z": z}, "joint_parent": CORNELL_JOINT_PARENTS[CORNELL_JOINTS(j).name]}
        j += 1
    for i in range(155, 168, 4):
        x = float(data[i])     # in meters
        y = float(data[i+1])   # in meters
        z = float(data[i+2])   # in meters

        joint_data[CORNELL_JOINTS(j).name] = {"joint_position": {"x": x, "y": y, "z": z}, "joint_parent": CORNELL_JOINT_PARENTS[CORNELL_JOINTS(j).name]}
        j += 1

    return json.dumps(result)


def format_stanford(str):
    # TODO
    return str
