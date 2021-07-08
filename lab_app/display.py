import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import Adafruit_DHT
import time
import csv
import sys
csvfile = "/var/www/lab_app/static/temp.csv"

#####Einstellungen
server_name = "Crypto_Miner"
#Wie oft wird das Programm gestartet?
messung = 5 #in Minuten
#Wie viele Tage sollen gespeichert werden?
tage = 14
while True:

	#Der Sensor wird ausgelesen
	humidity, temperature = Adafruit_DHT.read_retry(11, 17)
	max_werte = ((tage * 1440) / messung) + 1 #Tage werden in Minuten umgerechnet und max_werte wird ermittelt
	print('maximale Anzahl von Werten: ' + str(max_werte))
	temp_int = int(temperature)
	hum_int = int(humidity)
	#Wenn mehr als 37°C herrschen, wird eine Mail versendet
	if temp_int > 37:
		import smtplib
		from email.mime.multipart import MIMEMultipart
		from email.mime.text import MIMEText

		senderEmail = "transmitter@email"
		empfangsEmail = "receiver@email"
		msg = MIMEMultipart()
		msg['From'] = senderEmail
		msg['To'] = empfangsEmail
		msg['Subject'] = "Temperaturwarnung"

		emailText = "Der Serverschrank " + str(server_name) + " hat eine Temperatur von " + str(temp_int) + "°C und ist damit zu heiß!"
		msg.attach(MIMEText(emailText, 'html'))

		server = smtplib.SMTP('your.smtp.server', 587) # Die Server Daten
		server.starttls()
		server.login(senderEmail, "email.password") # Das Passwort
		text = msg.as_string()
		server.sendmail(senderEmail, empfangsEmail, text)
		server.quit()

	#Anzahl der Messwerte in Datenbank werden gezaehlt
	lines_t = sum(1 for line in open('/var/www/lab_app/static/temp.csv', 'r'))
	print('Aktuelle Anzahl von Messwerten: ' + str(lines_t))

	#Wenn die Maximale Anzahl überschritten wurde, wird der älteste Wert gelöscht
	if int(lines_t) > max_werte:
		f = open('/var/www/lab_app/static/temp.csv','r')
		lines = f.readlines()
		f.close()
		del lines[1]
		f = open('/var/www/lab_app/static/temp.csv','w')
		for l in lines:
			f.write(l)
		f.close()

	#Die aktuellen Messwerte werden in der Console ausgegeben
	if humidity is not None and temperature is not None:
		print('Temperature = ' + str(temperature) + '°C  Humidity = ' + str(humidity) + '%')
	else:
		print('can not connect to the sensor!')

	#Die Temperatur wird mit Zeitstempel abgespeichert in einer csv
	timeC = time.strftime("%H:%M:%S")
	data = [temperature, timeC]
	with open(csvfile, "a")as output:
		writer = csv.writer(output, delimiter=",", lineterminator = '\n')
		writer.writerow(data)

	#Die Messwerte werden geplottet
	df = pd.read_csv('http://localhost:8080/static/temp.csv')
	fig = go.Figure(go.Scatter(x = df['Zeit_x'], y = df['Temperatur_y'],
		name='Temperatur in °C'))

	fig.update_layout(title='Temperatur nach Zeit',
		plot_bgcolor='rgb(230, 230,230)',
		showlegend=True)

	fig.write_html("/var/www/lab_app/templates/historic.html")

	#Die Schleife wird beendet
	sleeptime = messung * 60
	time.sleep(sleeptime)