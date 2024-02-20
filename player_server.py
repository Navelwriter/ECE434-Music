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
  emit('status', 'Command received: {}'.format(command))

# request a .mp3 file from cluent using request.method == 'POST' 
# also use request.files['file'] to get the file and save it into the /music/ folder
@app.route('/upload', methods=['POST'])
def upload():
  if request.method == 'POST':
    f = request.files['file']
    #check if the file is an mp3 file
    if f.filename[-4:] != '.mp3':
      return 'file is not an mp3 file'
    f.save('/music/' + f.filename)
    return render_template("success.html", name = f.filename)

if __name__ == '__main__':
  socketio.run(app, host='0.0.0.0', port=8081, debug=True)
