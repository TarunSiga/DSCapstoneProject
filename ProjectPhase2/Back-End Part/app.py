from flask import Flask, session,render_template, request, redirect
import pyrebase

app = Flask(__name__)

config = {
    'apiKey': "AIzaSyDc6pG4ozv0J_Sbc9ELYSG13sTn4AYLQE4",
    'authDomain': "dscapstone-96cda.firebaseapp.com",
    'projectId': "dscapstone-96cda",
    'storageBucket': "dscapstone-96cda.appspot.com",
    'messagingSenderId': "682161845845",
    'appId': "1:682161845845:web:028a2e06fdadb6f88506dc",
    'measurementId': "G-CD6H1NV5LF",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

db = firebase.database()

app.secret_key = 'secret'

@app.route('/',methods=['POST','GET'])
def index():
    if('user' in session):
        return'Hi, {}'.format(session['user'])
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            session['user'] = email
        except:
            return 'Failed to login'
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
    
        user = auth.create_user_with_email_and_password(email, password)
            # Save additional user details in Firebase database
        db.child("users").child(user['localId']).set({"email": email})
        session['user'] = email
        print('Registered Successfully!')
        return 'Registered Successfully!'
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

if __name__ == '__main__':
    app.run(port=1111)