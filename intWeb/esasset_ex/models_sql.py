# Copyright 2015 Google Inc.
from datetime import datetime
from flask import Flask
from flask import current_app
from flask import g
import sqlite3

builtin_list = list

#def make_dicts(cursor, row):
#    return dict((cursor.description[idx][0], value)
#                for idx, value in enumerate(row))
#    #db.row_factory = make_dicts

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_db():
    DATABASE=current_app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///","")
    db = getattr(g, '_sqlite_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory=sqlite3.Row
    return db

#@app.teardown_appcontext
#    def close_connection(exception):
#        db = getattr(g, '_sqlite_database', None)
#        if db is not None:
#            db.close()
#            print("close sqlite3")

def ReadAccs():
    conn=get_db()
    items=conn.execute('SELECT * FROM Acc ;').fetchall()
    conn.close()
    return items


def ReadItems():
    conn=get_db()
    items=conn.execute('SELECT * FROM ITEM ;').fetchall()
    conn.close()
    return items

def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

def main():
    """
    If this script is run directly, create all the tables necessary to run the application.
    (env) C:\code\EsAsset>python intWeb\esasset_ex\models_sql.py 
    """
    app = Flask(__name__)
    app.config.from_pyfile('../../config.py')
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            #db.cursor().executescript(f.read())
            print(f.read())
        db.commit()

        for user in query_db('select * from user'):
            print( user['user'], 'has the id', user['id'])

        the_username="admin"
        user = query_db('select * from user where user = ?', [the_username], one=True)
        if user is None:
            print('No such user')
        else:
            print(the_username, 'has the id', user['id'] ) 

        db.close()      

    print("end.")

if __name__ == '__main__':
    main()

