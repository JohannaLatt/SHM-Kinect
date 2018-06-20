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
        public Dictionary<string, float[]> joint_data = new Dictionary<string, float[]>();
    }

}
