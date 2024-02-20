#!/bin/bash
#check if the script is run as root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

#check if there is already a tmux session named music_control running
# if there is, kill it 
tmux has-session -t music_control 2>/dev/null # if there is a session, return 0
if [ $? == 0 ]; then
    tmux kill-session -t music_control
fi
# Start a new tmux session (or attach to existing one if it's running)
tmux new-session -d -s music_control

# Split the window vertically into two panes 
tmux split-window -v

# Send the command to the first pane (server)
tmux send-keys -t 0 "sudo ./player_server.py" C-m  # 'C-m' represents the Enter key

# Move to the second pane (client)
tmux select-pane -t 1

echo "waiting for server to start..."

sleep 10 #wait for server to start

# Send the command to the second pane
tmux send-keys -t 1 "sudo ./player_client.py" C-m 

# Attach to the session
tmux attach-session -t music_control

