import sys
import io
from flask import Flask, render_template, request, redirect, url_for
import pymysql
from pymysql.err import MySQLError

# Fix Unicode printing on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)

def create_connection():
    try:
        connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',  # leave blank — default for XAMPP
    database='bus_ticket_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

        print("Database Connected Successfully")
        return connection
    except pymysql.MySQLError as e:
        print(f"[ERROR] Error while connecting to DB: {e}")
        return None



@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return redirect(url_for('login_page'))
    
    conn = create_connection()
    if conn is None:
        return "Database Connection Failed!", 500

    cursor = conn.cursor()

    # Get form data
    id = request.form.get('id')
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    alt_phone = request.form.get('altPhone')
    password = request.form.get('password')

    # Validate form data
    if not all([id, username, email, phone, alt_phone, password]):
        return "All fields are required!"

    try:
        sql = """
        INSERT INTO login (id, username, email, phone, alt_Phone, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (id, username, email, phone, alt_phone, password)
        cursor.execute(sql, values)
        conn.commit()
        print("Data inserted successfully!")
    except MySQLError as e:
        print(f"Error inserting data: {e}")
        return f"Database Error: {e}"
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('home'))


@app.route('/home')
def home():
    return "<h1>Welcome to EasyCommute Home Page!</h1>"


if __name__ == '__main__':
    app.run(debug=True)
