from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",        # your XAMPP phpMyAdmin username
    password="",        # your password (default is empty for XAMPP)
    database="bus_booking_system"
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('bus.html')

@app.route('/submit_journey', methods=['POST'])
def submit_journey():
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        travel_date = request.form['travel_date']
        passengers = request.form['passengers']

        sql = "INSERT INTO journeys (source, destination, travel_date, passengers) VALUES (%s, %s, %s, %s)"
        val = (source, destination, travel_date, passengers)
        cursor.execute(sql, val)
        db.commit()

        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
