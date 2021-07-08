# RaspberryPi-DHT
A simple way to display current and historic temperature using Python and a DHT11 sensor

## Credits: 

https://github.com/cwalk/Pi-Temp
- IMPORTANT: major parts of the code are 100% written by cwalk and not by me, I just renewed the existing project after 6 years of no updates; some files aren't used any more but inside the code - they will stay until the w.i.p. is done.

## How to install:

1) Connect the DHT Sensor with your Raspberry (-> Circuit.png) 
2) Install current Raspbian OS and activate SSH 
3) Connect to the Pi via local network
4) Commands:
- sudo apt-get update -y
- sudo apt-get upgrade -y

- sudo apt-get install nginx -y
- sudo apt-get install screen -y
- sudo apt-get install python3-pip -y
- sudo pip3 install flask uwsgi
- sudo apt-get install python3-pandas -y
- sudo pip3 install adafruit_dht
- sudo pip3 install plotly
- cd /var/www/
- sudo wget https://github.com/TilBln/RaspberryPi-DHT/raw/main/TemperaturMessung.zip
- sudo su
- unzip TemperaturMessung.zip
- rm TemperaturMessung.zip
- cd lab_app
5) Add cronjobs:
- crontab -e
- 1
- add following lines:
- @reboot python3 /var/www/lab_app/lab_app.py 
- @reboot python3 /var/www/lab_app/display.py 
6) Reboot the RaspberryPi
sudo reboot now

## Circuit:
![Circuit Diagram](/circuit.png?raw=true "Circuit Diagram")
