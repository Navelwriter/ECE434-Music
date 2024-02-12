#!/bin/bash
# Check if the user is root
if [ $(id -u) -ne 0 ]; then
    echo "You must be root to run this script"
    exit 1
fi

# This runs ./player_server.py in the background and stores the process id in a file
# This then run ./player.py in the foreground
# When ./player.py is killed, the process id of ./player_server.py is read from the file and the process is killed
./player_server.py &
SERVER_PID=$!
echo $SERVER_PID > /tmp/player_server.pid
# wait for the server to start
echo "Server is starting..."
sleep 12
# Let the user know that the server is running in http://192.168.7.2:8081/
echo "Server is running in http://192.169.7.2:8081/"

./player.py

echo "Shutting down server"
kill $(cat /tmp/player_server.pid)
# Remove the file
rm /tmp/player_server.pid
```
