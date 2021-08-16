from flask import Flask, render_template, request, redirect, url_for

#object relational mapper for python
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'

#initializing the db with app settings
db = SQLAlchemy(app)

#Create the db model
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
   
    def __repr__(self):
        return '<User %r>'% self.id

@app.route('/')
def landing():
    return render_template("landingpage.html")
    
@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == "POST":

        login = User(email= request.form['email'], password=request.form['password'])

        try:
            db.session.add(login)
            db.session.commit()
            return redirect('/')
        except:
            return "Invalid Credentials"
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.run(debug = True)
