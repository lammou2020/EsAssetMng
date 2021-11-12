from intWeb import storage, login_required_auth
from intWeb import get_assest_model
from flask import flash,Blueprint, current_app, redirect, render_template, request, \
    session, url_for,send_file,Flask,send_from_directory,jsonify
import os
import zipfile
import math
from urllib.parse import quote
from datetime import datetime


crud = Blueprint('crud', __name__)

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

@crud.route("/")
def home():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_assest_model().list(cursor=token)
    return render_template(
        "esasset/index.html",
        books=books,
        next_page_token=next_page_token)

@crud.route("/list")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_assest_model().list_desc(cursor=token)
    return render_template(
        "esasset/list.html",
        books=books,
        next_page_token=next_page_token)

# [START list_mine]
@crud.route("/mine")
@login_required_auth
def list_mine():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_assest_model().list_by_user(
        user_id=session['profile']['id'],
        cursor=token)
    return render_template(
        "esasset/list.html",
        books=books,
        next_page_token=next_page_token)
# [END list_mine]

@crud.route("/categoryitemlist/<cateid>")
def categoryitemlist(cateid):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_assest_model().categoryitemlist_desc(cateid=cateid,buwei=1000000,cursor=token)
    #between
    return render_template(
        "esasset/item/list.html",
        books=books,
        next_page_token=next_page_token)

@crud.route("/JSON/categoryitemlist/<cateid>")
def JSONcategoryitemlist(cateid):
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_assest_model().categoryitemlist_desc(cateid=cateid,buwei=1000,cursor=token)
    return jsonify(books)



def Get_FileList(crspath, filenames, prefix=None):
    path = current_app.config['HW_UPLOAD_FOLDER']
    LECTURE_FOLDER = os.path.join(path, crspath)
    if not os.path.isdir(LECTURE_FOLDER):
        os.mkdir(LECTURE_FOLDER)
    else:
        for root,dirs, files in os.walk(LECTURE_FOLDER):
            for file in files:
                if prefix==None:
                    basename, extension = file.rsplit('.', 1)
                    _file=basename.split('-_')[0]+"."+extension
                    filenames.append({"f":quote(str(file)),"n":_file})    
                elif prefix in file:
                    basename, extension = file.rsplit('.', 1)
                    _file=basename.split('-_')[0]+"."+extension
                    filenames.append({"f":quote(str(file)),"n":_file})    
    pass

#####
# [START add]


@crud.route('/<id>/item/<itemid>')
def itemview(id,itemid):
    book = get_assest_model().readItem(itemid)
    filenames=[]
    crspath=str(book["acc_acno"])
    Get_FileList(crspath,filenames,"ASS"+crspath+"ID"+str(book["id"])+"_")             
    return render_template("esasset/item/view.html",acc_id=id, book=book,filenames=filenames)


@crud.route('/<id>/item/add', methods=['GET', 'POST'])
@login_required_auth
def itemadd(id):
    acc_acno= (request.args.get('acno', "0"))
    regSDate= (request.args.get('regSDate', datetime.today().strftime( '%Y-%m-%d')))
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
        if data["itemno"]==""  or data["itemno"]=="None" or data["itemno"]==None:
            data["itemno"]=None
        else:
            #data["itemTypeId"]=math.floor(int(data["itemno"])/1000000)
            pass
        book = get_assest_model().createItem(data)

        return redirect(url_for('.itemview', id=id,itemid=book['id']))
    book={
        "quantity":"0",
        "price":"0",
        "adjust":"0",
        "amount":"0",
        "depr_ed":"0",
        "acc_acno":acc_acno,
        "regSDate":regSDate}
    return render_template("esasset/item/form.html", action="Add", book=book)
# [END add]

@crud.route('/<id>/item/api/JSON/update/<itemid>', methods=['GET', 'POST'])
@login_required_auth
def itemJsonUpdate(id,itemid):
    data=request.get_json()
    print(data)
    if 'regSDate' in data:
        data['regSDate']=datetime.strptime(data['regSDate'], '%Y-%m-%d')
    if 'itemno' in data:   
        if data["itemno"]=="" or data["itemno"]=="None" or data["itemno"]==None:
            data["itemno"]=None
        else:
            #data["itemTypeId"]=math.floor(int(data['itemno'])/1000000)
            pass
    book = get_assest_model().updateItem(data, itemid)
    return jsonify( book)


@crud.route('/<id>/item/<itemid>/edit', methods=['GET', 'POST'])
@login_required_auth
def itemedit(id,itemid):
    book = get_assest_model().readItem(itemid)
    print(book)
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
        else:
            #data["itemTypeId"]=math.floor(int(data['itemno'])/1000000)
            pass
        book = get_assest_model().updateItem(data, itemid)
        #return redirect(url_for('.view', id=book['id']))
        return redirect(url_for('.itemview', id=id,itemid=book['id']))

    return render_template("esasset/item/form.html", action="Edit", book=book)

#####
@crud.route('/<id>/item/<itemid>/delete')
@login_required_auth
def itemdelete(id,itemid):
    book = get_assest_model().readItem(itemid)
    crspath=book["acc_acno"]
    if (book["createdById"]==str(session['profile']['id']))  :
        path = current_app.config['HW_UPLOAD_FOLDER']
        #UPLOAD_FOLDER = os.path.join(path, crspath)
        #for root,dirs, files in os.walk(UPLOAD_FOLDER):
        #   for file in files:      
        #       os.remove(UPLOAD_FOLDER+"/"+file)
        get_assest_model().deleteItem(itemid)        
    return redirect(url_for('.view',id=id))


@crud.route('/<id>/item/<itemid>/upload', methods=['GET', 'POST'])
def uploadItemfiles(id,itemid):
    book = get_assest_model().readItem(itemid)
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

@crud.route('/<id>/item/<itemid>/download/<filename>')
def download_item_file(id,itemid,filename):
    book = get_assest_model().readItem(itemid)
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

#####
@crud.route('/<id>')
def view(id):
    book = get_assest_model().read(id)
    book["regSDate"]=book["regSDate"].strftime( '%Y-%m-%d')
    items=  get_assest_model().Itemlist_by_acno(book["acno"])
    filenames=[]
    crspath=str(book["acno"])
    Get_FileList(crspath,filenames)     #"ACC"+crspath+"_"
    return render_template("esasset/view.html", book=book,items=items,filenames=filenames)

# [START add]
@crud.route('/add', methods=['GET', 'POST'])
@login_required_auth
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        # If an image was uploaded, update the data to point to the new image.
        path = current_app.config['HW_UPLOAD_FOLDER']
        image_url = upload_image_file(request.files.get('image'),path,str(data["acno"]))
        if image_url:
            data['imageUrl'] = image_url
        # If the user is logged in, associate their profile with the new book.
        if 'profile' in session:
            data['createdById'] = session['profile']['id']
        data['regSDate']=datetime.strptime(data['regSDate'], '%Y-%m-%d')
        book = get_assest_model().create(data)
        return redirect(url_for('.view', id=book['id']))
    book={
        "total":"0",
        "readonly":"0",
        "regSDate":datetime.today().strftime( '%Y-%m-%d')
        }
        
    return render_template("esasset/form.html", action="Add", book=book)
# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
@login_required_auth
def edit(id):
    book = get_assest_model().read(id)
    book["regSDate"]=book["regSDate"].strftime( '%Y-%m-%d')
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        path = current_app.config['HW_UPLOAD_FOLDER']
        image_url = upload_image_file(request.files.get('image'),path,str(data["acno"]))

        if image_url:
            data['imageUrl'] = image_url
        data['regSDate']=datetime.strptime(data['regSDate'], '%Y-%m-%d')
        book = get_assest_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("esasset/form.html", action="Edit", book=book)


@crud.route('/<id>/delete')
@login_required_auth
def delete(id):
    book = get_assest_model().read(id)
    crspath=book["Path"]
    if (book["createdById"]==str(session['profile']['id']))  :

        path = current_app.config['HW_UPLOAD_FOLDER']
        UPLOAD_FOLDER = os.path.join(path, crspath)
        for root,dirs, files in os.walk(UPLOAD_FOLDER):
           for file in files:      
               os.remove(UPLOAD_FOLDER+"/"+file)
        get_assest_model().delete(id)        
    return redirect(url_for('.list'))


@crud.route("/<id>/itemgrid")
def itemgrid(id):
    book = get_assest_model().read(id)
    book["regSDate"]=book["regSDate"].strftime( '%Y-%m-%d')
    items= get_assest_model().Itemlist_by_acno(book["acno"])
    filenames=[]
    #Get_FileList(book,filenames)             
    return render_template("esasset/grid.html", book=book,items=items,lecturesfile=[],filenames=filenames)


@crud.route('/<id>/downloadall')
def download_all(id):
    book = get_assest_model().read(id)
    crspath=book["Path"]
    seat=session['profile']['Seat']
    path = current_app.config['HW_UPLOAD_FOLDER']
    UPLOAD_FOLDER = os.path.join(path, crspath)
    ZIP_PATH = os.path.join(path, "ZIPFILE")
    if not os.path.isdir(ZIP_PATH):
        os.mkdir(ZIP_PATH)
    # Zip file Initialization and you can change the compression type
    ZipFileName=f"HW{crspath}.zip"
    ZipFilePath=ZIP_PATH+"/"+ZipFileName
    zipfolder = zipfile.ZipFile(ZipFilePath,'w', compression = zipfile.ZIP_STORED)
    # zip all the files which are inside in the folder
    for root,dirs, files in os.walk(UPLOAD_FOLDER):
        for file in files:
            zipfolder.write(UPLOAD_FOLDER+'/'+file)
    zipfolder.close()
    return send_file(ZipFilePath,
            mimetype = 'zip',
            attachment_filename= ZipFileName,
            as_attachment = True)
    os.remove(ZipFilePath)

@crud.route('/<id>/download/<filename>')
def download_file(id,filename):
    book = get_assest_model().read(id)
    crspath=str(book["acno"])
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
                mimetype = 'image/*',
                )
    else:
        return send_file(FilePath,
                mimetype = 'zip',
                attachment_filename= _file,
                as_attachment = True)
    # Delete the zip file if not needed

@crud.route('/<id>/downloadlecture/<filename>')
def download_lecturefile(id,filename):
    book = get_assest_model().read(id)
    crspath=book["Path"]
    #return render_template("view.html", book=book)
    # Get current path os.getcwd()
    path = current_app.config['HW_UPLOAD_FOLDER']
    # file Upload
    UPLOAD_FOLDER = os.path.join(path, crspath+"LECTURE")
    FilePath=UPLOAD_FOLDER+"/"+filename
    basename, extension = filename.rsplit('.', 1)
    _file=basename.split('-_')[0]+"."+extension    
    return send_file(FilePath,
            mimetype = 'zip',
            attachment_filename= _file,
            as_attachment = True)
    # Delete the zip file if not needed

@crud.route('/<id>/img/<filename>')
def showimage(id,filename):
    # Get current path os.getcwd()
    path = current_app.config['HW_UPLOAD_FOLDER']
    # file Upload
    #UPLOAD_FOLDER = os.path.join(path, filename)
    FilePath=path+"/"+filename
    return send_file(FilePath,
            mimetype = 'image/*')
    # Delete the zip file if not needed

@crud.route('/<id>/upload', methods=['GET', 'POST'])
def uploadfiles(id):
    book = get_assest_model().read(id)
    crspath=str(book["acno"])
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
            upload_hw_file(file,UPLOAD_FOLDER,"ACC"+crspath+"_")
        
        flash('File(s) successfully uploaded')
        return redirect(f"/EsAsset/{id}")
        #return render_template("view.html", book=book)


@crud.route('/<id>/cleanclasswork')
@login_required_auth
def cleanclasswork(id):
    book = get_assest_model().read(id)
    crspath=book["Path"]
    if (book["createdById"]==str(session['profile']['id']))  :
        path = current_app.config['HW_UPLOAD_FOLDER']
        UPLOAD_FOLDER = os.path.join(path, crspath)
        for root,dirs, files in os.walk(UPLOAD_FOLDER):
           for file in files:      
               os.remove(UPLOAD_FOLDER+"/"+file)
        #get_assest_model().delete(id)        
    return redirect(url_for('.list'))



@crud.route('/JSON/db/<tablename>')
@login_required_auth
def JSON_DB(tablename):
    book = get_assest_model().readAllFromTable(tablename)
    return jsonify(book)