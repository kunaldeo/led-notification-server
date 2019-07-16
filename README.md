# Introduction

Welcome to the alpha release of **LED Notification Server**. This software allows you to show notifications on LED matrix panels.

*Pull Requests welcome*

**Current Features**

* Display Android notifications
* Display Plex On Screen Display on playback
   * Movie Information including Director, Rating and File format
   * TV information like season, episode name etc. 
* Output resolution of 128x128 using 4 64x64 Matrix panel

**Planned Features**

* Support for iOS Notifications
* Dynamic rendering for other resolutions: **Help Needed**
* Support for higher resolutions

## How it Looks

![Display1](https://user-images.githubusercontent.com/441799/56405728-3c1cb000-628b-11e9-8c13-3e4582dc306c.jpg) ![notification2](https://user-images.githubusercontent.com/441799/56506761-13234600-653d-11e9-9382-eee23bbc630e.jpg)

## Hardware Requirements

*If you do not want to buy the hardware you can also use TERMINAL output of noisebridge server* 

*4 64x64 LED module is not mandatory, it is just that I have designed the output to 128x128, one can easily add support for smaller resolutions as well with just one or two panels*

* **64x64 P3 or P2.5 LED Matrix Display Module** 4 Pieces. Can be purchased from [AliExpress](https://www.aliexpress.com/wholesale?&SearchText=P3+64x64+led+matrix), [Adafruit](https://www.adafruit.com/product/3649), [Sparkfun](https://www.sparkfun.com/products/14824)

* **5v Power Supply for LED Display Matrix, 20 Amps is recommended** [AliExpress](https://www.aliexpress.com/wholesale?&SearchText=5v+20a+power+supply)

* **Raspberry Pi 3 Model B+**, other Pi Models may work as well, [Official Page](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)

## Software Requirements

*This is just for reference. Installation steps will cover the installation of most of the components*

* **Python 3**
* **Noisebridge Flaschen Taschen Project** [Github](https://github.com/hzeller/flaschen-taschen)
* **Raspbian Stretch Lite** [Download Page](https://downloads.raspberrypi.org/raspbian_lite_latest)
* **pnmscale** fron [Netpbm](http://netpbm.sourceforge.net)
* **Kodi Notify Android App** [Playstore](https://play.google.com/store/apps/details?id=de.linuxwhatelse.android.notify) for Android Notifications
* **Plex Server** with Plex Pass(Webhook Support) for Plex Notfications [Plex](https://www.plex.tv), [Webhook Support](https://support.plex.tv/articles/115002267687-webhooks/)

```
If you are not using Plex you can ignore all plex related instructions
```

## Architecture Diagram
![LED Matrix Notification Center](https://user-images.githubusercontent.com/441799/56405556-63bf4880-628a-11e9-9a9c-124974801782.png)

1. Plex Server or Android device push payload to Webhook Server on LED Matrix Notfication Server
2. LED Matrix Notification Server parses the notification, generates an image and push it to Noisbridge LED Display Server via UDP
3. Noisebirdge Server pushes the image to LED Matrix Display which is connected to the GPIO of rasperry pi

## Installation Steps

### Setting Up Noisebridge LED Display Server on PI

#### A. Wiring the LED Matrix

1. Wire the first LED Panel using the instructions at [rpi-rgb-led-matrix Github project](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/wiring.md#wiring-diagram). Follow the instruction for 64x64 panel.
2. Chain the other three LED Panels using the following pattern

   ```
   // can be arranged in this U-shape
   //    [<][<] }----- Raspberry Pi connector
   //    [>][>]
   ```
   
![matrix1](https://user-images.githubusercontent.com/441799/56466132-111c9280-642a-11e9-9ad5-88bb75c97058.jpg)

![matrix2](https://user-images.githubusercontent.com/441799/56466134-1679dd00-642a-11e9-9ae5-560363394aa2.jpg)
   
#### B. Setting up Noisebridge LED DIsplay Server
*Following instructions/commands are for Rasperry PI*

1. Install Raspian Lite, [Instructables Guide](https://www.instructables.com/id/Install-and-Setup-Raspbian-Lite-on-Raspberry-Pi-3/)
2. Install development tools on the PI

    ```
    sudo apt-get install build-essential

    ```
3. Checkout Noisebridge Server (FlaschenTaschen)

    ```bash
    $ git clone --recursive https://github.com/hzeller/flaschen-taschen.git
    $ cd flaschen-taschen
    ```
4. Compile the server

    ```
	$ cd server
	$ make FT_BACKEND=rgb-matrix
	```
5. Create ```/etc/systemd/system/led.service``` with the following contents

    ```
    [Unit]
    Description=Led Service

    [Service]
    User=root
    Group=root
    Restart=always
    RestartSec=30
    ExecStart=/home/pi/flaschen-taschen/server/ft-server --led-rows=64 --led-cols=64 --led-chain=4 --led-pixel-mapper="U-mapper" --led-slowdown-gpio=2 --led-brightness=25

    [Install]
    WantedBy=multi-user.target
    ```
*Verify all the paths*
6. Enable and start the service

    ```
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable led
    $ sudo systemctl start led
    ```
7. Notedown the IP address of the PI.

### C. Setting up LED Notification Server

1. Clone this repository

    ```
    $ git clone https://github.com/kunaldeo/led-notification-server
    ```

2. Create a python virtualenv and install the dependencies

   ```
   $ sudo python3 -m pip install virtualenv # Optional step, if you have virtualenv skip it
   $ cd led-notification-server
   $ python3 -m virtualenv -p /usr/bin/python3 venv
   $ source venv/bin/activate
   $ pip install -r requirements.txt
   ```
3. Edit the values for the following variables in `plexobject/settings.py`. Mandatory items are **bold**.
    
    * **`ALLOWED_HOSTS`**: *Set it to the IP address where the repo has been cloned*
    * `ICON_CACHE_DIR`: *Path where the notification icons will be cached*
    * **`PLEX_TOKEN`** = *Plex auth token. See [Finding Plex authentication token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/).*
    * `PLEX_OUTPUT_IMAGE_PATH` = *Generated image location for Plex notification*
    * `PLEX_OUTPUT_SCRIPT_PATH` = *Script responsible for pushing plex image*
    * `SCREEN_CLEAR_COMMAND` = *Command for clearing the screen*
    * `IMAGE_BACKGROUND` = *Backgorund of the notfication image*
    * `FONT_NAME` = *Font path*
    * `FONT_SIZE` = *Font size*
    * `NOTIFICATION_OUTPUT_IMAGE_PATH` = *Android notification image path*
    * `NOTIFICATION_OUTPUT_SCRIPT_PATH` = *Script responsible for pushing Andorid notfication image*

4. Edit the run scripts
    * For Plex Notifcations, edit `PLEX_OUTPUT_SCRIPT_PATH` file. Substitute the values under < >.
    
    ```
    #!/bin/bash
    cat <PLEX_OUTPUT_IMAGE_PATH> | stdbuf -o64k pnmscale -xysize 128 128 | socat -b64000 STDIO UDP-SENDTO:<Pi IP Address>:1337
    echo "Image Displayed.."
    ```
    
    * For Android Notifcations, edit `NOTIFICATION_OUTPUT_SCRIPT_PATH ` file. Substitute the values under < >.
    
    ```
    #!/bin/bash
    cat <NOTIFICATION_OUTPUT_IMAGE_PATH> | stdbuf -o64k pnmscale -xysize 128 128 | socat -b64000 STDIO UDP-SENDTO:<Pi IP Address>:1337
    echo "Image Displayed.."
    ```

5. Run the server. Note the IP address of the server.
   
   ```
   $ screen -S notification
   $ python manage.py runserver 0.0.0.0:8000
   ```
   
### D. Configuring Android Notifications

1. Open notfiy app
2. Go to Devices section and click `+`>`Add Manually`. Fill in the IP address and the port(8000).
3. In the main screen select the apps from which you want the notifications to be sent

![notifyapp](https://user-images.githubusercontent.com/441799/56465854-f5fb5400-6424-11e9-9dda-a83601bfb504.jpg)

### E. Configuring Plex Server

1. Open to Plex Server
2. Go to `Settings`>`Webhooks`>`Add Webhook`
3. Enter the server address in the following format

```
http://192.168.1.4:8000/khook/
```
![plexwebhook](https://user-images.githubusercontent.com/441799/56466048-c1899700-6428-11e9-8499-c25f2bf4e191.jpg)
