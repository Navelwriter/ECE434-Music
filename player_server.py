#!/usr/bin/env python3
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
  return render_template('index.html')

@socketio.on('control')
def handle_control(data):
  command = data['command']
  print('Command:', command)
  socketio.emit('command', command) # Send command to client
  emit('status', 'Command received: {}'.format(command)) # Send status to client


if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0', port=8081, debug=True)
