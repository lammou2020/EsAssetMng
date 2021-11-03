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

