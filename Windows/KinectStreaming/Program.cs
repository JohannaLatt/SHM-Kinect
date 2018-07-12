using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Threading;
using System.Text;

namespace KinectStreaming
{
    class Program
    {

        private static ConcurrentQueue<KeyValuePair<string, byte[]>> msg_queue = new ConcurrentQueue<KeyValuePair<string, byte[]>>();

        static void Main(string[] args)
        {
            Console.Clear();
            Console.WriteLine("Application started. Press Esc to stop.");

            Console.Write("Enter IP Address of RabbitMQ (hit enter for default): ");
            var ip = Console.ReadLine();
            if (string.IsNullOrEmpty(ip))
            {
                ip = "10.171.18.216";                
            } 
            Console.WriteLine("Loading Messaging Service..");
            Messaging.Init(ip);
            Thread messagingThread = new Thread(() => Messaging.StartMessaging(msg_queue));
            messagingThread.Start();

            Console.WriteLine("Messaging ready. Loading Kinect..");
            KinectConnection kinect = new KinectConnection();

            Console.WriteLine("Kinect connected. Waiting for skeleton data..");
            kinect.OnSkeletonData += PrintSkeletonData;
            kinect.OnSkeletonData += SendSkeletonData;
            kinect.OnColorData += SendColorData;
            kinect.OnTrackingStarted += SendTrackingStarted;
            kinect.OnTrackingLost += SendTrackingLost;

            while (!(Console.KeyAvailable && Console.ReadKey(true).Key == ConsoleKey.Escape))
            {
                // do something
            }

            // Cleanup
            kinect.Destroy();
            messagingThread.Abort();
        }

        private static void PrintSkeletonData(string data)
        {
            Console.WriteLine(data);
        }

        private static void SendSkeletonData(string data)
        {
            msg_queue.Enqueue(new KeyValuePair<string, byte[]>("TRACKING_DATA", Encoding.UTF8.GetBytes(data)));
        }

        private static void SendColorData(byte[] data)
        {
            msg_queue.Enqueue(new KeyValuePair<string, byte[]>("COLOR_DATA", data));
        }

        private static void SendTrackingStarted()
        {
            Console.WriteLine("TRACKING_STARTED");
            msg_queue.Enqueue(new KeyValuePair<string, byte[]>("TRACKING_STARTED", Encoding.UTF8.GetBytes("")));
        }

        private static void SendTrackingLost()
        {
            Console.WriteLine("TRACKING_LOST");   
            msg_queue.Enqueue(new KeyValuePair<string, byte[]>("TRACKING_LOST", Encoding.UTF8.GetBytes("")));
        }
    }

}
