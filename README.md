# AutoDoggoMonitoro3000
Senior Capstone Project for an IoT device


# Steps Taken on Raspberry Pi

## Schematic

Here is the overall schematic for our system (v0.1)
![alt_text](https://user-images.githubusercontent.com/47087525/100073859-41dd5e80-2dfb-11eb-9189-17576a0fa752.png)

* **NOTE**: The TXD and RXD pins on GPS module were interchanged. Thus, for the GPS to be connected to the correct pins on the PI, they had to be flipped.

## Setting up Raspberry Pi Zero

* The specific Raspberry Pi Zero being used can be found for sale here: https://rb.gy/mcofca

* Raspbian Jesse was used on our Pi, and can be downloaded here: http://downloads.raspberrypi.org/raspbian/images/raspbian-2020-02-14/2020-02-13-raspbian-buster.zip

Now, do `sudo apt-get update` to update the OS's dependencies. Then do `sudo reboot`

For easy access to the Pi, ssh is also setup. In order to setup ssh, complete the following:

* `sudo raspi-config`

* Select *Interfacing Options* 

![alt text](https://phoenixnap.com/kb/wp-content/uploads/2020/01/raspi-config-interfacing-options.png)

* Select *SSH* and select <Yes> on the “Would you like the SSH server to be enabled?” prompt.
  
![alt_text](https://phoenixnap.com/kb/wp-content/uploads/2020/01/raspi-config-ssh.png)


* **NOTE**: In order to enable I2C for I2C enabled devices, follow the same steps, but select *I2C* instead of *SSH*.


Now the Raspberry Pi should be able to accept ssh connections. In order to enable SSH, follow these steps:
* `sudo systemctl enable ssh`
* `sudo systemctl start ssh`


Dependency Installation:

```
sudo apt-get install clang

sudo pip install gps
sudo pip3 install gps
```
##Anti-bark Module
First, connect the audio breakout board, speaker, and microphone as indicated in the schematic

Secondly, we need to edit some config files in the pi before it is able to output audio through the speaker
using your favorite editor open the file /boot/config.txt
`sudo vim /boot/config/txt`
edit/add the following lines
`#dtparam=audio=on
dtoverlay=hifiberry-dac
dtoverlay=i2s-mmap`

Next, we want to add a new file /etc/asound.conf

`sudo vim /etc/asound.conf`
and we want to add the following lines:

`pcm.hifiberry {
type hw card 0
}

pcm.!default {
type plug
slave.pcm "dmixer"
}

pcm.dmixer {
type dmix
ipc_key 1024
slave{
pcm "hifiberry"
channels 2
}
}`
## GPS Module

**Prerequisites**

* First, update the Raspberry Pi's kernel by using `rpi-update`
  This process may take up to 30 minutes
* Now, type in `sudo reboot` to reboot the Raspberri Pi

Next, we will install some dependencies to be able to interact with the GPS module:
* `sudo apt-get install gpsd`
* `sudo apt-get install gpsd-clients`

Then, we need to enable the serial ports on the Raspberry Pi. With the GPS module plugged in, execute the following command:

`sudo raspi-config`

![alt text](https://maker.pro/storage/6tMJPDg/6tMJPDg1MG3tNSvbXQCItSYAZObuUtuqohDisW2t.png)

Select *Interfacing Options*, then *Serial*
* Choose 'No' for the first prompt, and 'Yes' for the second prompt. Your window should look like the following after everything is setup successfully:

![alt_text](https://maker.pro/storage/G2g9fjl/G2g9fjlbcKjQNlGecFn1yekjWx3B3f791dMzyMjY.png)

Select *Finish*, then type in `sudo reboot` to reboot the Raspberry Pi.

**Interfacing with GPS Module**

Now we can begin interfacing with the GPS Module, and viewing the data it is recieving. Since we are using a Raspberry Pi Zero W, we will be interfacing with the `/dev/ttyS0`. Other articles mention using `/dev/ttyAMA0`, however this is only on Raspberry Pi's 1 & 2.

* To test that the GPS is outputting data, execute the following command: `cat /dev/serial0`
* Now that we've confirmed that the GPS is outputting correctly, we need to stop the GPSD service to clear its default settings: `sudo systemctl disable gpsd.socket`

*Please NOTE: The following command MUST be executed everytime the Raspberry Pi is restarted*
* Start a new GPSD instance redirecting to our desired serial port: `sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock`


Now the GPS Module should be outputting its data to the Pi. In order to view the data, execute this command:
* `sudo gpsmon /dev/ttyS0`
-----------------------------------------------------------------------------

## Accelerometer Module

**Prerequisites**

* First, we need to install the GPIO control module for the Raspberry Pi using the command `pip3 install RPi.GPIO`
* Then, we install the mpu6050 module for accessing the digital accelerometer and gyroscope on a Raspberry Pi with `pip3 install mpu6050-raspberrypi`

With this, the dependencies have been installed.

Check all connections are in place. After running the `pedometer/step_counter.py`, we get the current temperature and steps taken as output. 


## Bluetooth Interfacing with Raspberry Pi (Scrapped)

**Prerequisites**

```
sudo apt-get update
sudo apt-get upgrade
```
* After updating, we will need to download a couple Bluetooth Packages:

`sudo apt-get install bluetooth blueman bluez`

* Now, reboot the Pi with `sudo reboot`

We'll need the Python Library for Bluetooth communication to allow us to send and recieve data

`sudo apt-get install python-bluetooth`

and we also need the GPIO Library:

`sudo apt-get install python-rpi.gpio`

## RethinkDB Database Setup

* Rather than relying on a bluetooth connection to interact with the Raspberry Pi using the Android App, the Raspberry Pi will instead send information to a database that the app can then access.

* Source: https://rethinkdb.com/docs/install/raspbian/


# Prerequisite (Raspberry Pi Zero)

* Since the Raspberry Pi Zero has very limited memory, we need to setup a 1GB SWAP partition for the compilation of RethinkDB to work properly (source: https://nebl.io/neblio-university/enabling-increasing-raspberry-pi-swap/).

```
sudo dphys-swapfile swapoff

sudo nano /etc/dphys-swapfile
    #modify the variable CONF_SWAPSIZE to 1024:
    CONF_SWAPSIZE=1024

sudo dphys-swapfile setup

sudo dphys-swapfile swapon

sudo reboot
```

# Installing RethinkDB

* For RethinkDB, a secondary Raspberry Pi is setup to be used as the 'server' that stores the information, while the Rasberry Pi Zero with the modules connected to it will act like the 'client' that is sending the data out.

* The following steps were used on BOTH Raspberry Pi's.

```
sudo apt-get install g++ protobuf-compiler libprotobuf-dev libboost-dev curl m4 wget clang

#At this point make sure you check to see that 2.0.4 is still the most recent version of RethinkDB! http://rethinkdb.com

wget https://download.rethinkdb.com/repository/raw/dist/rethinkdb-2.4.1.tgz
tar xf rethinkdb-latest.tgz
rm rethinkdb-latest.tgz
cd rethinkdb-*
./configure --with-system-malloc --allow-fetch 
make

#Export the proper C++ flags for Raspberry Pi 1/2

export CXXFLAGS="-mfpu=neon-vfpv4 -mcpu=native -march=native -mfloat-abi=hard" | make -j3 ALLOW_WARNINGS=1
sudo make install
```

* Now that RethinkDB is installed, we need to ensure that RethinkDB starts correctly when using it.

* In order to do this, `sudo nano /etc/rc.local` and modify it to look like the following:
```
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

rethinkdb --bind all --server-name rbpi_rethinkdb -d /home/pi --daemon

exit 0
```

* Now, to start the 'server' Raspberry Pi, please enter the following command:
`rethinkdb --bind all`
