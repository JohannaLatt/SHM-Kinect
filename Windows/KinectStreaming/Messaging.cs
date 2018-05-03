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

        public static void Init()
        {
            var factory = new ConnectionFactory() { HostName = "10.171.18.216", UserName = "Kinect", Password = "kinect" };  // Mac
            var connection = factory.CreateConnection();

            channel = connection.CreateModel();
            channel.QueueDeclare(queue: "queue-from-kinect",
                                durable: false,
                                exclusive: false,
                                autoDelete: false,
                                arguments: null);
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
                        channel.BasicPublish(exchange: "from-kinect",
                                        routingKey: msg.Key,
                                        basicProperties: null,
                                        body: Encoding.UTF8.GetBytes(msg.Value));
                        Console.WriteLine("Sent: " + msg.Value);
                    } else
                    {
                        continue;
                    }
                }
            }
        }
    }
}
