# ECE434-Music
## Summary
This is a mp3-player for the BeagleBone Black SBC. 
## Hardware Setup
#### Needed Materials
1. 2.4" TFT LCD display via SPI (ili9341)
2. 4x Pushbuttons
3. eQEP Rotary Encoder
4. Driverless USB Stereo Audio Adapter [Example product here](https://www.amazon.com/dp/B00IRVQ0F8)
#### LCD Installation
| LCD Label | Pin Location |
| ------------ | ----- |
| MISO | P9_21 |
| LED | P9_16 |
| SCK | P9_22 | 
| MOSI | P9_18 |
| D/C | P9_19 |
| RESET | P9_20 |
| CS | P9_17 |
| GND | P9_2 |
| VCC | P9_4 |
#### Pushbutton Location
| Function | Pin A | Pin B |
| ------------ | ----- | ----- |
| QUIT | P8_16 | VCC |
| Next Song | P8_15 | VCC |
| Play/Pause | P9_14 | VCC |
| Previous Song | P9_15 | GND |

#### Rotary Encoder Installation
<img src="https://github.com/Navelwriter/ECE434-Music/assets/77686570/cb78c29c-554a-4236-a5cd-7b19a4df42a7" width="30%" height="30%"> \
This is using eQEP2 on BeagleBoard:
|Function| GND | Pin A | Pin B |
|-----| ------------ | ----- | ----- |
|Volume| GND | P8_11 | P8_12 |

## Driver Setup and Install
Download the repository in a folder of your choosing
#### LCD Device Tree Install
Either copy uEnv.txt from the repository into /boot or follow the following instructions:

Edit /boot/uEnv.txt and find the line starting with \
``#uboot_overlay_addr4=``

Uncomment it and change it to: \
``uboot_overlay_addr4=/lib/firmware/BB-LCD-ADAFRUIT-24-SPI0-00A0.dtbo``

Further down uncomment the following lines to disable the hdmi audio and video from overriding the usb audio device: \
``#disable_uboot_overlay_video=1``\
``#disable_uboot_overlay_audio=1``

Inside the ECE343-Music folder from downloading the repo, run the following scripts\
``sudo ./installDep.sh`` This installs the necessary packages\
``sudo ./install.sh`` This adds the music player as a systemd package and runs the app

## Instructions
### Music Install
Install any number of music files by inserting only ``.mp3`` files into the ``/music/`` folder of the respoitory.
### Running the Software (Systemd)
Once software and systemd has been installed using ``sudo./install.sh``, you can run the program in two ways:\
``sudo ./runner.sh``\
Or on boot using the systemctl service or\
``systemctl start player.service``
### Running the Software (Flask Server)
Run both the flask server and client in two ways:\
``sudo ./start_server.sh``\
<img src="https://github.com/Navelwriter/ECE434-Music/assets/77686570/ae75ac10-8dcd-4c5c-a981-7ff00c84ffd0" width="60%" height="60%"> 

Or run it manually by: \
On one shell window run ``sudo ./player_server.py`` and wait for the server to load.\
Opening another window, run ``sudo ./player_client.py`` 
### Connect to flask server webpage
After the server is started, connect to the server using the link http://192.168.7.2:8081/
![image](https://github.com/Navelwriter/ECE434-Music/assets/77686570/d4737866-6cd7-4cda-9b0d-2c815cc4d4c0)







