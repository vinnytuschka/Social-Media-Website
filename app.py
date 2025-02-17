from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from pymongo import MongoClient
import bcrypt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# MongoDB Connection
client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
db = client['social_media_db']
users_collection = db['users']
posts_collection = db['posts']

@app.route('/')
def home():
    # Fetch latest posts
    posts = list(posts_collection.find().sort('timestamp', -1).limit(10))
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        if users_collection.find_one({'username': username}):
            return 'Username already exists', 400
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        users_collection.insert_one({
            'username': username,
            'password': hash_password
        })
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = users_collection.find_one({'username': username})
        if user and bcrypt.checkpw(password, user['password']):
            session['username'] = username
            return redirect(url_for('home'))
        return 'Invalid username or password', 400
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/post', methods=['POST'])
def create_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    content = request.form['content']
    post = {
        'username': session['username'],
        'content': content,
        'timestamp': datetime.utcnow()
    }
    posts_collection.insert_one(post)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)