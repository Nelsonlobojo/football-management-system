from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'bacon'


# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '#Billionare27'
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
    if 'loggedin' in session:
        if request.method == 'POST':
            playerdetails = request.form
            coach_name = playerdetails['name']
            coach_number = playerdetails['phone_number']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Coach(coach_name,phone_number) VALUES(%s,%s)",(coach_name,coach_number))
            mysql.connection.commit()
            cur.close
            return 'success'
        return render_template('personnel.html')

    return redirect(url_for('login'))

        

    

@app.route('/addpersonnel/coach')
def list_coach():
    return render_template('coach.html')
    
        
#Unit page
@app.route('/login/unit', methods=['GET', 'POST'])
def unit():
   
     if 'loggedin' in session:
        if request.method == 'POST':
            unitdetails = request.form
            unit_name = unitdetails['name']
            unit_number = unitdetails['id']
            athlete_choice = unitdetails['athlete']
            coach_name = unitdetails['name']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Unit(unit_id,unit_name,athlete_name,coach_name) VALUES(%s,%s)",(unit_number,unit_name,athlete_choice,coach_name))
            mysql.connection.commit()
            cur.close
            return 'success'
        return render_template('units.html')

     return redirect(url_for('login'))

#Drills page
@app.route('/login/drills', methods=['GET', 'POST'])
def drills():
    if 'loggedin' in session:
        if request.method == 'POST':
            drilldetails = request.form
            drill_name = drilldetails['name']
            drill_number = drilldetails['id']
            drill_category = drilldetails['category']
            drill_category_number = drilldetails['id']
            drill_description = drilldetails['description']
            drill_requirement = drilldetails['requirement']
            drill_image = drilldetails['image']
            drill_video = drilldetails['video']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO drill(drill_name,drill_id,category,description,requirements,image,video,category_id) VALUES(%s,%s)",(drill_name,drill_number,drill_category,drill_category_number,drill_description,drill_requirement,drill_image,drill_video))
            mysql.connection.commit()
            cur.close
            return 'success'
        return render_template('drills.html')
    return redirect(url_for('login'))

#Session page
@app.route('/login/session', methods=['GET', 'POST'])
def addsession():
    if 'loggedin' in session:
        if request.method == 'POST':
            sessiondetails = request.form
            session_number = sessiondetails['id']
            session_name = sessiondetails['name']
            session_coach_number = sessiondetails['id']
            session_coach_name = sessiondetails['name']
            session_duration = sessiondetails['duration']
            session_drill_number = sessiondetails['id']
            session_drill_name = sessiondetails['name']
            session_unit_number = sessiondetails['id']
            session_unit_name = sessiondetails['name']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Session(session_id,session_name,coach_id,coach_name,duration,drill_id,drill_name,unit_id,unit_name) VALUES(%s,%s)",(session_number,session_name,session_coach_number,session_coach_name,session_duration,session_drill_number,session_drill_name,session_unit_number,session_unit_name))
            mysql.connection.commit()
            cur.close
            return 'success'
        return render_template('session.html')
    return redirect(url_for('login'))

#Session Window


  
                      

   
if __name__ == '__main__':
    app.run(debug = True)
