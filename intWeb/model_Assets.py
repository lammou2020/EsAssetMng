# Copyright 2015 Google Inc.
from datetime import datetime
#from typing_extensions import NotRequired
#from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from config import SECRET_KEY

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

class Acc(db.Model):
    __tablename__ = 'Acc'
    id= db.Column(db.Integer,primary_key=True)
    acno = db.Column(db.String(80),unique=True,nullable=False)
    acc= db.Column(db.String(160))
    orderNo= db.Column(db.String(80))
    regSDate= db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    regEdate= db.Column(db.DateTime)
    voucherNo= db.Column(db.String(80))
    vendor= db.Column(db.String(80))
    total=db.Column(db.Integer)
    createdById = db.Column(db.String(255))    
    imageUrl = db.Column(db.String(255))    
    ctime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  #创建时间
    utime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  #更新时间
    describe=db.Column(db.Text)
    def __init__(self, acno=None, acc=None, orderNo=None, regSDate=None,voucherNo=None,vendor=None,createdById=None,imageUrl=None):
        self.acno=acno
        self.acc=acc
        self.orderNo=orderNo
        self.regSDate=regSDate
        self.voucherNo=voucherNo
        self.vendor=vendor
        self.createdById=createdById
        self.imageUrl=None
    def __repr__(self):
        return "<acc(accno='%s', acc=%s)" % (self.accno, self.acc)    

class Item(db.Model):
    __tablename__ = 'Item'    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    model= db.Column(db.String(80),unique=True,nullable=False)
    sn = db.Column(db.String(80),unique=True,nullable=False)
    quantity= db.Column(db.Integer)
    price = db.Column(db.Integer)
    amount= db.Column(db.Integer)
    # status
    adjust= db.Column(db.Integer)
    depreciation= db.Column(db.Integer)
    insure= db.Column(db.Integer)
    # ItemType
    itemTypeId = db.Column(db.Integer)
    # Acc
    # acno
    acc_id = db.Column(db.Integer, db.ForeignKey('Acc.id'), nullable=False)
    acc = db.relationship('Acc',  backref=db.backref('Item', lazy=True))
    #orderNO  = db.Column(db.String(80),unique=True,nullable=False)
    #voucherNo = db.Column(db.String(80),unique=True,nullable=False)
    #vendor = db.Column(db.String(80),unique=True,nullable=False)
    # Area
    #area_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    #db.relationship('Area', backref='Item', lazy=True)
    area = db.Column(db.String(80),unique=True,nullable=False)
    imageUrl = db.Column(db.String(255))    
    ctime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  #创建时间
    utime = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  #更新时间
    describe = db.Column(db.Text)
    #belong = models.ForeignKey('Belong', verbose_name='所属公司', null=True, blank=True, on_delete=models.SET_NULL)
    #manufacturer = models.ForeignKey('Manufacturer',verbose_name='厂家', null=True, blank=True, on_delete=models.CASCADE)
    #asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='virtual_machine', verbose_name="资产类型")
    #status = models.SmallIntegerField(choices=asset_status_choice, default=0, verbose_name='设备状态')
    #cpu = models.CharField(max_length=60,blank=True, null=True)
    #disk = models.CharField(max_length=60,blank=True, null=True)
    #memory = models.CharField(max_length=60,blank=True, null=True)
    #cabinet = models.CharField(max_length=32, null=True, blank=True, verbose_name='机柜号')
    #railnum = models.IntegerField(null=True, blank=True, verbose_name="导轨位置")
    #put_shelf_time = models.DateField(verbose_name='上线时间')

    def __init__(self, name=None):
        self.name =name
    def __repr__(self):
        return "<item(name='%s')" % (self.name)    

asset_type_choice = (
        ('cloud_host', '云主机'),
        ('virtual_machine', '虚拟机'),
        ('virtual_node','虚拟机节点'),
        ('container_node','容器主机节点'),
        ('server', '物理机'),
        ('switch', '交换机'),
        ('route', '路由器'),
        ('firewall', '防火墙'),
        ('lb','负载均衡设备'),
    )# 类型
asset_status_choice = (
        (0, '激活'),
        (1, '停用'),
        (2, '故障'),
    )# 状态

class ItemType(db.Model):
    __tablename__ = 'ItemType'    
    """    所有资产的共有数据表    """
    itemTypeId = db.Column(db.Integer,primary_key=True)
    itemTypeName = db.Column(db.String(80),unique=True,nullable=False)
    pk=db.Column(db.Integer)
    sk=db.Column(db.Integer)
    leaf=db.Column(db.Integer)
    describe=db.Column(db.Text)
    def __init__(self, itemTypeName=None, pk=None, sk=None, leaf=None, nodescribete=None):
        self.itemType=itemTypeName
        self.pk=pk
        self.sk=sk
        self.leaf=leaf
        self.describe=nodescribete
    def __repr__(self):
        return "<itemType(itemType='%s')" % (self.itemType)    

class Area(db.Model):
    __tablename__ = 'Area'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False) #"区域"
    subnet = db.Column(db.String(80))                          # ip subent 
    describe = db.Column(db.Text)
    def __init__(self, name=None):
        self.name=name
    def __repr__(self):
        return "<Area(name)='%s')" % (self.name)    

class Manufacturer(db.Model):
    __tablename__ = 'Manufacturer'
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(80),unique=True,nullable=False)
    contact = db.Column(db.String(80),unique=True,nullable=False)
    phone =db.Column(db.String(80),unique=True,nullable=False)
    describe = db.Column(db.Text)
    def __init__(self, name=None):
        self.name=name
    def __str__(self):
        return self.name

class Belong(db.Model):
    __tablename__ = 'Belong'    
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(80),unique=True,nullable=False)
    describe = db.Column(db.Text)
    def __init__(self, name=None):
        self.name=name
    def __str__(self):
        return self.name

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        """
        admin = User("admin","123","admin","1")
        studa = User("stu","123","stu","8","SC1A","01")
        studb = User("sta","123","stu","8","SC2A","01")
        db.session.add(admin)
        db.session.add(studa)
        db.session.add(studb)
        """
        db.session.commit()
    print("All tables created")

if __name__ == '__main__':
    _create_database()

