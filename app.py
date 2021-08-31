from flask import Flask, render_template, request, redirect, url_for, session, flash, \
    send_from_directory
from PIL import Image
import PIL
import glob
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename 
import os
import MySQLdb.cursors

UPLOAD_FOLDER = 'static/uploads/'
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
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

@app.route('/login/profile', methods=['POST'])
def upload_files():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('profile.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
    
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


#Add personnel via utilization of session objects
@app.route('/login/addpersonnel', methods=['GET', 'POST'])
def addpersonnel():
    if 'loggedin' in session:
        if request.method == 'POST':
            playerdetails = request.form
            coachid = playerdetails['coachid']
            coach_name = playerdetails['name']
            coach_number = playerdetails['phone_number']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Coach(coach_id,coach_name,phone_number) VALUES(%s,%s,%s)",(coachid,coach_name,coach_number))
            mysql.connection.commit()
            cur.close
            return 'success'
        return render_template('personnel.html')

    return redirect(url_for('login'))

        

    

@app.route('/login/addpersonnel/player', methods=['GET', 'POST'])
def addplayer():
    if 'loggedin' in session:
        if request.method == 'POST':
            playerdetails = request.form
            athleteid = playerdetails['athleteid']
            athlete_name = playerdetails['athlete_name']
            athlete_phone_number = playerdetails['athlete_phone_number']
            date_birth = playerdetails['date_birth']
            position = playerdetails['position']
            pref_foot = playerdetails['pref_foot']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Athlete(athlete_id,athlete_name,date_of_birth,position,preferred_foot,phone_number) VALUES(%s,%s,%s,%s,%s,%s)",(athleteid,athlete_name,date_birth,position,pref_foot,athlete_phone_number))
            mysql.connection.commit()
            cur.close
            return 'success'
        return render_template('personnel.html')

    return redirect(url_for('login'))
    
        
#Unit page
@app.route('/login/unit', methods=['GET', 'POST'])
def unit():
   
     if 'loggedin' in session:
        cur = mysql.connection.cursor()
        coach = mysql.connection.cursor()
        coach.execute('SELECT * FROM Coach')
        coachList = coach.fetchall()
        cur = mysql.connection.cursor()
        play = mysql.connection.cursor()
        cur.execute('SELECT * FROM Unit')
        play.execute('SELECT * FROM Athlete')
        athleteList = play.fetchall()
        unitList = cur.fetchall() 
        if request.method == 'POST':
            unitdetails = request.form
            unit_name = unitdetails['unit_name']
            unit_number = unitdetails['id']
            coach_id = unitdetails['coach_name']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Unit(unit_id,unit_name,coach_id) VALUES(%s,%s,%s)",(unit_number,unit_name,coach_id))
            mysql.connection.commit()
            cur.close
            return 'success'
        return render_template('units.html',coachList=coachList,athleteList=athleteList,unitList=unitList)

     return redirect(url_for('login'))


#Add Players

@app.route('/login/unit/player', methods=['GET', 'POST'])
def addplayertounit():
   
     if 'loggedin' in session:
        if request.method == 'POST':
            unit_list = request.form['unit']
            athlete = request.form['athlete']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO UnitMembers(athlete_id,unit_id) VALUES(%s,%s)", (athlete,unit_list))
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
        coach = mysql.connection.cursor()
        cur = mysql.connection.cursor()
        ses = mysql.connection.cursor()
        dr = mysql.connection.cursor()
        coach.execute('SELECT * FROM Coach')
        cur.execute('SELECT * FROM Unit')
        ses.execute('SELECT * FROM Session')
        dr.execute('SELECT * FROM Drill')
        coachList = coach.fetchall()
        unitList = cur.fetchall()
        sessionList = ses.fetchall()
        drillList = dr.fetchall() 
        if request.method == 'POST':
            sessiondetails= request.form
            sessionid= sessiondetails['sessionid']
            sessionname= sessiondetails['sessionname']
            duration = sessiondetails['duration']
            coach_name = sessiondetails['coach_name']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Session(session_id,duration,coach_id,session_name) VALUES(%s,%s,%s,%s)",(sessionid,duration,coach_name,sessionname))
            mysql.connection.commit()
            cur.close
            return 'success'
        return render_template('session.html',coachList=coachList, unitList=unitList, sessionList=sessionList,drillList=drillList)
    return redirect(url_for('login'))

#Session Window
@app.route('/login/session/elements', methods=['GET', 'POST'])
def addelement():
    if 'loggedin' in session:

        if request.method == 'POST':
            
            cur = mysql.connection.cursor()
            cur.execute()
            mysql.connection.commit()
            cur.close
            return 'success'
        return render_template('session.html')
    return redirect(url_for('login'))



  
                      

   
if __name__ == '__main__':
    app.run(debug = True)
