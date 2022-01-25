from cmd import IDENTCHARS
from winsound import SND_LOOP
from intWeb import storage, login_required_auth
from intWeb import get_assest_model
from flask import flash,Blueprint, current_app, redirect, render_template, request, \
    session, url_for,send_file,Flask,send_from_directory,jsonify
import os
import zipfile
import math
from urllib.parse import quote
from datetime import datetime,date
from flask import Response
import json
import io
from openpyxl.workbook import Workbook
from openpyxl import load_workbook   
from flask_qrcode import QRcode


crud_item = Blueprint('crud', __name__)

def upload_hw_file(file,UPLOAD_FOLDER,seat):
    if not file:
        return None
    public_url = storage.upload_hw_file(
        file,
        file.filename,
        file.content_type,
        UPLOAD_FOLDER,
        0,
        seat
    )
    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)
    return public_url


def upload_image_file(file,UPLOAD_FOLDER,pixStr=None):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None
    public_url = storage.upload_file(
        file,#.read(),
        file.filename,
        file.content_type,
        UPLOAD_FOLDER,
        pixStr,
        "EsAsset",
    )
    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)
    return public_url



def CheckOwnRecordErr(book,session):
    if session["profile"].get("id")==1 : return None
    if str(session["profile"].get("id")) != book["createdById"] :  return "no create user!"
    return None


@crud_item.route("/showitem")
@login_required_auth
def show_item_grid():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_assest_model().Itemlist(limit=6000,cursor=token)
    return render_template(
        "esasset/grid.html",
        book={"id":0},
        items=books,
        next_page_token=next_page_token)  



@crud_item.route("/locationitemlist/<roomid>")
def locationitemlist(roomid):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_assest_model().locationitemlist_desc(roomid=roomid,buwei=1000000,cursor=token)
    #between
    return render_template(
        "esasset/item/list.html",
        books=books,
        next_page_token=next_page_token,roomid=roomid)

@crud_item.route("/snitemlist/<serialno>")
def snitemlist(serialno):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    if len(serialno)<4 : 
        return render_template("esasset/item/list.html", books=[])

    books, next_page_token = get_assest_model().snitemlist_desc(sn=serialno,cursor=token)
    #between
    return render_template(
        "esasset/item/list.html",
        books=books,
        next_page_token=next_page_token)


@crud_item.route("/modelitemlist/<model_no>")
def modelitemlist(model_no):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    if len(model_no)<4 : 
        return render_template("esasset/item/list.html", books=[])

    books, next_page_token = get_assest_model().modelitemlist_desc(model=model_no,cursor=token)
    #between
    return render_template(
        "esasset/item/list.html",
        books=books,
        next_page_token=next_page_token)


@crud_item.route("/categoryitemlist/<cateid>")
def categoryitemlist(cateid):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    buwei=1000000
    modwei=10000000000 
    if len(cateid)>4 : buwei=1000
    books, next_page_token = get_assest_model().categoryitemlist_asc(cateid=cateid,modwei=modwei,buwei=buwei,cursor=token)
    #between
    return render_template(
        "esasset/grid.html",
        book={"id":0},items=books,
        next_page_token=next_page_token)


@crud_item.route("/JSON/categoryitemlist/<cateid>")
def JSONcategoryitemlist(cateid):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    buwei=1000
    mask=request.args.get("mask",None)
    if mask!=None:
        buwei=int(mask)
    books, next_page_token = get_assest_model().categoryitemlist_desc(cateid=cateid,buwei=buwei,cursor=token)
    print(books)
    return jsonify(books)



#####
# [START add]


@crud_item.route('/<id>/item/<itemid>')
@login_required_auth
def itemview(id,itemid):
    book,acc_id= get_assest_model().readItem(itemid)
    if id!="0" : acc_id=id
    filenames=[]
    crspath=str(book["acc_acno"])
    Get_FileList(crspath,filenames,"ASS"+crspath+"ID"+str(book["id"])+"_")             
    return render_template("esasset/item/view.html",acc_id=acc_id, book=book,filenames=filenames)


@crud_item.route('/<id>/item/add', methods=['GET', 'POST'])
@login_required_auth
def itemadd(id):
    acc_acno= request.args.get('acno', "0")
    sess= request.args.get('sess', "0000")
    regSDate= request.args.get('regSDate', datetime.today().strftime( '%Y-%m-%d'))
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        path = current_app.config['HW_UPLOAD_FOLDER']
        image_url = upload_image_file(request.files.get('image'),path,acc_acno)

        if image_url:
            data['imageUrl'] = image_url

        # If the user is logged in, associate their profile with the new book.
        if 'profile' in session:
            data['createdById'] = session['profile']['id']
        data['regSDate']=datetime.strptime(data['regSDate'], '%Y-%m-%d')

        for f_ in ['itemno',"price", "quantity", "p_amount", "amount", "fund_amount","gno","ict"]:
            if f_ in data:   
                if data[f_]=="" or data[f_]=="None" or data[f_]==None:
                    data[f_]=None
        book = get_assest_model().createItem(data)

        return redirect(url_for('.itemview', id=id,itemid=book['id']))
    book={
        "quantity":"0",
        "price":"0",
        "adjust":"0",
        "amount":"0",
        "depr_year":"0",
        "sess":sess,
        "acc_acno":acc_acno,
        "regSDate":regSDate}
    return render_template("esasset/item/form.html", action="Add", book=book)
# [END add]


@crud_item.route('/<id>/item/addbatch/<cnt>', methods=['GET', 'POST'])
@login_required_auth
def itemaddbatch(id,cnt):
    acc_acno= (request.args.get('acno', "0"))
    sess= (request.args.get('sess', "0000"))
    regSDate= (request.args.get('regSDate', datetime.today().strftime( '%Y-%m-%d')))
    if acc_acno=="0" :
        acc_rec = get_assest_model().read(id)
        regSDate=acc_rec["regSDate"].strftime( '%Y-%m-%d')
        acc_acno=  acc_rec["acno"]
    data={
        "itemno":"",
        "quantity":"0",
        "price":"0",
        "amount":"0",
        "sess":sess,
        "acc_acno":acc_acno,
        "regSDate":regSDate}
        
    if 'profile' in session:
        data['createdById'] = session['profile']['id']

    data['regSDate']=datetime.strptime(data['regSDate'], '%Y-%m-%d')
    if data["itemno"]==""  or data["itemno"]=="None" or data["itemno"]==None:
        data["itemno"]=None
    else:
        pass
    #for i in range(int(cnt)):
    book = get_assest_model().createItem_Blank(data,int(cnt))
    return f"{cnt}"
# [END add]


@crud_item.route('/<id>/item/api/JSON/update/<itemid>', methods=['GET', 'POST'])
@login_required_auth
def itemJsonUpdate(id,itemid):
    data=request.get_json()
    if 'regSDate' in data:
        data['regSDate']=datetime.strptime(data['regSDate'], '%Y-%m-%d')
    for f_ in ['itemno',"price", "quantity", "p_amount", "amount", "fund_amount","gno","ict"]:
        if f_ in data:   
            if data[f_]=="" or data[f_]=="None" or data[f_]==None:
                data[f_]=None
    print(data)
    print(itemid)
    book = get_assest_model().updateItem(data, itemid)
    return jsonify( book)


@crud_item.route('/<id>/item/api/JSON/updateSet/<nothing>', methods=['GET', 'POST'])
@login_required_auth
def itemJsonUpdateSet(id,nothing):
    data=request.get_json()
    for itemid in data:
        if 'regSDate' in data[itemid]:
            data[itemid]['regSDate']=datetime.strptime(data[itemid]['regSDate'], '%Y-%m-%d')
        for f_ in ['itemno',"price", "quantity", "p_amount", "amount", "fund_amount","gno","ict"]:
            
            if f_ in data[itemid]:
                if data[itemid][f_]=="" or data[itemid][f_]=="None" or data[itemid][f_]==None:
                    data[itemid][f_]=None
    cnt = get_assest_model().updateItem_DataSet(data)
    return f"updated {cnt} rows."



@crud_item.route('/<id>/item/<itemid>/edit', methods=['GET', 'POST'])
@login_required_auth
def itemedit(id,itemid):
    book, acc_id  = get_assest_model().readItem(itemid)
    Err=CheckOwnRecordErr(book,session) 
    if Err!= None :  return Err
    if  book['regSDate'] !=None:
        book['regSDate']=book['regSDate'].isoformat()[:10]
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        path = current_app.config['HW_UPLOAD_FOLDER']
        image_url = upload_image_file(request.files.get('image'),path,str(data["acc_acno"]))
        if image_url:
            data['imageUrl'] = image_url
        
        data['regSDate']=datetime.strptime(data['regSDate'], '%Y-%m-%d')
        if data["itemno"]=="" or data["itemno"]=="None" or data["itemno"]==None:
            data["itemno"]=None
        
        for f_ in ['itemno',"price", "quantity", "p_amount", "amount", "fund_amount","gno","ict"]:
            if f_ in data:   
                if data[f_]=="" or data[f_]=="None" or data[f_]==None:
                    data[f_]=None      
        
        book = get_assest_model().updateItem(data, itemid)
        #return redirect(url_for('.view', id=book['id']))
        return redirect(url_for('.itemview', id=id,itemid=book['id']))

    return render_template("esasset/item/form.html", action="Edit", book=book)


#####
@crud_item.route('/<id>/item/<itemid>/delete')
@login_required_auth
def itemdelete(id,itemid):
    book,acc_id = get_assest_model().readItem(itemid)
    crspath=book["acc_acno"]
    if (book["createdById"]==str(session['profile']['id']))  :
        path = current_app.config['HW_UPLOAD_FOLDER']
        #UPLOAD_FOLDER = os.path.join(path, crspath)
        #for root,dirs, files in os.walk(UPLOAD_FOLDER):
        #   for file in files:      
        #       os.remove(UPLOAD_FOLDER+"/"+file)
        get_assest_model().deleteItem(itemid)        
    return redirect(url_for('.view',id=id))


@crud_item.route('/<id>/item/<itemid>/upload', methods=['GET', 'POST'])
def uploadItemfiles(id,itemid):
    book,acc_id = get_assest_model().readItem(itemid)
    crspath=str(book["acc_acno"])
    path = current_app.config['HW_UPLOAD_FOLDER']
    UPLOAD_FOLDER = os.path.join(path, crspath)
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return render_template("view.html", book=book)
        files = request.files.getlist('files[]')
        for file in files:
            upload_hw_file(file,UPLOAD_FOLDER,"ASS"+crspath+"ID"+str(book["id"])+"_")
        flash('File(s) successfully uploaded')
        return redirect(f"/EsAsset/{id}")
        #return render_template("view.html", book=book)    


@crud_item.route('/<id>/item/<itemid>/download/<filename>')
def download_item_file(id,itemid,filename):
    book,acc_id = get_assest_model().readItem(itemid)
    crspath=str(book["acc_acno"])
    #return render_template("view.html", book=book)
    # Get current path os.getcwd()
    path = current_app.config['HW_UPLOAD_FOLDER']
    # file Upload
    UPLOAD_FOLDER = os.path.join(path, crspath)
    FilePath=UPLOAD_FOLDER+"/"+filename
    basename, extension = filename.rsplit('.', 1)
    _file=basename.split('-_')[0]+"."+extension    
    if extension in  ['jpg']:
        return send_file(FilePath,
                mimetype = 'image/*')
    else:
        return send_file(FilePath,
                mimetype = 'zip',
                attachment_filename= _file,
                as_attachment = True)
    # Delete the zip file if not needed



@crud_item.route("/<id>/itemgrid")
@login_required_auth
def itemgrid(id):
    book = get_assest_model().read(id)
    Err=CheckOwnRecordErr(book,session)
    if Err != None:  return Err
    book["regSDate"]=book["regSDate"].strftime( '%Y-%m-%d')
    items= get_assest_model().Itemlist_by_acno(book["acno"])
    filenames=[]
    return render_template("esasset/grid.html", book=book,items=items,lecturesfile=[],filenames=filenames)



