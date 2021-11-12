from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from intWeb.auth.models import User
from intWeb.blog.models import Post
from intWeb.hello.models import Todo
from intWeb.esasset.models import Acc,Item,ItemType
from intWeb.lessons.models import Lesson
from datetime import datetime
#datetime.strptime(start, '%Y-%m-%d')

builtin_list = list

def initdb_data(db,app):
    print("do it")
    db.drop_all()
    db.create_all()
    admin = User("admin","123","admin","1")
    mbc_admin = User("mbc","abcd1234","admin","1")
    studa = User("stu","123","stu","8","SC1A","01")
    studb = User("sta","123","stu","8","SC2A","01")
    acc=Acc(acno=0, acc="學校資產", orderNo="None", regSDate=datetime.now(),voucherNo="None",vendor="None",createdById=1)
    db.session.add(admin)
    db.session.add(mbc_admin)
    db.session.add(studa)
    db.session.add(studb)
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

AccTable=[
    Acc(acno='2002427110', acc='電腦熒幕, Reborn Card,CDRW,電腦主機, ', orderNo='2427110', regSDate=datetime.strptime('2002-10-24', '%Y-%m-%d'), voucherNo='8P10-10',vendor='CTM',createdById=1),
    Acc(acno='2002427111', acc='電腦主機', orderNo='2427111', regSDate=datetime.strptime('2002-10-24', '%Y-%m-%d'), voucherNo='8P10-21',vendor='易通電腦公司',createdById=1)
    ]