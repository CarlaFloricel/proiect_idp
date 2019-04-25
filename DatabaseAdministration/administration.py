from typing import List, Dict
from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import json
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

config = {
    'user': 'root',
    'password': 'root',
    'host': 'database',
    'port': '3306',
    'database': 'timetable'
}

@app.route('/', endpoint='chooseActionEndpoint')
@basic_auth.required
def chooseActionForm():
    auth = request.authorization
    return redirect(url_for('addMovieEndpoint'))

@app.route('/', methods=['POST'])
def chooseAction():
    return redirect(url_for('addMovieEndpoint'))


@app.route('/addMovie', endpoint='addMovieEndpoint')
@basic_auth.required
def addFlightForm():
    return render_template('addMovieForm.html')

@app.route('/addMovie', methods=['POST'])
def addFlight():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    text = "CREATE TABLE IF NOT EXISTS movies (movieId VARCHAR(20), name VARCHAR(50), displayDay INT, displayHour INT);"
    cursor.execute(text)
    cursor.execute("COMMIT")
    text = "CREATE TABLE IF NOT EXISTS seats (movieId VARCHAR(20), numberOfSeats INT, reservedSeats INT, boughtSeats INT);"
    cursor.execute(text)
    cursor.execute("COMMIT")
    text = "INSERT INTO movies (movieId, name, displayDay, displayHour) "
    text += " VALUES (\'"
    text += request.form['movieId'] + "\', \'"  + request.form['name'] + "\',"
    text += request.form['displayDay']  + ", " + request.form['displayHour']
    text += ")"
    cursor.execute(text)
    cursor.execute("COMMIT")
    text = "INSERT INTO seats (movieId, numberOfSeats, reservedSeats, boughtSeats) VALUES (\'"
    text += request.form['movieId'] + "\', " + request.form['numberOfSeats'] + ", 0, 0)"
    cursor.execute(text)
    cursor.execute("COMMIT")
    cursor.close()
    connection.close()
    return redirect(url_for('chooseActionEndpoint'))

@app.route('/print/<table>')
def printAll(table):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table)
    results = [var for var in cursor]
    cursor.close()
    connection.close()
    return str(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
