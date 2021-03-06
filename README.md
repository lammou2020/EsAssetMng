# EsAsset

##
python main.py --help

init db   
python main.py --initdb   

run    
python main.py   

## ER

![](img/acc.png)


## SQL

```sql
CREATE TABLE IF NOT EXISTS User (
        id INTEGER NOT NULL,
        user VARCHAR(255) NOT NULL,
        password VARCHAR(225) NOT NULL,
        Name VARCHAR(255),
        Classno VARCHAR(255),
        Seat VARCHAR(255),
        Role VARCHAR(255),
        PRIMARY KEY (id),
        UNIQUE (user)
);

CREATE TABLE IF NOT EXISTS Acc (
        id INTEGER NOT NULL,
        acno VARCHAR(16) NOT NULL,
        acc VARCHAR(160),
        regSDate DATETIME NOT NULL,
        describ TEXT,
        createdById VARCHAR(255),
        /*
        readonly INTEGER,
        Path VARCHAR(80),
        imageUrl VARCHAR(255),
        ctime DATETIME NOT NULL,
        utime DATETIME NOT NULL,
        total INTEGER,
        */
        PRIMARY KEY (id),
        UNIQUE (acno)
);

CREATE TABLE IF NOT EXISTS ItemCategory (
        id INTEGER NOT NULL,
        itemcat_pri BIGINT,
        itemcat_sec INTEGER,
        name VARCHAR(80),
        depr_year INTEGER,
        note1 TEXT,
        note2 TEXT,
        describ TEXT,
        PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Item (
        id INTEGER NOT NULL,
        itemno VARCHAR(30),
        itemcatno BIGINT,
        name VARCHAR(80),
        model VARCHAR(80),
        sn VARCHAR(80),
        price NUMERIC(10, 2),
        quantity INTEGER,
        amount NUMERIC(10, 2),
        fund_amount INTEGER,
        fund_name VARCHAR(80),
        keeper VARCHAR(80),
        place VARCHAR(80),
        depr_year INTEGER,
        warr_period NUMERIC(10, 2),
        note1 TEXT,
        note2 TEXT,
        regSDate DATETIME NOT NULL,
        acc_acno VARCHAR(16) NOT NULL,
        createdById VARCHAR(255),
        describ TEXT,
        /*
        Path VARCHAR(80),
        imageUrl VARCHAR(255),
        ctime DATETIME NOT NULL,
        utime DATETIME NOT NULL,
        adjust NUMERIC(10, 2),
        */
        PRIMARY KEY (id),
        UNIQUE (itemno),
        UNIQUE (itemcatno),
        FOREIGN KEY(acc_acno) REFERENCES Acc (acno)
);

CREATE TABLE IF NOT EXISTS ItemMoveLog (
        id INTEGER NOT NULL,
        itemno VARCHAR(30),
        keeper VARCHAR(80),
        place VARCHAR(80),
        createdById VARCHAR(255),
        ctime DATETIME NOT NULL,
        utime DATETIME,
        PRIMARY KEY (id),
        FOREIGN KEY(itemno) REFERENCES Item (itemno)
);
```

## ORM


config.py
```python
import os
PORT=85
# [START secret_key]
SECRET_KEY = 'keyboard_cat'
SESSION_COOKIE_NAME='connect.sid'
REDIS_PORT=6379
# [END secret_key]
DATA_BACKEND = 'sqlite'
SQLITE_PATH=f"{os.getcwd()}\\bookshelf.db"
SQLALCHEMY_SQLITE_URI = ( 'sqlite:///{path}').format(path=SQLITE_PATH)
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_SQLITE_URI
```

models.py    
```python
from datetime import datetime
from flask import Flask
from sqlalchemy.sql.elements import between
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

builtin_list = list

db = SQLAlchemy()

def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)

def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

# ?????????/???????????? ACC[FA2021-xxx-001/-00[1-9] ITEM[ACCNO]-[4271046][0001]
class Acc(db.Model):
    __tablename__ = 'Acc'
    id= db.Column(db.Integer,primary_key=True) # ??????
    acno = db.Column(db.String(16),unique=True,nullable=False)  #?????????/????????????
    acc= db.Column(db.String(160))  #??????
    regSDate= db.Column(db.DateTime, nullable=False,default=datetime.utcnow) #????????????
    describ=db.Column(db.Text)  # ??????
    # User info
    createdById = db.Column(db.String(255))    
    def __init__(self, acno=None, acc=None, regSDate=None, describ=None, createdById=None):
        self.acno=acno
        self.acc=acc
        self.regSDate=regSDate
        self.createdById=createdById
        self.describ=describ
    def __repr__(self):
        return "<acc(accno='%s', acc=%s)" % (self.accno, self.acc)    

# ?????? ITEM  [FA2021-xxx-001/-00[1-9]-[4271046][0001]
class Item(db.Model):
    __tablename__ = 'Item'    
    id = db.Column(db.Integer,primary_key=True) # ??????
    itemno=db.Column(db.String(30),unique=True,nullable=True)    # ????????????
    itemcatno=db.Column(db.BigInteger,unique=True,nullable=True) # ??????????????????
    name = db.Column(db.String(80))  # ??????
    model= db.Column(db.String(80))  # ??????
    sn = db.Column(db.String(80))    # SN/PN
    price = db.Column(db.Numeric(precision=10,scale=2))   # ??????
    quantity= db.Column(db.Integer,default=0)  # ??????
    amount=  db.Column(db.Numeric(precision=10,scale=2))  # ??????
    fund_amount=db.Column(db.Integer)  # ????????????
    fund_name=db.Column(db.String(80)) # ????????????/??????
    keeper=db.Column(db.String(80))  # ?????? link to _table
    place =db.Column(db.String(80))  # ????????????
    depr_year   = db.Column(db.Integer,default=0)  # 0505 rate:5/5 NN?????????/???????????????
    warr_period = db.Column(db.Numeric(precision=10,scale=2))  # ??????
    note1 =db.Column(db.Text)  # ?????????????????? ??????
    note2 =db.Column(db.Text)  # ??????????????????
    # Acc_acno
    regSDate = db.Column(db.DateTime, nullable=False,default=datetime.utcnow) 
    acc_acno = db.Column(db.String(16), db.ForeignKey('Acc.acno'), nullable=False)
    acc      = db.relationship('Acc',  backref=db.backref('Item', lazy=True))
    # User info
    createdById = db.Column(db.String(255))    
    describ = db.Column(db.Text)   

    def __init__(self, 
                 itemno=None,
                 itemcatno=None,
                 name=None,
                 model=None,
                 sn=None,
                 quantity=None,
                 price=None,
                 amount=None,
                 fund_amount=None,
                 fund_name=None,
                 place=None,
                 keeper=None,
                 depr_year=None,
                 note1=None,
                 note2=None,
                 acc_acno=None,
                 regSDate=None,
                 createdById=None,
                 describ=None,
                 ):
        self.itemno =itemno
        self.itemcatno =itemcatno
        self.name =name
        self.model =model
        self.sn =sn
        self.quantity =quantity
        self.price =price
        self.amount = amount
        self.depr_year=depr_year
        self.fund_amount = fund_amount
        self.fund_name = fund_name
        self.place=place
        self.keeper=keeper
        self.note1=note1
        self.note2=note2
        self.acc_acno=acc_acno
        self.regSDate=regSDate
        self.createdById=createdById
        self.describ=describ

    def __repr__(self):
        return "<item(name='%s')" % (self.name)    

# ???????????? ItemCategory [4271046][0001]
class ItemCategory(db.Model):
    __tablename__ = 'ItemCategory'    
    id = db.Column(db.Integer,primary_key=True)
    itemcat_pri=db.Column(db.BigInteger) # ??????????????????
    itemcat_sec=db.Column(db.Integer) # ??????????????????
    name = db.Column(db.String(80))  # ??????
    depr_year= db.Column(db.Integer)  # ????????????
    note1 =db.Column(db.Text)  # ?????????????????? ??????
    note2 =db.Column(db.Text)  # ?????????????????? ??????
    describ =db.Column(db.Text)  # ?????????????????? ??????
    def __init__(self, 
                 itemcat_pri=None,
                 itemcat_sec=None,
                 name=None,
                 depr_year=None,
                 note1=None,
                 note2=None,
                 describ=None
                 ):
        self.itemcat_pri =itemcat_pri
        self.itemcat_sec =itemcat_sec
        self.name =name
        self.depr_year =depr_year
        self.note1=note1
        self.note2=note2
        self.describ=describ

    def __repr__(self):
        return "<itemCate(name='%s')" % (self.name)    

# [ItemMoveLog]
class ItemMoveLog(db.Model):
    __tablename__ = 'ItemMoveLog'    
    id = db.Column(db.Integer,primary_key=True)
    itemno = db.Column(db.String(30), db.ForeignKey("Item.itemno"),nullable=True) # ????????????
    item = db.relationship('Item', backref="places",lazy=True) 
    keeper=db.Column(db.String(80))  # ?????? link to _table
    place =db.Column(db.String(80))  # ????????????
    createdById = db.Column(db.String(255))    
    ctime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  #????????????
    utime = db.Column(db.DateTime)  #????????????
    
    def __init__(self, 
                 itemno=None,
                 place=None,
                 keeper=None,
                 createdById=None
                 ):
        self.itemno =itemno
        self.place=place
        self.keeper=keeper
        self.createdById=createdById

    def __repr__(self):
        return "<ItemMoveLog(name='%s')" % (self.name)    

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../../config.py')
    init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        for i in range(700):
            u_= ItemCategory(
                 itemcat_pri='0',
                 itemcat_sec='0',
                 name="",
                 depr_year=0)
            db.session.add(u_)
        db.session.commit()
    print("All tables created")

if __name__ == '__main__':
    _create_database()
```

??????    
1.???????????? (?????????????????????, ??????????????????, ??????????????????/?????? )   
??????/?????? 
view
edit
list

2.??????????????????  

## ????????????
### ORM ?????????????????? 

#### query filter by date

from datetime import datetime
datetime.strptime(start, '%Y-%m-%d')
Idea.query.filter(Idea.time >= datetime.strptime(start, '%Y-%m-%d'),
                  Idea.time <= datetime.strptime(end, '%Y-%m-%d')).all()


#### 1 ????????????
?????????	MySQL??????	python??????	??????
SmallInteger	smallint	int	??????????????????????????????16???
Integer	int	int	?????????????????????32???
BigInteger	bigint	int/long	?????????????????????
Float	float	float	?????????
Numeric	decimal	decimal.Decimal	?????????
String	varchar	str	???????????????
Text(65536)	tinytext	str	??????????????????64K,2 16 ??? 1 2^{16}-12 16 ???1=65535bytes
Text(16777216)	mediumtext	str	??????????????????max16M,2 24 ??? 1 2^{24}-12 24 ???1=16777215bytes
Text(4294967295)	longtext	str	??????????????????max32M,2 32 ??? 1 2^{32}-12 32 ???1=4294967295bytes
LargeBinary	blob	str	??????????????????64K
LargeBinary(65536)	mediumblob	str	????????????max16M
LargeBinary(16777216)	longblob	str	????????????max32M
PickleType	blob	??????python??????	????????????Pickle??????????????????blob
Unicode	varchar	unicode	???????????????
UnicodeText	text	unicode	??????????????????64K
Boolean	tinyint	bool	?????????
Date	date	datetime.date	??????
Time	time	date.time	??????
DateTime	datetime	datetime.datetime	???????????????
Interval	datetime	datetime.timedelta	????????????
Enum	enum	str	???????????????

#### ?????????????????????
??????MySQL???
class Data(db.Model):
	__tablename__ = "datas"
	id = db.Column(db.Integer, primary_key=True)
	smallInteger = db.Column(db.SmallInteger)
	bigInteger = db.Column(db.BigInteger)
	floatData = db.Column(db.Float(10))
	numericData = db.Column(db.Numeric(10))
	stringData = db.Column(db.String(250))
	textData = db.Column(db.Text(200))
	mediumText = db.Column(db.Text(65536))
	longText = db.Column(db.Text(16777216))
	largeBinary = db.Column(db.LargeBinary(300))
	mediumBlob = db.Column(db.LargeBinary(65536))
	longBlob = db.Column(db.LargeBinary(16777216))
	pickle = db.Column(db.PickleType)
	mediumPickle = db.Column(db.PickleType(65536))
	longPickle = db.Column(db.PickleType(16777216))
	unicodeData = db.Column(db.Unicode(10))
	unicodeText = db.Column(db.UnicodeText)
	booleanData = db.Column(db.Boolean(0))
	dateData = db.Column(db.Date)
	timeData = db.Column(db.Time)
	dateTime = db.Column(db.DateTime)
	interval = db.Column(db.Interval)
	enumData = db.Column(db.Enum('father', 'mother'))
	def __repr__(self):
		return "Data {}".format(self.id)

MySQL?????????
+--------------+-------------------------+------+-----+---------+----------------+
| Field        | Type                    | Null | Key | Default | Extra          |
+--------------+-------------------------+------+-----+---------+----------------+
| id           | int(11)                 | NO   | PRI | NULL    | auto_increment |
| smallInteger | smallint(6)             | YES  |     | NULL    |                |
| bigInteger   | bigint(20)              | YES  |     | NULL    |                |
| floatData     |  float                   | YES  |     | NULL    |                |
| numericData  | decimal(10,0)           | YES  |     | NULL    |                |
| stringData   | varchar(250)            | YES  |     | NULL    |                |
| textData     | tinytext                | YES  |     | NULL    |                |
| mediumText   | mediumtext              | YES  |     | NULL    |                |
| longText     | longtext                | YES  |     | NULL    |                |
| largeBinary  | blob                    | YES  |     | NULL    |                |
| mediumBlob   | mediumblob              | YES  |     | NULL    |                |
| longBlob     | longblob                | YES  |     | NULL    |                |
| pickle       | blob                    | YES  |     | NULL    |                |
| mediumPickle | blob                    | YES  |     | NULL    |                |
| longPickle   | blob                    | YES  |     | NULL    |                |
| unicodeData  | varchar(10)             | YES  |     | NULL    |                |
| unicodeText  | text                    | YES  |     | NULL    |                |
| booleanData  | tinyint(1)              | YES  |     | NULL    |                |
| dateData     | date                    | YES  |     | NULL    |                |
| timeData     | time                    | YES  |     | NULL    |                |
| dateTime     | datetime                | YES  |     | NULL    |                |
| interval     | datetime                | YES  |     | NULL    |                |
| enumData     | enum('father','mother') | YES  |     | NULL    |                |
+--------------+-------------------------+------+-----+---------+----------------+


#### 3 Flask-MySQL?????????
??????	??????	?????????
primary_key	??????	True
unique	???????????????	True
index	??????	True
nullable	??????	True
default	?????????	null
????????????????????????????????????????????????
