import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
app = Flask(__name__)
CORS(app)
def get_db_connection():
 return psycopg2.connect(
 host=os.environ['DB_HOST'],
 database=os.environ['DB_NAME'],
 user=os.environ['DB_USER'],
 password=os.environ['DB_PASSWORD'],
 port=5432
 )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "Welcome to the Todo API Service"
    }), 200

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM todos;')
    todos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('INSERT INTO todos (title) VALUES (%s) RETURNING *;', (data['title'],))
    new_todo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_todo), 201

if __name__ == '__main__':
    try:
        init_db()
    except Exception as e:
        print(f"Database init warning: {e}")
    app.run(host='0.0.0.0', port=5000)
