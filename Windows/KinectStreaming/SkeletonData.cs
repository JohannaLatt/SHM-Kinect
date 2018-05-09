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
        public Dictionary<string, JointData> joint_data = new Dictionary<string, JointData>();
    }

    public class JointData
    {
        public JointPosition joint_position;
        public string joint_parent;

        public JointData(Tuple<float, float, float> position, string parent)
        {
            joint_position = new JointPosition(position.Item1, position.Item2, position.Item3);
            joint_parent = parent;
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
