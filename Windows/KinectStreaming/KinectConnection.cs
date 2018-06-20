using System;
using System.Collections.Generic;
using System.Web.Script.Serialization;
using Microsoft.Kinect;

namespace KinectStreaming
{
    class KinectConnection
    {

        /// <summary>
        /// Active Kinect sensor
        /// </summary>
        private KinectSensor kinectSensor = null;

        /// <summary>
        /// Coordinate mapper to map one type of point to another
        /// </summary>
        private CoordinateMapper coordinateMapper = null;

        /// <summary>
        /// Reader for body frames
        /// </summary>
        private BodyFrameReader bodyFrameReader = null;

        /// <summary>
        /// Array for the bodies
        /// </summary>
        private Body[] bodies = null;

        /// <summary>
        /// definition of bones
        /// </summary>
        private List<Tuple<JointType, JointType>> bones;

        /// <summary>
        /// Constant for clamping Z values of camera space points from being negative
        /// </summary>
        private const float InferredZPositionClamp = 0.1f;

        /// <summary>
        /// Event handling when new skeleton data is available
        /// </summary>
        public delegate void SkeletonDataHandler(string data);
        public event SkeletonDataHandler OnSkeletonData;

        public delegate void TrackingStartedHandler();
        public event TrackingStartedHandler OnTrackingStarted;

        public delegate void TrackingLostHandler();
        public event TrackingLostHandler OnTrackingLost;

        /// <summary>
        /// Keeps track of the tracking status over frames
        /// </summary>
        private bool isTracking = false;

        public KinectConnection()
        {
            // one sensor is currently supported
            this.kinectSensor = KinectSensor.GetDefault();

            // get the coordinate mapper
            this.coordinateMapper = this.kinectSensor.CoordinateMapper;

            // get the depth (display) extents
            FrameDescription frameDescription = this.kinectSensor.DepthFrameSource.FrameDescription;

            // open the reader for the body frames
            this.bodyFrameReader = this.kinectSensor.BodyFrameSource.OpenReader();

            // set FrameArrived event notifier
            this.bodyFrameReader.FrameArrived += this.Reader_FrameArrived;

            // set IsAvailableChanged event notifier
            //this.kinectSensor.IsAvailableChanged += this.Sensor_IsAvailableChanged;

            // open the sensor
            this.kinectSensor.Open();
        }

        public void Destroy()
        {
            if (this.bodyFrameReader != null)
            {
                // BodyFrameReader is IDisposable
                this.bodyFrameReader.Dispose();
                this.bodyFrameReader = null;
            }

            if (this.kinectSensor != null)
            {
                this.kinectSensor.Close();
                this.kinectSensor = null;
            }
        }

        /// <summary>
        /// Handles the body frame data arriving from the sensor
        /// </summary>
        /// <param name="sender">object sending the event</param>
        /// <param name="e">event arguments</param>
        private void Reader_FrameArrived(object sender, BodyFrameArrivedEventArgs e)
        {
            bool dataReceived = false;

            using (BodyFrame bodyFrame = e.FrameReference.AcquireFrame())
            {
                if (bodyFrame != null)
                {
                    if (this.bodies == null)
                    {
                        this.bodies = new Body[bodyFrame.BodyCount];
                    }

                    // The first time GetAndRefreshBodyData is called, Kinect will allocate each Body in the array.
                    // As long as those body objects are not disposed and not set to null in the array,
                    // those body objects will be re-used.
                    bodyFrame.GetAndRefreshBodyData(this.bodies);
                    dataReceived = true;
                }  
            }

            if (dataReceived)
            {
                // We only care about the active body
                Body body = GetActiveBody();

                if (body != null)
                {
                    // Check if newly tracked
                    if (!isTracking)
                    {
                        // Send tracking started
                        OnTrackingStarted();

                        // Set internal variable for next frame
                        isTracking = true;
                    }

                    // Iterate through joints and build the result string
                    Dictionary<string, float[]> frame_data = new Dictionary<string, float[]>();

                    foreach (KeyValuePair<JointType, Joint> joint in body.Joints)
                    {
                        // Retrieve the position and convert it to millimeters
                        float[] jointData = new float[] { joint.Value.Position.X * 1000, joint.Value.Position.Y * 1000, joint.Value.Position.Z * 1000 };
                        frame_data.Add(joint.Key.ToString(), jointData);
                    }

                    string result = new JavaScriptSerializer().Serialize(frame_data);

                    // Send the data to listeners
                    OnSkeletonData(result);
                } else if (isTracking)
                {
                    // Send tracking lost
                    OnTrackingLost();

                    // Set internal variable for next frame
                    isTracking = false;
                }
            }
        }

        private ulong currTrackingId = 0;
        private Body GetActiveBody()
        {
            if (currTrackingId <= 0)
            {
                foreach (Body body in this.bodies)
                {
                    if (body.IsTracked)
                    {
                        currTrackingId = body.TrackingId;
                        return body;
                    }
                }

                return null;
            }
            else
            {
                foreach (Body body in this.bodies)
                {
                    if (body.IsTracked && body.TrackingId == currTrackingId)
                    {
                        return body;
                    }
                }
            }

            currTrackingId = 0;
            return GetActiveBody();
        }
    }

}
