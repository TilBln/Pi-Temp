from flask import Flask, request, render_template
import time

app = Flask(__name__)
app.debug = True  # Make this False if you are no longer debugging

@app.route("/")
def lab_temp():
        import sys
        import random
        import Adafruit_DHT
        humidity, temperature = Adafruit_DHT.read_retry(11, 17)
        if humidity is not None and temperature is not None:
                return render_template("lab_temp.html",temp=temperature,hum=humidity)
        else:
                return render_template("no_sensor.html")

@app.route("/historic")
def historic():
	if 1 == 1:
		return render_template("historic.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

