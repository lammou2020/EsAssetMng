from datetime import datetime
from flask import Flask
from sqlalchemy.sql.elements import between
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

builtin_list = list

from intWeb import db

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

# 按項目/發票定義 ACC[FA2021-xxx-001/-00[1-9]  ITEM [ACCNO]-[4271046][0001]
class Acc(db.Model):
    __tablename__ = 'Acc'
    id= db.Column(db.Integer,primary_key=True)
    acno = db.Column(db.String(16),unique=True,nullable=False)  #按項目/發票定義 ACC[FA2021-xxx-001/-00[1-9]
    acc= db.Column(db.String(160))  #名稱
    regSDate= db.Column(db.DateTime, nullable=False,default=datetime.utcnow) #登記日期
    total=db.Column(db.Integer)  # 計算時使用 
    describe=db.Column(db.Text)  # 描述
    readonly=db.Column(db.Integer,default=0)
    createdById = db.Column(db.String(255))    
    Path=db.Column(db.String(80))
    imageUrl = db.Column(db.String(255))    
    ctime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  #创建时间
    utime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  #更新时间
    
    def __init__(self, acno=None, acc=None, regSDate=None, total=None,describe=None,createdById=None,imageUrl=None,Path=None):
        self.acno=acno
        self.acc=acc
        self.regSDate=regSDate
        self.createdById=createdById
        self.imageUrl=imageUrl
        self.total=total
        self.describe=describe
        self.Path=Path
    def __repr__(self):
        return "<acc(accno='%s', acc=%s)" % (self.accno, self.acc)    

# [ ACC crud]
def read(id):
    result = Acc.query.get(id)
    if not result:
        return None
    return from_sql(result)

def create(data):
    acc = Acc(**data)
    db.session.add(acc)
    db.session.commit()
    return from_sql(acc)

def update(data, id):
    acc = Acc.query.get(id)
    for k, v in data.items():
        setattr(acc, k, v)
    db.session.commit()
    return from_sql(acc)

def delete(id):
    Acc.query.filter_by(id=id).delete()
    db.session.commit()

# [START list_asc]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Acc.query
             #.filter_by(Open=1)
             .order_by(Acc.id)
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)

# [START list_desc]
def list_desc(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Acc.query
             #.filter_by(Open=1)
             .order_by(desc(Acc.id))
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)

# [START list_by_user]
def list_by_user(user_id, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Acc.query
             .filter_by(createdById=user_id)
             .order_by(Acc.id)
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)
# [END list_by_user]

# 物品 ITEM  [FA2021-xxx-001/-00[1-9]-[4271046][0001]
class Item(db.Model):
    __tablename__ = 'Item'    
    id = db.Column(db.Integer,primary_key=True)
    itemno=db.Column(db.String(30),unique=True,nullable=True) # 物品編號
    name = db.Column(db.String(80))  # 產品
    model= db.Column(db.String(80))  # 型號
    sn = db.Column(db.String(80))    # SN/PN
    price = db.Column(db.Integer)    # 單價
    quantity= db.Column(db.Integer)  # 數量
    adjust= db.Column(db.Integer)    # 攤折
    amount= db.Column(db.Integer)    # 淨值
    depr_ed= db.Column(db.Integer)   # 淨攤
    fund_amount=db.Column(db.Integer)# 資助金額
    fund_name=db.Column(db.String(80))  # 資助單位/個人
    keeper=db.Column(db.String(80))  # 移動 history
    place =db.Column(db.String(80))  # 地方
    note1 =db.Column(db.Text)  # 地方
    note2 =db.Column(db.Text)  # 資助
    # Acc_acno
    regSDate= db.Column(db.DateTime, nullable=False,default=datetime.utcnow) 
    acc_acno = db.Column(db.String(16), db.ForeignKey('Acc.acno'), nullable=False)
    acc = db.relationship('Acc',  backref=db.backref('Item', lazy=True))
    # User info
    createdById = db.Column(db.String(255))    
    Path=db.Column(db.String(80))
    imageUrl = db.Column(db.String(255))    
    ctime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  #创建时间
    utime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  #更新时间
    describe = db.Column(db.Text)    
    # Status
    #lebalmark= db.Column(db.String(80))   # 標籤
    #inventory= db.Column(db.String(80))   # 清查
    def __init__(self, 
                 itemno=None,
                 name=None,
                 model=None,
                 sn=None,
                 quantity=None,
                 price=None,
                 adjust=None,
                 amount=None,
                 depr_ed=None,
                 insure=None,
                 keeper=None,
                 note1=None,
                 note2=None,
                 acc_acno=None,
                 regSDate=None,
                 Path=None,
                 imageUrl=None,
                 createdById=None,
                 describe=None
                 ):
        self.itemno =itemno
        self.name =name
        self.model =model
        self.sn =sn
        self.quantity =quantity
        self.price =price
        self.adjust = adjust
        self.amount = amount
        self.adjust = adjust
        self.depr_ed = depr_ed
        self.insure=insure
        self.keeper=keeper
        self.note1=note1
        self.note2=note2
        self.acc_acno=acc_acno
        self.regSDate=regSDate
        self.Path=Path
        self.imageUrl=imageUrl
        self.createdById=createdById
        self.describe=describe

    def __repr__(self):
        return "<item(name='%s')" % (self.name)    

#[ ITEM CRUD]
def readItem(id):
    result = Item.query.get(id)
    if not result:
        return None
    return from_sql(result)

def createItem(data):
    acc = Item(**data)
    db.session.add(acc)
    db.session.commit()
    return from_sql(acc)

def updateItem(data, id):
    acc = Item.query.get(id)
    for k, v in data.items():
        setattr(acc, k, v)
    db.session.commit()
    return from_sql(acc)

def deleteItem(id):
    Item.query.filter_by(id=id).delete()
    db.session.commit()

# [ 按地點房號查詢]
def locationitemlist_desc(roomid, buwei=1000000, limit=500,cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Item.query
             .filter(Item.note1.like(f"%{roomid}%"))
             .order_by(desc(Item.itemno))
             #.limit(limit)
             #.offset(cursor)
             )
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)

# [ 按sn號查詢]
def snitemlist_desc(sn,buwei=1000000, limit=10,cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Item.query
             .filter(Item.sn.like(f"%{sn}%"))
             .order_by(desc(Item.itemno))
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)

# [ 按型號查詢]
def modelitemlist_desc(model,buwei=1000000, limit=10,cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Item.query
             .filter(Item.model.like(f"%{model}%"))
             .order_by(desc(Item.itemno))
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)

# [ 按產品號, 中的分類查詢]
def categoryitemlist_desc(cateid,buwei=1000000, limit=10,cursor=None):
    cursor = int(cursor) if cursor else 0
    sint=int(cateid)*buwei
    print(sint)
    query = (Item.query
             .filter(Item.itemno.between(sint,sint+buwei-1))
             .order_by(desc(Item.itemno))
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)

# [ 按票號查詢]
def Itemlist_by_acno(acc_acno):
    query = (Item.query
             .filter_by(acc_acno=acc_acno)
             .order_by(Item.id))
    lessons = builtin_list(map(from_sql, query.all()))
    return (lessons)

# [ START Item list]
def Itemlist(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Item.query
             #.filter_by(Open=1)
             .order_by(Item.id)
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)

# [ START Item list by desc]
def Itemlist_desc(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Item.query
             #.filter_by(Open=1)
             .order_by(desc(Item.id))
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)

# [START Item_list_by_CreateByUserID]
def Itemlist_by_user(user_id, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Item.query
             .filter_by(createdById=user_id)
             .order_by(Item.id)
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)
# [END Item_list_by_CreateByUserID]

# [ Read rows by tablename, for backup data.]
def readAllFromTable(tablename):
    if tablename=="acc":
        query = (Acc.query
                 .order_by(Acc.id))
        lessons = builtin_list(map(from_sql, query.all()))
        return (lessons)

    elif  tablename=="item":
        query = (Item.query
                 .order_by(Item.id))
        lessons = builtin_list(map(from_sql, query.all()))
        return (lessons)
    return None

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
        """
        Users_def=[
            User("admin","123","admin","1"),
            User("mbc","123","admin","1"),
            User("fin","123","admin","1"),
            User("fin1","123","admin","1"),
            User("ict","123","admin","1"),
            User("ga","123","admin","1"),
        ]
        #studa = User("stu","123","stu","8","SC1A","01")
        for u_ in Users_def:
            db.session.add(u_)
        """
        db.session.commit()
    print("All tables created")

if __name__ == '__main__':
    _create_database()

