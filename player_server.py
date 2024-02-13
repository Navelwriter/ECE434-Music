#!/usr/bin/env python3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<control>')
def handle_control(data):
    command = data['command']
    print('Command:', command)
    #clear commands.txt and write the new command
    with open('commands.txt', 'w') as file:
        #clear the file
        file.write('')
        file.write(command)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
