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

In order to get the GPS module to connect to the Pi, run this instruction:
* `sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock`

Now the GPS Module should be outputting its data to the Pi. In order to view the data, execute this command:
* `sudo gpsmon /dev/ttyS0`

The output should resemble the following:
![alt_text](https://user-images.githubusercontent.com/44142909/98030107-c2e1a100-1dcd-11eb-898a-79c2dd4db52f.png)

## Accelerometer Module

**Prerequisites**

* First, we need to install the GPIO control module for the Raspberry Pi using the command `pip3 install RPi.GPIO`
* Then, we install the mpu6050 module for accessing the digital accelerometer and gyroscope on a Raspberry Pi with `pip3 install mpu6050-raspberrypi`

With this, the dependencies have been installed.

Check all connections are in place. After running the step_counter.py, we get the current temperature and steps taken as output. 
