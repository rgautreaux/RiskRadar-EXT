using System;
using System.IO.Pipes;
using System.Text;
using System.Threading;

namespace Sender
{
    class Program
    {
        private const string PipeName = "InterProcessMessagePipe";

        static void Main(string[] args)
        {
            Console.WriteLine("=== Message Sender ===");
            Console.WriteLine("Starting Named Pipe Server...");
            Console.WriteLine($"Pipe Name: {PipeName}");
            Console.WriteLine("Waiting for receiver to connect...\n");

            try
            {
                using (var pipeServer = new NamedPipeServerStream(
                    PipeName,
                    PipeDirection.Out,
                    1,
                    PipeTransmissionMode.Message,
                    PipeOptions.Asynchronous))
                {
                    // Wait for client connection
                    pipeServer.WaitForConnection();
                    Console.WriteLine("Receiver connected!");
                    Console.WriteLine("Sending messages every 0.5 seconds...\n");

                    int messageCount = 0;

                    while (true)
                    {
                        messageCount++;
                        string timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff");
                        string message = $"Message #{messageCount} | Timestamp: {timestamp} | Random: {new Random().Next(1000, 9999)}";

                        byte[] messageBytes = Encoding.UTF8.GetBytes(message);

                        try
                        {
                            pipeServer.Write(messageBytes, 0, messageBytes.Length);
                            pipeServer.Flush();
                            Console.WriteLine($"[SENT] {message}");
                        }
                        catch (IOException)
                        {
                            Console.WriteLine("Receiver disconnected. Exiting...");
                            break;
                        }

                        // Wait 0.5 seconds (500 milliseconds)
                        Thread.Sleep(500);
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
                Console.WriteLine("\nPress any key to exit...");
                Console.ReadKey();
            }
        }
    }
}
