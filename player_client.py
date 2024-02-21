#!/usr/bin/env python3
import sys
import getpass
if getpass.getuser() != 'root':
    sys.exit("Must be run as root.")
import os
from pygame import mixer
import pygame
import math
import time
from mutagen.mp3 import MP3
import gpiod
from flask import Flask, render_template, request
import socketio
app = Flask(__name__)
folder_path = "/home/debian/ECE434-Music/music"
player = None
white_color = (255, 255, 255)
black_color = (0, 0, 0)

class pyPlayer :
    screen = None
    mix = None
    is_Paused = False
    song_list = []
    song_index = 0
    song = ""
    song_info = ""
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        os.putenv('SDL_NOMOUSE', '1')
        pygame.display.init()
        self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print("Framebuffer size: ", self.size[0], "x", self.size[1])
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Turn off cursor
        pygame.mouse.set_visible(False)
        # Initialise font support
        pygame.font.init()
        self.scan_music()
        # Loading the first song 
        self.set_song(self.song_list[self.song_index])
        # Setting the volume 
        mixer.music.set_volume(0.7) 

    def scan_music(self):
        list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".mp3"):
                    list.append(file)
        print(list)
        self.song_list = list
        

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc." 

    def set_song(self, song):
        self.song = song
        print(folder_path)
        path = folder_path + "/" + song
        mixer.music.load(path)
        self.song_info = MP3(path)

    def command(self, cmd):
        "Processes a single command"
        print(cmd)
        if cmd == "Play/Pause":
            if self.is_Paused:
                mixer.music.unpause()
                self.is_Paused = False
            else:
                mixer.music.pause()
                self.is_Paused = True
        elif cmd == "Quit":
            mixer.music.stop()
            pygame.quit()
            sys.exit()
        elif cmd == "Next":
            self.song_index += 1
            if self.song_index >= len(self.song_list):
                self.song_index = 0
            self.set_song(self.song_list[self.song_index])
            mixer.music.play()
            self.is_Paused = False
        elif cmd == "Previous":
            if mixer.music.get_pos() < 3000:
                self.song_index -= 1
            if self.song_index < 0:
                self.song_index = len(self.song_list) - 1
            self.set_song(self.song_list[self.song_index])
            mixer.music.play()
            self.is_Paused = False
        elif cmd == "Refresh":
            self.scan_music()


    def startMusic(self):
        mixer.music.play()

    def drawTitle(self, font):
        # clear the screen before drawing
        shape = (0, 0, self.size[0], 50) # x, y, width, height
        pygame.draw.rect(self.screen, black_color, shape)
        # cut the .mp3 from the song name
        song_name = self.song[:-4]
        # append index/total to the song name
        song_name = str(self.song_index+1) + "/" + str(len(self.song_list)) + " " + song_name
        text = font.render(song_name, 1, white_color)
        self.screen.blit(text, (10, 10))

    def drawVolume(self, font):
        # display the volume on the screen as text
        vol = mixer.music.get_volume()
        vol = round(vol, 2)
        vol = vol * 100
        vol = int(vol)
        text = font.render("Volume: " + str(vol), 1, white_color)
        #display on bottom left
        shape = (10, self.size[1]-50, 150, 50) # x, y, width, height
        text_location = (10, self.size[1]-50)
        pygame.draw.rect(self.screen, black_color, shape)
        self.screen.blit(text, text_location)

    def getTime(self, time):
        minutes = math.floor(time/60)
        seconds = time%60
        seconds = math.floor(seconds)
        if seconds < 10:
            seconds = "0" + str(seconds)
        return str(minutes) + ":" + str(seconds)

    def draw(self):
        # display the name of the song on the screen
        font = pygame.font.Font(None, 36) 
        self.drawTitle(font)

        # display the progress of the song on the screen as text 
        pos = mixer.music.get_pos()
        # convert from milliseconds to seconds 
        pos = pos/1000
        time = self.getTime(pos)
        text = font.render(time, 1, white_color)
        shape = (10, 90, 100, 50) # x, y, width, height
        text_location = (10, 90) # x, y
        pygame.draw.rect(self.screen, black_color, shape) #this prevents overlapping of text
        self.screen.blit(text, text_location) 

        #get the total length of the song 
        length = self.song_info.info.length
        time = self.getTime(length)
        text = font.render(time, 1, white_color)
        shape = (self.size[0]-110, 90, 100, 50) # x, y, width, height
        text_location = (self.size[0]-110, 90) # x, y
        pygame.draw.rect(self.screen, black_color, shape)
        self.screen.blit(text, text_location)

        self.drawVolume(font)

        progress = round(pos/length, 2) # get the progress of the song as a percentage
        if pos < 0:
            self.command("Next")
        # draw a rectangle on the screen to represent the progress of the song
        shape = (0, 50, self.size[0], 25) # x, y, width, height
        pygame.draw.rect(self.screen, black_color, shape)
        shape = (0, 50, self.size[0]*progress, 25) # x, y, width, height
        pygame.draw.rect(self.screen, white_color, shape)


CONSUMER='getset'
CHIP='1'
getoffsets=[14, 15, 18, 16] # P8_16, P8_15, P9_14, P9_15

chip = gpiod.Chip(CHIP) # Open the GPIO chip
getlines = chip.get_lines(getoffsets) # Get the GPIO lines
getlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_BOTH_EDGES)

eQEP = '2'
COUNTERPATH = '/dev/bone/counter/' + eQEP + '/count0'

maxCount = '1000000'

# set eQEP max count
f = open(COUNTERPATH+ '/ceiling', 'w')
f.write(maxCount)
f.close()

# Enable
f = open(COUNTERPATH + '/enable', 'w')
f.write('1')
f.close()
f =  open(COUNTERPATH + '/count', 'r')

olddata = '1'

def get_input(player):
    vals = getlines.get_values()
    ev_lines = getlines.event_wait(sec=1)
    if ev_lines:
        for line in ev_lines:
            event = line.event_read()
    if(vals[2] == 1):
        player.command("Play/Pause")
    elif(vals[1] == 1):
        player.command("Next")
    elif(vals[3] == 0):
        player.command("Previous")
    elif(vals[0] == 1):
        player.command("Quit")

# create socketio client
sio = socketio.Client()
sio.connect('http://localhost:8081')

def start_listener(player):
    @sio.on('command')
    def on_command(data):
        print('I received a command: ', data)
        player.command(data)

# Start playing the song 
mixer.init()
player = pyPlayer()
player.startMusic()
sio.start_background_task(start_listener, player)
vol = 0.7

print("Connected to Server: Connect to http://192.168.7.2:8081/")
while True:
    player.draw()
    pygame.display.update()
    get_input(player)
    f.seek(0)
    data = f.read()[:-1]
    if data != olddata:
        if(data > olddata):
            vol += 0.1
        else:
            vol -= 0.1
        olddata = data
        if(vol > 1):
            vol = 1.0
        elif(vol < 0):
            vol = 0.0
        vol = round(vol, 2)
        mixer.music.set_volume(vol) 
        print("volume = " + str(vol))
