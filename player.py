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
from flask import Flask, render_template, request
import gpiod

app = Flask(__name__)
folder_path = "/home/debian/ECE434-Music/music"
player = None

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
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".mp3"):
                    self.song_list.append(file)
        print(self.song_list)

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
            self.song_index -= 1
            if self.song_index < 0:
                self.song_index = len(self.song_list) - 1
            self.set_song(self.song_list[self.song_index])
            mixer.music.play()
            self.is_Paused = False

    def startMusic(self):
        mixer.music.play()

    def drawTitle(self, font):
        # clear the screen before drawing
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.size[0], 50))
        text = font.render(self.song, 1, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def draw(self):
        # display the name of the song on the screen
        font = pygame.font.Font(None, 36) 
        self.drawTitle(font)
        # display the progress of the song on the screen as text 
        pos = mixer.music.get_pos()
        minutes = math.floor(pos/60000)
        seconds = (pos%60000)/1000
        seconds = math.floor(seconds)
        # add a leading zero if seconds is less than 10
        if seconds < 10:
            seconds = "0" + str(seconds)
        text = font.render(str(minutes) + ":" + str(seconds), 1, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 50, 100, 50))
        self.screen.blit(text, (10, 50))
        # print(pos)
        if int(pos) < 0:
            print("Playing next song")
            self.command("Next")
        #get the total length of the song 
        length = self.song_info.info.length
        minutes = math.floor(length/60)
        seconds = length%60
        #truncate to 0 decimal places and only have minutes and seconds
        seconds = math.floor(seconds)
        text = font.render(str(minutes) + ":" + str(seconds), 1, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.size[0]-110, 50, 100, 50))
        self.screen.blit(text, (self.size[0]-110, 50))

CONSUMER='getset'
CHIP='1'
getoffsets=[14, 15, 18, 16] # P8_16, P8_15, P9_14, P9_15

chip = gpiod.Chip(CHIP) # Open the GPIO chip
getlines = chip.get_lines(getoffsets) # Get the GPIO lines
getlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_BOTH_EDGES)

eQEP = '2'
COUNTERPATH = '/dev/bone/counter/' + eQEP + '/count0'

#ms = 100 # time between samples in ms
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

# Start playing the song 
mixer.init()
player = pyPlayer()
player.startMusic()

vol = 0.7
#sio.start_background_task(start_listener, player)

print("Press 'p' to pause, 'r' to resume, 's' to stop, 'q' to quit")
while True:
    player.draw()
    pygame.display.update()
    get_input(player)
    f.seek(0)
    data = f.read()[:-1]
    # print only if data changes
    # print("data: " + data + " " + str(type(data)))
    # print("olddata: " + str(olddata) + " " + str(type(olddata)))
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
    #time.sleep(ms/1000)
    
    # time.sleep(0.1)
