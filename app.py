from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

UPLOAD_FOLDER = 'static/uploads/'
 
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
            session['id'] = account['user_id']
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


#this will be the home page, only accessible for loggedin users and are able to edit their information

@app.route('/login/profile' ,methods=['POST','GET'])
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE user_id = %s', (session['id'],))
        account = cursor.fetchone()
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email    = request.form['email']
            coachname = request.form['coach-name']
            phonenumber = request.form['phone-number']
            cur = mysql.connection.cursor()
            cur.execute("Update Users SET phone_number=%s,coach_name=%s,username=%s,email=%s,password=%s WHERE user_id=%s",(phonenumber,coachname,username,email,password,session['id']))
            mysql.connection.commit()
            cur.close
            return redirect(url_for('profile'))
        return render_template('profile.html',account=account)
    return redirect(url_for('login'))

#Add personnel via utilization of session objects
@app.route('/login/addpersonnel', methods=['GET', 'POST'])
def addpersonnel():
    if 'loggedin' in session:
        if request.method == 'POST':
            playerdetails = request.form
            coachid = playerdetails['coachid']
            username = request.form['username']
            password = request.form['password']
            email    = request.form['email']
            coach_name = playerdetails['name']
            coach_number = playerdetails['phone_number']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Users(user_id,phone_number,coach_name,username,email,password) VALUES(%s,%s,%s,%s,%s,%s)",(coachid,coach_number,coach_name,username,email,password))
            mysql.connection.commit()
            cur.close
            return redirect(url_for('userlist'))
        return render_template('personnel.html')

    return redirect(url_for('login'))

#Get list of the various users and their information

@app.route('/login/addpersonnel/list', methods=['GET', 'POST'])
def userlist():
    cur = mysql.connection.cursor()
 
    cur.execute('SELECT * FROM Users')
    data = cur.fetchall()
  
    cur.close()
    return render_template('coach.html', coach = data)


#Delete various users and their information
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_user(id):
    
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Users WHERE user_id = %s', (id,))
    mysql.connection.commit()
    cur.close
    flash('Coach Removed Successfully')
    return redirect(url_for('userlist'))


#Add users of the various athletes and their information
@app.route('/login/addpersonnel/athletes', methods=['GET', 'POST'])
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
            cur.execute("INSERT INTO Athlete(athlete_id,phone_number,date_of_birth,position,preferred_foot,athlete_name) VALUES(%s,%s,%s,%s,%s,%s)",(athleteid,athlete_phone_number,date_birth,position,pref_foot,athlete_name))
            mysql.connection.commit()
            cur.close
            return redirect(url_for('list'))
        return render_template('personnel.html')

    return redirect(url_for('login'))

#Get list of the various athletes and their information
@app.route('/login/addpersonnel/athletes/list', methods=['GET', 'POST'])
def list():
    cur = mysql.connection.cursor()
 
    cur.execute('SELECT * FROM Athlete')
    data = cur.fetchall()
  
    cur.close()
    return render_template('athlete.html', athlete = data)


#Edit list of the various athletes and their information
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_athlete(id):

    cur = mysql.connection.cursor()
  
    cur.execute('SELECT * FROM Athlete WHERE athlete_id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', athlete = data[0])
 
@app.route('/update/<id>', methods=['POST'])
def update_athlete(id):
    if request.method == 'POST':
        playerdetails = request.form
        athlete_name = playerdetails['athlete_name']
        athlete_phone_number = playerdetails['athlete_phone_number']
        date_birth = playerdetails['date_birth']
        position = playerdetails['position']
        pref_foot = playerdetails['pref_foot']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Athlete SET athlete_name = %s, date_of_birth = %s,phone_number = %s, preferred_foot= %s, position = %s WHERE athlete_id = %s", (athlete_name, date_birth, athlete_phone_number,position,pref_foot, id))
        flash('Athlete Updated Successfully')
        mysql.connection.commit()
        cur.close
        return redirect(url_for('list'))

    
 #Delete various athletes and their information
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_athlete(id):
    
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Athlete WHERE athlete_id = %s', (id,))
    mysql.connection.commit()
    cur.close
    flash('Athlete Removed Successfully')
    return redirect(url_for('list'))
    
        
#Unit page
@app.route('/login/unit', methods=['GET', 'POST'])
def unit():
     if 'loggedin' in session:
        cur = mysql.connection.cursor()
        coach = mysql.connection.cursor()
        coach.execute('SELECT * FROM Users')
        usersList = coach.fetchall()
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
            cur.execute("INSERT INTO Unit(unit_name,unit_id,user_id) VALUES(%s,%s,%s)",(unit_name,unit_number,coach_id))
            mysql.connection.commit()
            cur.close
            return redirect(url_for('unitlist'))
        return render_template('units.html',usersList=usersList,athleteList=athleteList,unitList=unitList)

     return redirect(url_for('login'))


#Get list of the various units
@app.route('/login/unit/list', methods=['GET', 'POST'])
def unitlist():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT Unit.user_id, Unit.unit_id,Unit.unit_name, Users.coach_name from Unit JOIN Users ON Unit.user_id=Users.user_id;")
    data = cursor.fetchall()
    cursor.close()
    return render_template('unitlist.html', unit = data)

 
#Delete various athletes and their information
@app.route('/login/unit/list/delete/<string:id>', methods = ['POST','GET'])
def delete_unit(id):
    
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM Unit WHERE unit_id = %s', (id,))
    mysql.connection.commit()
    cursor.close
    flash('Unit Removed Successfully')
    return redirect(url_for('unitlist'))



#Add Players to the Units

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
            return redirect(url_for('playerlist'))
        return render_template('units.html')

     return redirect(url_for('login'))

#Delete Players from the Units
@app.route('/login/unit/player/list', methods=['GET', 'POST'])
def playerlist():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT Unit.unit_id, Unit.unit_name, UnitMembers.member_id, UnitMembers.athlete_id, Athlete.athlete_name from Unit JOIN UnitMembers ON Unit.unit_id=UnitMembers.unit_id JOIN Athlete ON UnitMembers.athlete_id=Athlete.athlete_id ;")
    data = cursor.fetchall()
    cursor.close()
    return render_template('playerlist.html', player = data)

@app.route('/login/unit/player/list/delete/<string:id>', methods = ['POST','GET'])
def delete_player(id):
    
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM UnitMembers WHERE member_id = %s', (id,))
    mysql.connection.commit()
    cursor.close
    flash('Player Removed Successfully')
    return redirect(url_for('playerlist'))

#Drills page
@app.route('/login/drills', methods=['GET', 'POST'])
def drills():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT video FROM Drill')
        video = cur.fetchall()
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Category')
        categoryList = cursor.fetchall()
        if request.method == 'POST':
            drilldetails = request.form
            drill_id = drilldetails['drillid']
            drill_name = drilldetails['drill_name']
            drill_category = drilldetails['category']
            drill_description = drilldetails['description']
            drill_requirement = drilldetails['requirements']
            drill_video = drilldetails['video']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Drill(drill_id,category_id,description,requirements,video,drill_name) VALUES(%s,%s,%s,%s,%s,%s)",
            (drill_id,drill_category,drill_description,drill_requirement,drill_video,drill_name))
            mysql.connection.commit()
            cur.close
            return redirect(url_for('drills'))
        return render_template('drills.html' ,video=video, categoryList=categoryList)
    return redirect(url_for('login'))

#Session page
@app.route('/login/session', methods=['GET', 'POST'])
def addsession():
    if 'loggedin' in session:
        coach = mysql.connection.cursor()
        cur = mysql.connection.cursor()
        ses = mysql.connection.cursor()
        dr = mysql.connection.cursor()
        coach.execute('SELECT * FROM Users')
        cur.execute('SELECT * FROM Unit')
        ses.execute('SELECT * FROM Session')
        dr.execute('SELECT * FROM Drill')
        usersList = coach.fetchall()
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
            cur.execute("INSERT INTO Session(session_id,duration,user_id,session_name) VALUES(%s,%s,%s,%s)",(sessionid,duration,coach_name,sessionname))
            mysql.connection.commit()
            cur.close
            return 'success'
        return render_template('session.html',usersList=usersList, unitList=unitList, sessionList=sessionList,drillList=drillList)
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

@app.route('/login/addtrainingdata', methods=['GET', 'POST'])
def addtrainingdata():
    if 'loggedin' in session:
        ses = mysql.connection.cursor()
        ses.execute('SELECT * FROM Session')
        sessionList = ses.fetchall()
        play = mysql.connection.cursor()
        play.execute('SELECT * FROM Athlete')
        athleteList = play.fetchall()
        if request.method == 'POST':
            
            cur = mysql.connection.cursor()
            cur.execute()
            mysql.connection.commit()
            cur.close
            return 'success'
        return render_template('trainingdata.html', sessionList=sessionList,athleteList=athleteList)
    return redirect(url_for('login'))


            
                      

   
if __name__ == '__main__':
    app.run(debug = True)

