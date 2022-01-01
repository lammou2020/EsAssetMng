from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from intWeb.auth.models import User
from intWeb.blog.models import Post
from intWeb.hello.models import Todo
from intWeb.esasset.models import Acc,Item
from intWeb.lessons.models import Lesson
from datetime import datetime
#datetime.strptime(start, '%Y-%m-%d')

builtin_list = list

def initdb_data(db,app):
    print("do it")
    db.drop_all()
    db.create_all()
    Users_def=[
        User("admin","123","admin","1"),
        User("mbc","123","admin","1"),
        User("fin","123","admin","1"),
        User("fin1","123","admin","1"),
        User("ict","123","admin","1"),
        User("ga","123","admin","1"),
    ]
    for u_ in Users_def:
        db.session.add(u_)
        
    acc=Acc(acno="FA0000-TMP-000-000", acc="學校資產",  regSDate=datetime.now(),createdById=1)
    db.session.add(acc)
    for acc_ in AccTable:
        db.session.add(acc_)
    db.session.commit()

def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

AccTable=[    ]
