from __future__ import print_function
from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

from copy import deepcopy
import json
from typing import List, Dict
import sys


app = Flask(__name__)

# Configuraions for connecting to database
config = {
    'user': 'root',
    'password': 'root',
    'host': 'database',
    'port': '3306',
    'database': 'timetable'
}

@app.route('/')
def chooseActionForm():
    return redirect(url_for('reserveEndpoint'))

@app.route('/showReservation')
def addReservationForm():
    return render_template('showReservationForm.html')


@app.route('/showReservation', methods=['POST'])
def showReservation():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT movieId, numberOfSeats FROM reservedSeats WHERE reservationId = " + request.form['reservationId'] + ";")
    #cursor.execute("COMMIT")
    results = [var for var in cursor]
    sys.stderr.write(str(results) + '\n')
    return 'MOVIE ID: ' + str(results[0][0]) + ' NUMBER OF SEATS: ' + str(results[0][1]) + ' for your reservation.'


@app.route('/reserveMovie', endpoint='reserveEndpoint')
def reserveMovieForm():
    return render_template('reserveMovieForm.html')



@app.route('/reserveMovie', methods=['POST'])
def reserveMovie():
    global reservId
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    #cursor.execute("DROP TABLE reservedSeats")
    #cursor.execute("COMMIT")
    #return 

    text = "CREATE TABLE IF NOT EXISTS reservedSeats (reservationId INT NOT NULL AUTO_INCREMENT, movieId VARCHAR(20), numberOfSeats INT);"
    cursor.execute(text)
    cursor.execute("COMMIT")

    cursor.execute("SELECT numberOfSeats FROM movies WHERE movieId = " + request.form['movieId'] + ";")
    results = [var for var in cursor]
    seats_left = results[0][0] - int(request.form['nrOfSeats'])
    sys.stderr.write(str(seats_left) + '\n')
    if results[0][0] >= int(request.form['nrOfSeats']):

        text = "UPDATE movies SET numberOfSeats = " + str(seats_left) +  " WHERE movieId = " + request.form['movieId'] + ";"
        sys.stderr.write(text + '\n')
        cursor.execute(text)
        cursor.execute("COMMIT")


        text = "SELECT MAX(reservationId) FROM reservedSeats"
        sys.stderr.write(text + '\n')
        cursor.execute(text)
        results = [var for var in cursor]


        sys.stderr.write(str(results))
        if results[0][0] == None:
            id_res = 0
        else:
            id_res = int(results[0][0]) + 1



        text = "INSERT INTO reservedSeats (reservationId, movieId, numberOfSeats)"
        text += " VALUES (" + str(id_res) + ","
        text += "\'"
        text += request.form['movieId'] + "\',"
        text += request.form['nrOfSeats']
        text += ")"
        sys.stderr.write(text + '\n')
        cursor.execute(text)
        cursor.execute("COMMIT")
    else:
        return "Sorry, not enough seats available"


    cursor.close()
    connection.close()  
    return str(id_res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
