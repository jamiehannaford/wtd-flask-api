import sqlite3
from flask import Flask, jsonify, g, request

# config
DATABASE = '/tmp/cats.db'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

@app.route('/cats')
def show_cats():
  cur = g.db.execute('select * from cats order by id desc')
  entries = [dict(name=row[0], breed=row[1], colour=row[2], tail_length=row[3]) for row in cur.fetchall()]
  return jsonify({"cats":entries}) 

@app.route('/cats', methods=['POST'])
def add_cat():
  json = request.get_json()
  g.db.execute('insert into cats(name, breed, colour, tail_length) values (?, ?, ?, ?)',
    [json['name'], json['breed'], json['colour'], json['tail_length']])
  g.db.commit()
  return jsonify({"status":201})

if __name__ == '__main__':
  app.run()
