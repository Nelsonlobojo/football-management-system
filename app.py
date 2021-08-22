from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'bacon'


# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'teams'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/')
def landing():
    return render_template("landingpage.html")
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    #Output message if something goes wrong...
    msg= ''

        # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
            # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            # Redirect to home page
            return redirect(url_for('profile'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)
        
# logout page
@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   
   # Redirect to login page
   return redirect(url_for('login'))
#this will be the home page, only accessible for loggedin users

@app.route('/login/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page

       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('SELECT * FROM Users WHERE id = %s', (session['id'],))
       account = cursor.fetchone()

        # Show the profile page with account info

       return render_template('profile.html', account=account)
# User is not loggedin redirect to login page

    return redirect(url_for('login'))

#Add personnel via utilization of session objects
@app.route('/login/addpersonnel', methods=['GET', 'POST'])
def addpersonnel():
    if request.method == 'POST':
        #Print the form data to the console
        for key, value in request.form.items():
            print(f'{key}: {value}')
        #Save the form data to the session object
        session['coach_id']=request.form['coach_id']
        session['coach_name']=request.form['coach_name']
        session['phone_number']=request.form['phone_number']

    return render_template('addpersonnel.html')
@app.route('/login/addpersonnel/coach')
def list_coach():
    return render_template('coach.html')
    
        
#Unit page
@app.route('/login/unit')
def unit():
  return render_template("units.html")

if __name__ == '__main__':
    app.run(debug = True)
