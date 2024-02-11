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

class pyPlayer :
    screen = None;
    mix = None;
    bar_width = 5
    bars = []
    song = "hina.mp3"
    song_info = MP3(song)
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        # os.putenv('SDL_FBDEV',   '/dev/fb0')
        # os.putenv('SDL_VIDEODRIVER', driver)
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
        # Loading the song 
        mixer.music.load("hina.mp3") 
        # Setting the volume 
        mixer.music.set_volume(0.7) 

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc." 
    def command(self, cmd):
        "Processes a single command"
        if cmd == "pause":
            mixer.music.pause()
        elif cmd == "unpause":
            mixer.music.unpause()
        elif cmd == "stop":
            mixer.music.stop()
        elif cmd == "quit":
            pygame.quit()
            sys.exit()
    def checkInput(self):
        "Check for any input events and return the command string"
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return "pause"
                elif event.key == pygame.K_r:
                    return "unpause"
                elif event.key == pygame.K_s:
                    return "stop"
                elif event.key == pygame.K_q:
                    return "quit"
        return ""

    def startMusic(self):
        mixer.music.play()

    def draw(self):
        # display the name of the song on the screen
        font = pygame.font.Font(None, 36)
        text = font.render(self.song, 1, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        # display the progress of the song on the screen as text 
        pos = mixer.music.get_pos()
        minutes = math.floor(pos/60000)
        seconds = (pos%60000)/1000
        seconds = math.floor(seconds)
        #if the seconds are less than 10, add a 0 in front of it
        if seconds < 10:
            text = font.render(str(minutes) + ":0" + str(seconds), 1, (255, 255, 255))
        else:
            text = font.render(str(minutes) + ":" + str(seconds), 1, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 50, 100, 50))
        self.screen.blit(text, (10, 50))
        #get the total length of the song 
        length = self.song_info.info.length
        minutes = math.floor(length/60)
        seconds = length%60
        #truncate to 0 decimal places and only have minutes and seconds
        seconds = math.floor(seconds)
        text = font.render(str(minutes) + ":" + str(seconds), 1, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.size[0]-110, 50, 100, 50))
        self.screen.blit(text, (self.size[0]-110, 50))











# Start playing the song 
mixer.init()
player = pyPlayer()
player.startMusic()
print("Press 'p' to pause, 'r' to resume, 's' to stop, 'q' to quit")
while True:
    cmd = player.checkInput()
    player.command(cmd)
    player.draw()
    pygame.display.update()
    time.sleep(0.1)
