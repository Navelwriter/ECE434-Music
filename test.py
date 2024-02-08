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

class pyPlayer :
    screen = None;
    mix = None;
    bar_width = 5
    bars = []
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
        mixer.music.load("piano2.wav") 
        # Setting the volume 
        mixer.music.set_volume(0.7) 
        self.bars = [pygame.Rect(x * self.bar_width, self.size[1] // 2, self.bar_width, self.size[1] // 2) for x in range(int(self.size[0] / self.bar_width))]

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc." 

    def startMusic(self):
        mixer.music.play()
        while True:
            currentTime = time.localtime()
            hour = currentTime[3]%12    # Convert to 12 hour time
            minute = currentTime[4]
            second = currentTime[5]

            # Get audio data and update visualization
            data = mixer.music.get_pos()  # Get current position in milliseconds
            volume = mixer.music.get_volume()  # Get current volume (0.0 to 1.0)
            scaled_volume = int(volume * self.size[1] // 2)
            #print("Time: ", hour, ":", minute, ":", second)
            print("volume: ", volume)

            # Update bar heights based on volume
            for i, bar in enumerate(self.bars):
                bar.height = scaled_volume * (math.sin(i * 0.1 + data * 0.001) + 1) // 2
                            # Clear screen and redraw bars

            self.screen.fill((0, 0, 0))
            for bar in self.bars:
                pygame.draw.rect(self.screen, (255, 255, 255), bar)

            pygame.display.update
            pygame.time.wait(200)
  
# Start playing the song 
mixer.init()
player = pyPlayer()
player.startMusic()
