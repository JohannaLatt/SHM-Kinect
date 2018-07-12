using RabbitMQ.Client;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Text;

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

            channel.ExchangeDeclare(exchange: "from-kinect-skeleton", type: "fanout");
            channel.ExchangeDeclare(exchange: "from-kinect-color", type: "fanout");
        }

        public static void StartMessaging(ConcurrentQueue<KeyValuePair<string, string>> msg_queue)
        {
            if (channel == null)
                Console.WriteLine("Error! Channel not initialized yet.");
            else
            {
                while (true)
                {
                    KeyValuePair<string, string> msg = new KeyValuePair<string, string>();
                    if (msg_queue.TryDequeue(out msg))
                    {
                        if (msg.Key.Equals('COLOR_DATA'))
                        {
                            channel.BasicPublish(exchange: "from-kinect-color",
                                        routingKey: msg.Key,
                                        basicProperties: null,
                                        body: Encoding.UTF8.GetBytes(msg.Value));
                        }
                        else
                        {
                            channel.BasicPublish(exchange: "from-kinect-skeleton",
                                        routingKey: msg.Key,
                                        basicProperties: null,
                                        body: Encoding.UTF8.GetBytes(msg.Value));
                        }
                        // Console.WriteLine("Sent: " + msg.Value);
                    } else
                    {
                        continue;
                    }
                }
            }
        }
    }
}
