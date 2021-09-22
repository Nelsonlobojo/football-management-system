from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_mysqldb import MySQL
import MySQLdb.cursors
import secrets
from functools import wraps
 
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = secrets.token_bytes(16)


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
            session['role'] = account['role']
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
            flash('User updated Successfully')
            return redirect(url_for('profile'))
        return render_template('profile.html',account=account)
    return redirect(url_for('login'))

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['role']== "admin":
            return f(*args, **kwargs)
        else:
            abort(401)
    return wrap

#Add personnel via utilization of session objects
@app.route('/login/addpersonnel', methods=['GET', 'POST'])
@admin_required
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
            flash('Coach added Successfully')
            return redirect(url_for('userlist'))
        return render_template('personnel.html')

    return redirect(url_for('login'))

#Get list of the various users and their information

@app.route('/login/addpersonnel/list', methods=['GET', 'POST'])
@admin_required
def userlist():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Users')
        data = cur.fetchall()
        cur.close()
        return render_template('coach.html', coach = data)
    return redirect(url_for('login'))


#Delete various users and their information
@app.route('/delete/<string:id>', methods = ['POST','GET'])
@admin_required
def delete_user(id):
  if 'loggedin' in session:  
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Users WHERE user_id = %s', (id,))
    mysql.connection.commit()
    cur.close
    flash('Coach Removed Successfully')
    return redirect(url_for('userlist'))
  return redirect(url_for('login'))


#Add users of the various athletes and their information
@app.route('/login/addpersonnel/athletes', methods=['GET', 'POST'])
@admin_required
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
            flash('Athlete added Successfully')
            return redirect(url_for('list'))
        return render_template('personnel.html')

    return redirect(url_for('login'))

#Get list of the various athletes and their information
@app.route('/login/addpersonnel/athletes/list', methods=['GET', 'POST'])
@admin_required
def list():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Athlete')
        data = cur.fetchall()
        cur.close()
        return render_template('athlete.html', athlete = data)
    return redirect(url_for('login'))

#Edit list of the various athletes and their information
@app.route('/edit/<id>', methods = ['POST', 'GET'])
@admin_required
def get_athlete(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
  
        cur.execute('SELECT * FROM Athlete WHERE athlete_id = %s', (id,))
        data = cur.fetchall()
        cur.close()
        print(data[0])
        return render_template('edit.html', athlete = data[0])
    return redirect(url_for('login'))
 
@app.route('/update/<id>', methods=['POST'])
@admin_required
def update_athlete(id):
    if 'loggedin' in session:
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
    return redirect(url_for('login'))

    
 #Delete various athletes and their information
@app.route('/delete/<string:id>', methods = ['POST','GET'])
@admin_required
def delete_athlete(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM Athlete WHERE athlete_id = %s', (id,))
        mysql.connection.commit()
        cur.close
        flash('Athlete Removed Successfully')
        return redirect(url_for('list'))
    return redirect(url_for('login'))
    
        
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
            flash('Unit added Successfully')
            cur.close
            return redirect(url_for('unitlist'))
        return render_template('units.html',usersList=usersList,athleteList=athleteList,unitList=unitList)

     return redirect(url_for('login'))


#Get list of the various units
@app.route('/login/unit/list', methods=['GET', 'POST'])
def unitlist():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Unit.user_id, Unit.unit_id,Unit.unit_name, Users.coach_name from Unit JOIN Users ON Unit.user_id=Users.user_id;")
        data = cursor.fetchall()
        cursor.close()
        return render_template('unitlist.html', unit = data)
    return redirect(url_for('login'))

 
#Delete various athletes and their information
@app.route('/login/unit/list/delete/<string:id>', methods = ['POST','GET'])
def delete_unit(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Unit WHERE unit_id = %s', (id,))
        mysql.connection.commit()
        cursor.close
        flash('Unit Removed Successfully')
        return redirect(url_for('unitlist'))
    return redirect(url_for('login'))



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
            flash('Athlete added to unit successfully')
            return redirect(url_for('playerlist'))
        return render_template('units.html')

     return redirect(url_for('login'))

#Delete Players from the Units
@app.route('/login/unit/player/list', methods=['GET', 'POST'])
def playerlist():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Unit.unit_id, Unit.unit_name, UnitMembers.member_id, UnitMembers.athlete_id, Athlete.athlete_name from Unit JOIN UnitMembers ON Unit.unit_id=UnitMembers.unit_id JOIN Athlete ON UnitMembers.athlete_id=Athlete.athlete_id ;")
        data = cursor.fetchall()
        cursor.close()
        return render_template('playerlist.html', player = data)
    return redirect(url_for('login'))

@app.route('/login/unit/player/list/delete/<string:id>', methods = ['POST','GET'])
def delete_player(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM UnitMembers WHERE member_id = %s', (id,))
        mysql.connection.commit()
        cursor.close
        flash('Player Removed Successfully')
        return redirect(url_for('playerlist'))
    return redirect(url_for('login'))

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
            cur.execute("INSERT INTO Drill(drill_id,drill_name,category_id,description,requirements,video) VALUES(%s,%s,%s,%s,%s,%s)",
            (drill_id,drill_name,drill_category,drill_description,drill_requirement,drill_video))
            mysql.connection.commit()
            flash('Drill added Successfully')
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
            session_date = sessiondetails['session_date']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Session(duration,session_name,session_id,user_id,session_date) VALUES(%s,%s,%s,%s,%s)",(duration,sessionname,sessionid,coach_name,session_date))
            mysql.connection.commit()
            cur.close
            flash('Session added Successfully')
            return redirect(url_for('sessionlist'))
        return render_template('session.html',usersList=usersList, unitList=unitList, sessionList=sessionList,drillList=drillList)
    return redirect(url_for('login'))


# Session list
@app.route('/login/session/list', methods=['GET', 'POST'])
def sessionlist():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Session.session_id, Session.session_name, Session.duration, Users.coach_name from Session JOIN Users ON Session.user_id=Users.user_id;")
        data = cursor.fetchall()
        cursor.close()
        return render_template('sessionlist.html', session = data)
    return redirect(url_for('login'))

# Edit and update Session
@app.route('/login/session/list/edit/<id>', methods = ['POST', 'GET'])
def get_session(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Session WHERE session_id = %s', (id,))
        data = cur.fetchall()
        cur.close()
        print(data[0])
        return render_template('editsessions.html', session = data[0])
    return redirect(url_for('login'))
 
@app.route('/login/session/list/update/<id>', methods=['POST'])
def update_session(id):
    if 'loggedin' in session:
        if request.method == 'POST':
            sessiondetails= request.form
            sessionname= sessiondetails['sessionname']
            duration = sessiondetails['duration']
            session_date = sessiondetails['session_date']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Session SET duration = %s,session_name = %s, session_date=%s WHERE session_id = %s", (duration, sessionname,session_date, id))
            flash('Session Updated Successfully')
            mysql.connection.commit()
            cur.close
            return redirect(url_for('sessionlist'))
    return redirect(url_for('login'))

    
 #Delete sessions and their information
@app.route('/login/session/list/delete/<string:id>', methods = ['POST','GET'])
def delete_session(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM Session WHERE session_id = %s', (id,))
        mysql.connection.commit()
        cur.close
        flash('Session Removed Successfully')
        return redirect(url_for('sessionlist'))
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
            flash('Elements added Successfully')
            return redirect(url_for('sessionlist'))
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
            purpose = request.form['purpose']
            if purpose == 'P':
                session_list = request.form['session']
                athlete_id = request.form['athlete']
                acccelerate = request.form['acceleration']
                agility = request.form['agility']
                balance = request.form['balance']
                jumping = request.form['jumping']
                fitness = request.form['fitness']
                pace = request.form['pace']
                stamina = request.form['stamina']
                strength = request.form['strength']
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO Physical(athlete_id,session_id,acceleration,agility,balance,jumping,natural_fitness,pace,stamina,strength) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (athlete_id,session_list,acccelerate,agility,balance,jumping,fitness,pace,stamina,strength))
                mysql.connection.commit()
                flash('Data added Successfully')
                cur.close
                return redirect(url_for('addtrainingdata'))
            elif purpose == 'T':
                session_list = request.form['session']
                athlete_id = request.form['athlete']
                corners = request.form['corner']
                crossing = request.form['crossing']
                dribbling = request.form['dribbling']
                finishing = request.form['finishing']
                firsttouch = request.form['firsttouch']
                freekicks = request.form['freekicks']
                heading = request.form['heading']
                longshots = request.form['longshots']
                longthrows = request.form['longthrows']
                marking = request.form['marking']
                passing = request.form['passing']
                penalty = request.form['penalty']
                tackling = request.form['tackling']
                technique = request.form['technique']
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO Technical(athlete_id,session_id,corners,crossing,dribbling,finishing,first_touch,free_kicks,heading,long_shots,long_throws,marking,passing,penalty,tackling,technique) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (athlete_id,session_list,corners,crossing,dribbling,finishing,firsttouch,freekicks,heading,longshots,longthrows,marking,passing,penalty,tackling,technique))
                mysql.connection.commit()
                flash('Data added Successfully')
                cur.close
                return redirect(url_for('addtrainingdata'))
            elif purpose == 'M':
                session_list = request.form['session']
                athlete_id = request.form['athlete']
                aggression = request.form['aggression']
                anticipation = request.form['anticipation']
                bravery = request.form['bravery']
                composure = request.form['composure']
                concentration = request.form['concentration']
                creativity = request.form['creativity']
                decisions = request.form['decisions']
                determination = request.form['determination']
                flair = request.form['flair']
                influence = request.form['influence']
                offtheball = request.form['offtheball']
                positioning = request.form['positioning']
                teamwork = request.form['teamwork']
                workrate = request.form['workrate']
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO Mental(athlete_id,session_id,aggression,anticipation,bravery,composure,concentration,creativity,decisions,determination,flair,influence,off_the_ball,positioning,teamwork,work_rate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (athlete_id,session_list,aggression,anticipation,bravery,composure,concentration,creativity,decisions,determination,flair,influence,offtheball,positioning,teamwork,workrate))
                mysql.connection.commit()
                flash('Data added Successfully')
                cur.close
                return redirect(url_for('addtrainingdata'))

        return render_template('trainingdata.html', sessionList=sessionList,athleteList=athleteList)
    return redirect(url_for('login'))

@app.route('/login/collection', methods=['GET', 'POST'])
def collection():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Drill")
        data = cursor.fetchall()
        cursor.close()
        return render_template('drilllist.html', drill = data) 
    return redirect(url_for('login'))       

@app.route('/login/collection/view/<id>', methods=['GET', 'POST'])
def viewcollection(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor() 
        cur.execute('SELECT * FROM Drill WHERE drill_id = %s', (id,))
        data = cur.fetchall()
        cur.close()
        print(data[0])
        return render_template('viewdrill.html', drill = data)  
    return redirect(url_for('login'))         

@app.route('/login/collection/edit/<id>', methods = ['POST', 'GET'])
def edit_drill(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Drill WHERE drill_id = %s', (id,))
        data = cur.fetchall()
        cur.close()
        print(data[0])
        return render_template('editdrills.html', drill = data[0])
    return redirect(url_for('login'))     

@app.route('/login/collection/update/<id>', methods=['POST'])
def update_drill(id):
    if 'loggedin' in session:
     if request.method == 'POST':
        drilldetails = request.form
        drill_description = drilldetails['description']
        drill_requirement = drilldetails['requirements']
        drill_video = drilldetails['video']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Drill SET description = %s,requirements = %s,video = %s  WHERE drill_id = %s", (drill_description,drill_requirement,drill_video, id))
        flash('Drill Updated Successfully')
        mysql.connection.commit()
        cur.close
        return redirect(url_for('collection'))
    return redirect(url_for('login'))

@app.route('/login/collection/delete/<string:id>', methods = ['POST','GET'])
def delete_drill(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM Drill WHERE drill_id = %s', (id,))
        mysql.connection.commit()
        cur.close
        flash('Drill Removed Successfully')
        return redirect(url_for('collection'))
    return redirect(url_for('login'))

@app.route('/login/calendar', methods=['GET', 'POST'])
def calendar():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Session")
        calendar = cur.fetchall()  
        return render_template('calendar.html', calendar = calendar)


@app.route('/login/reports')
def reports():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Athlete')
        data = cur.fetchall()
        cur.close()
        return render_template('report.html', report = data)
    return redirect(url_for('login'))  

@app.route('/login/reports/view/<id>', methods=['GET', 'POST'])
def viewreports(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor() 
        cursor = mysql.connection.cursor()
        cursor1= mysql.connection.cursor()
        cur.execute('SELECT athlete_id,session_id,corners,crossing,dribbling,finishing,first_touch,free_kicks,heading,long_shots,long_throws,marking,passing,penalty,tackling,technique FROM Technical WHERE athlete_id = %s', (id,))
        cursor.execute('SELECT athlete_id,session_id,acceleration,agility,balance,jumping,natural_fitness,pace,stamina,strength FROM Physical WHERE athlete_id=%s', (id,))
        cursor1.execute('SELECT athlete_id,session_id,aggression,anticipation,bravery,composure,concentration,creativity,decisions,determination,flair,influence,off_the_ball,positioning,teamwork,work_rate FROM Mental WHERE athlete_id=%s', (id,))
        data = cur.fetchall()
        data1= cursor.fetchall()
        data2= cursor1.fetchall()
        cur.close()
        print(data[0])
        return render_template('reports.html', technical = data, physical=data1, mental=data2)  
    return redirect(url_for('login'))           

   
if __name__ == '__main__':
    app.run(debug = True)

