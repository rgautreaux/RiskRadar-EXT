# C# Inter-Process Messaging

This project demonstrates inter-process communication (IPC) between two C# console applications using Named Pipes.

## Overview

- **Sender**: Sends messages every 0.5 seconds via Named Pipe
- **Receiver**: Receives and displays messages immediately upon receipt

## Project Structure

```
├── InterProcessMessaging.sln
├── src/
│   ├── Sender/
│   │   ├── Sender.csproj
│   │   └── Program.cs
│   └── Receiver/
│       ├── Receiver.csproj
│       └── Program.cs
```

## Requirements

- .NET 8.0 SDK or later

## Building the Solution

```bash
dotnet build InterProcessMessaging.sln
```

## Running the Applications

### Important: Run in Order

1. **First, start the Sender** (it creates the Named Pipe server):
   ```bash
   dotnet run --project src/Sender/Sender.csproj
   ```

2. **Then, start the Receiver** (in a separate terminal):
   ```bash
   dotnet run --project src/Receiver/Receiver.csproj
   ```

## How It Works

1. The **Sender** creates a Named Pipe server and waits for a connection
2. The **Receiver** connects as a client to the Named Pipe
3. Once connected, the **Sender** transmits a new message every 500ms (0.5 seconds)
4. The **Receiver** displays each message immediately upon receipt with timestamp

## Sample Output

### Sender Output:
```
=== Message Sender ===
Starting Named Pipe Server...
Pipe Name: InterProcessMessagePipe
Waiting for receiver to connect...

Receiver connected!
Sending messages every 0.5 seconds...

[SENT] Message #1 | Timestamp: 2025-12-08 10:30:45.123 | Random: 5847
[SENT] Message #2 | Timestamp: 2025-12-08 10:30:45.623 | Random: 3291
```

### Receiver Output:
```
=== Message Receiver ===
Connecting to sender...
Pipe Name: InterProcessMessagePipe

Connected to sender!
Receiving messages...

[RECEIVED at 2025-12-08 10:30:45.124]
  Message #1 | Timestamp: 2025-12-08 10:30:45.123 | Random: 5847

[RECEIVED at 2025-12-08 10:30:45.624]
  Message #2 | Timestamp: 2025-12-08 10:30:45.623 | Random: 3291
```

## Technical Details

- **IPC Method**: Named Pipes (`System.IO.Pipes`)
- **Pipe Name**: `InterProcessMessagePipe`
- **Message Frequency**: Every 500 milliseconds (0.5 seconds)
- **Message Format**: UTF-8 encoded text with message number, timestamp, and random data
- **Platform**: Cross-platform (Windows, Linux, macOS)
