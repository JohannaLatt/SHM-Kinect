using RabbitMQ.Client;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;

namespace KinectStreaming
{
    static class Messaging
    {

        private static IModel channel;

        public static void Init(string ip)
        { 
            var factory = new ConnectionFactory() { HostName = ip, UserName = "Kinect", Password = "kinect" };  // Mac
            var connection = factory.CreateConnection();

            channel = connection.CreateModel();

            channel.ExchangeDeclare(exchange: "from-kinect-skeleton", type: "direct");
            channel.ExchangeDeclare(exchange: "from-kinect-color", type: "direct");
        }

        public static void StartMessaging(ConcurrentQueue<KeyValuePair<string, byte[]>> msg_queue)
        {
            if (channel == null)
                Console.WriteLine("Error! Channel not initialized yet.");
            else
            {
                while (true)
                {
                    KeyValuePair<string, byte[]> msg = new KeyValuePair<string, byte[]>();
                    if (msg_queue.TryDequeue(out msg))
                    {
                        if (msg.Key.Equals("COLOR_DATA"))
                        {
                            channel.BasicPublish(exchange: "from-kinect-color",
                                        routingKey: msg.Key,
                                        basicProperties: null,
                                        body: msg.Value);
                        }
                        else
                        {
                            // TODO: Switch to UDP streaming for this, RabbitMQ is too slow and cannot handle this 
                            // many messages, resulting in an out of memory exception
                            //channel.BasicPublish(exchange: "from-kinect-skeleton",
                            //            routingKey: msg.Key,
                            //            basicProperties: null,
                            //            body: msg.Value);
                            continue;
                        }
                    }
                   
                }
            }
        }
    }
}
