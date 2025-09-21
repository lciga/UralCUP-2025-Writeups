import os
import psycopg2
from psycopg2 import sql
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import DB_CONFIG
import re
import time


app = Flask(__name__)
app.secret_key = os.urandom(24)


def init_db():
            
    retries = 0
    while retries < 5:
        try:
            """Initialize the database with required tables"""
            conn = psycopg2.connect(
                dbname='postgres',
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port']
            )
            conn.autocommit = True
            cursor = conn.cursor()
                
            # Create database if it doesn't exist
            cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_CONFIG['dbname'],))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_CONFIG['dbname'])))
            
            cursor.close()
            conn.close()
                
            # Connect to our database and create tables
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
                
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_admin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create admin user if not exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = TRUE")
            if cursor.fetchone()[0] == 0:
                admin_password = generate_password_hash('my_beautiful_password_123123')
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash, is_admin) VALUES (%s, %s, %s, %s)",
                    ('admin', 'admin@pynotes.com', admin_password, True)
                )
                
            # Create notes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    title VARCHAR(200) NOT NULL,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Create admin user if not exists
            cursor.execute("SELECT COUNT(*) FROM notes WHERE user_id = 1")
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s)",
                    (1, "ВАЖНО!", "Админ попросил на время оставить пароль\nПароль: my_beautiful_password_123123\nУдалить после 17:00")
                )
                
            conn.commit()
            cursor.close()
            conn.close()
            break
        except:
            if retries < 5:
                time.sleep(1)
            else:
                raise Exception('fuck fuck database')


def get_db_connection():
    """Create and return a database connection"""
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, title, content, created_at FROM notes WHERE user_id = %s ORDER BY created_at DESC LIMIT 10",
        (session['user_id'],)
    )
    notes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', notes=notes, username=session['username'])

@app.route('/note/<int:note_id>')
def get_note(note_id: int):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, content, created_at, updated_at FROM notes WHERE id = %s ORDER BY created_at DESC",
        (note_id,)
    )

    note = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('note.html', note=note, username=session['username'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        password_hash = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash)
            )
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except psycopg2.IntegrityError:
            flash('Username or email already exists!', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, username, password_hash, is_admin FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = user[3]
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/create_note', methods=['GET', 'POST'])
def create_note():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s)",
            (session['user_id'], title, content)
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash('Note created successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('create_note.html')

@app.route('/admin')
def admin():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    user_filter = request.args.get('user_filter', 'all')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all users for the filter dropdown
    cursor.execute("SELECT id, username FROM users ORDER BY username")
    all_users = cursor.fetchall()

    # Base query for notes per user
    notes_query = '''
        SELECT u.id, u.username, COUNT(n.id) 
        FROM users u 
        LEFT JOIN notes n ON u.id = n.user_id 
    '''
    try:
        # Apply user filter if specified
        if user_filter != 'all':
            notes_query += f' WHERE u.id = {user_filter}'
        
        notes_query += ' GROUP BY u.id, u.username ORDER BY COUNT(n.id) DESC'
        
        if user_filter != 'all':
            cursor.execute(notes_query)
        else:
            cursor.execute(notes_query)
        
        notes_per_user = cursor.fetchall()
    
    except Exception as e:
        notes_per_user = [(-1, e, -1)]
        cursor.close()
        conn.close()
    
    conn = get_db_connection()
    cursor = conn.cursor()

    user_filter = re.sub("[^0-9]", "", user_filter)
    if user_filter == "":
        user_filter = "all"
    
    # Get total notes count (with filter if applied)
    total_notes_query = "SELECT COUNT(*) FROM notes"
    if user_filter != 'all':
        total_notes_query += " WHERE user_id = %s"
        cursor.execute(total_notes_query, (user_filter,))
    else:
        cursor.execute(total_notes_query)
    total_notes = cursor.fetchone()[0]
    
    # Get recent notes (last 7 days) with filter if applied
    recent_notes_query = '''
        SELECT COUNT(*) 
        FROM notes 
        WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
    '''
    if user_filter != 'all':
        recent_notes_query += " AND user_id = %s"
        cursor.execute(recent_notes_query, (user_filter,))
    else:
        cursor.execute(recent_notes_query)
    recent_notes = cursor.fetchone()[0]
    
    # Get average notes per user
    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM notes WHERE user_id IS NOT NULL")
    users_with_notes = cursor.fetchone()[0]
    avg_notes_per_user = total_notes / users_with_notes if users_with_notes > 0 else 0
    
    # Get most active user (most notes)
    cursor.execute('''
        SELECT u.username, COUNT(n.id) as note_count
        FROM users u 
        JOIN notes n ON u.id = n.user_id 
        GROUP BY u.id, u.username 
        ORDER BY note_count DESC 
        LIMIT 1
    ''')
    most_active_user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template(
        'admin.html',
        total_notes=total_notes,
        notes_per_user=notes_per_user,
        recent_notes=recent_notes,
        avg_notes_per_user=round(avg_notes_per_user, 1),
        most_active_user=most_active_user,
        all_users=all_users,
        selected_user=user_filter
    )

init_db()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
