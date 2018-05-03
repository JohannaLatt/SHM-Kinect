using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace KinectStreaming
{
    /// <summary>
    /// Serialization classes
    /// </summary>
    public class SkeletonData
    {
        public List<JointData> joint_data = new List<JointData>();
    }

    public class JointData
    {
        public string joint_type;
        public JointPosition joint_position;

        public JointData(string joint_type, Tuple<float, float, float> joint_position)
        {
            this.joint_type = joint_type;
            this.joint_position = new JointPosition(joint_position.Item1, joint_position.Item2, joint_position.Item3);
        }
    }

    public class JointPosition
    {
        public float x;
        public float y;
        public float z;

        public JointPosition(float x, float y, float z)
        {
            this.x = x;
            this.y = y;
            this.z = z;
        }
    }

}
