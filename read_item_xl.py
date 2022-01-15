from openpyxl import Workbook  
out_wb = Workbook()
out_ws = out_wb.active
source_file_name="doc/out_asset_data.xlsx"
out_file_name="doc/out_item.py"

from openpyxl import load_workbook   

field_colum_names=  ['物品編號', '年度', '憑單編號',            '傳票號碼', '物品', '牌子及型號', 'S/N (P/N)', '數量', '單價(M$) ', '總值(M$)', '攤折淨值(M$)', '存放地點', '資助', '資助項目名稱', '備註', '供應商', '登賬日期','cate_','unit']
ignore_ws=['資產分類表','工作表1']
ignore_col=['異動   原因','異動原因','*    攤折完成',  '*  攤折完', '* 攤折完成','*  攤折完成','^ 投保產物', '投保項備註','學校資金']

out_ws.append(field_colum_names)

wb = load_workbook(filename = source_file_name)
for sn_ in wb.sheetnames:
    if sn_ != "Sheet" :continue    
    ws=wb[sn_]
    for ridx in range(1,70):
        row_ =[]
        for cidx in range(65,88):
            colum_name_=ws[f"{chr(cidx)}{ridx}"].value
            #if colum_name_==None: break
            row_.append(colum_name_)
        print(row_)
        out_ws.append(row_)

out_wb.save(out_file_name)