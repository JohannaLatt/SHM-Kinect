﻿using System;
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

        /// <summary>
        /// Parent-child-bone mapping (see https://msdn.microsoft.com/en-us/library/microsoft.kinect.jointtype.aspx)
        /// </summary>
        private Dictionary<JointType, JointType> parent_joints = new Dictionary<JointType, JointType>()
            {
                { JointType.Head, JointType.Neck },
                { JointType.Neck, JointType.SpineShoulder },
                { JointType.SpineShoulder, JointType.SpineShoulder },
                { JointType.SpineBase, JointType.SpineMid },
                { JointType.SpineMid, JointType.SpineShoulder },

                { JointType.HandTipLeft, JointType.HandLeft },
                { JointType.HandLeft, JointType.WristLeft },
                { JointType.ThumbLeft, JointType.WristLeft },

                { JointType.WristLeft, JointType.ElbowLeft },
                { JointType.ElbowLeft, JointType.ShoulderLeft },
                { JointType.ShoulderLeft, JointType.SpineShoulder },

                { JointType.FootLeft, JointType.AnkleLeft },
                { JointType.AnkleLeft, JointType.KneeLeft },
                { JointType.KneeLeft, JointType.HipLeft },
                { JointType.HipLeft, JointType.SpineBase },

                { JointType.HandTipRight, JointType.HandRight },
                { JointType.HandRight, JointType.WristRight },
                { JointType.ThumbRight, JointType.WristRight },

                { JointType.WristRight, JointType.ElbowRight },
                { JointType.ElbowRight, JointType.ShoulderRight },
                { JointType.ShoulderRight, JointType.SpineShoulder },

                { JointType.FootRight, JointType.AnkleRight },
                { JointType.AnkleRight, JointType.KneeRight },
                { JointType.KneeRight, JointType.HipRight },
                { JointType.HipRight, JointType.SpineBase }
            };

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
                foreach (Body body in this.bodies)
                {
                    if (body.IsTracked)
                    {

                        // Iterate through joints and build the result string
                        SkeletonData frame_data = new SkeletonData();

                        foreach (KeyValuePair<JointType, Joint> joint in body.Joints)
                        {
                            JointData jointData = new JointData(new Tuple<float, float, float>(joint.Value.Position.X, joint.Value.Position.Y, joint.Value.Position.Z), parent_joints[joint.Key].ToString());
                            frame_data.joint_data.Add(joint.Key.ToString(), jointData);
                        }

                        string result = new JavaScriptSerializer().Serialize(frame_data);

                        // Send the data to listeners
                        OnSkeletonData(result);
                    }
                }
            }
        }
    }

}