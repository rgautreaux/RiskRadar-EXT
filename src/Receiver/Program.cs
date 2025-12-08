using System;
using System.IO.Pipes;
using System.Text;

namespace Receiver
{
    class Program
    {
        private const string PipeName = "InterProcessMessagePipe";
        private const int BufferSize = 1024;

        static void Main(string[] args)
        {
            Console.WriteLine("=== Message Receiver ===");
            Console.WriteLine("Connecting to sender...");
            Console.WriteLine($"Pipe Name: {PipeName}\n");

            try
            {
                using (var pipeClient = new NamedPipeClientStream(
                    ".",
                    PipeName,
                    PipeDirection.In,
                    PipeOptions.Asynchronous))
                {
                    // Connect to the sender
                    pipeClient.Connect(5000); // 5 second timeout
                    Console.WriteLine("Connected to sender!");
                    Console.WriteLine("Receiving messages...\n");

                    byte[] buffer = new byte[BufferSize];

                    while (pipeClient.IsConnected)
                    {
                        try
                        {
                            int bytesRead = pipeClient.Read(buffer, 0, buffer.Length);

                            if (bytesRead > 0)
                            {
                                string message = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                                string receivedTime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff");

                                Console.ForegroundColor = ConsoleColor.Green;
                                Console.WriteLine($"[RECEIVED at {receivedTime}]");
                                Console.ForegroundColor = ConsoleColor.White;
                                Console.WriteLine($"  {message}\n");
                                Console.ResetColor();
                            }
                        }
                        catch (Exception ex)
                        {
                            Console.WriteLine($"Error reading message: {ex.Message}");
                            break;
                        }
                    }

                    Console.WriteLine("Sender disconnected.");
                }
            }
            catch (TimeoutException)
            {
                Console.WriteLine("Connection timeout. Make sure the Sender is running first.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }

            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }
    }
}
