"# EsAsset" 
init db   
python main.py --initdb   

from datetime import datetime
datetime.strptime(start, '%Y-%m-%d')
Idea.query.filter(Idea.time >= datetime.strptime(start, '%Y-%m-%d'),
                  Idea.time <= datetime.strptime(end, '%Y-%m-%d')).all()
   
run    
python main.py   
設定    
1.號資產類 (為超級不分類別, 無法不需處理, 不屬任一項目/票據 )   
項目/票據 
view
edit
list

2.細項分類定義  

# 參考資料
## ORM 数据定義教程 
1 数据类型
类型名	MySQL类型	python类型	描述
SmallInteger	smallint	int	取值范围较小，一般为16位
Integer	int	int	普通整数，一般32位
BigInteger	bigint	int/long	不限精度的整数
Float	float	float	浮点数
Numeric	decimal	decimal.Decimal	定点数
String	varchar	str	变长字符串
Text(65536)	tinytext	str	变长字符串，64K,2 16 − 1 2^{16}-12 16 −1=65535bytes
Text(16777216)	mediumtext	str	变长字符串，max16M,2 24 − 1 2^{24}-12 24 −1=16777215bytes
Text(4294967295)	longtext	str	变长字符串，max32M,2 32 − 1 2^{32}-12 32 −1=4294967295bytes
LargeBinary	blob	str	二进制文件，64K
LargeBinary(65536)	mediumblob	str	二进制，max16M
LargeBinary(16777216)	longblob	str	二进制，max32M
PickleType	blob	任何python对象	自动使用Pickle序列化，只有blob
Unicode	varchar	unicode	变长字符串
UnicodeText	text	unicode	变长字符串，64K
Boolean	tinyint	bool	布尔值
Date	date	datetime.date	日期
Time	time	date.time	时间
DateTime	datetime	datetime.datetime	日期和时间
Interval	datetime	datetime.timedelta	时间间隔
Enum	enum	str	一组字符串
2 数据库类型设计
建立MySQL表
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

MySQL表结构
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


3 Flask-MySQL键属性
属性	描述	生效值
primary_key	主键	True
unique	键值唯一性	True
index	索引	True
nullable	空值	True
default	默认值	null
————————————————
