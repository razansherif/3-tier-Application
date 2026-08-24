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
 password=os.environ['DB_PASSWORD']
 )
# ... standard Flask routes for GET/POST /todos ...
if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000)