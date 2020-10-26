# AutoDoggoMonitoro3000
Senior Capstone Project for an IoT device


# Steps Taken on Raspberry Pi

**Schematic**

Here is the overall schematic for our system (v0.1)
![alt_text](https://user-images.githubusercontent.com/44142909/96659591-2d89db80-12fc-11eb-9afc-ad92f7a492bc.png)

**Setting up Raspberry Pi Zero**

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


**GPS Module**

* First, update the Raspberry Pi's kernel by using `rpi-update`
  This process may take up to 30 minutes
* Now, type in `sudo reboot` to reboot the Raspberri Pi

Then, we need to enable the serial ports on the Raspberry Pi. With the GPS module plugged in, execute the following command:

`sudo raspi-config`

![alt text](https://maker.pro/storage/6tMJPDg/6tMJPDg1MG3tNSvbXQCItSYAZObuUtuqohDisW2t.png)

Select *Interfacing Options*, then *Serial*
* Choose 'No' for the first prompt, and 'Yes' for the second prompt. Your window should look like the following after everything is setup successfully:

![alt_text](https://maker.pro/storage/G2g9fjl/G2g9fjlbcKjQNlGecFn1yekjWx3B3f791dMzyMjY.png)

Select *Finish*, then type in `sudo reboot` to reboot the Raspberry Pi.
