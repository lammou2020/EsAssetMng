from intWeb import get_model,  storage, login_required_auth
from flask import flash,Blueprint, current_app, redirect, render_template, request, \
    session, url_for,send_file,Flask,send_from_directory
import os
import zipfile

from urllib.parse import quote

crud = Blueprint('crud', __name__)

def upload_hw_file(file,UPLOAD_FOLDER,seat):
    if not file:
        return None
    public_url = storage.upload_hw_file(
        file,
        file.filename,
        file.content_type,
        UPLOAD_FOLDER,
        seat
    )
    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)
    return public_url

def upload_image_file(file,UPLOAD_FOLDER):
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
        UPLOAD_FOLDER
    )
    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)
    return public_url

@crud.route("/")
def home():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_model().list(cursor=token)
    return render_template(
        "index.html",
        books=books,
        next_page_token=next_page_token)

@crud.route("/list")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_model().list(cursor=token)
    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)

# [START list_mine]
@crud.route("/mine")
@login_required_auth
def list_mine():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_model().list_by_user(
        user_id=session['profile']['id'],
        cursor=token)
    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)
# [END list_mine]

@crud.route('/<id>')
def view(id):
    book = get_model().read(id)
    crspath=book["Path"]
    crsclassno=book["Classno"]
    lecturesfile=[]    
    filenames=[]  
    path = current_app.config['HW_UPLOAD_FOLDER']
    LECTURE_FOLDER = os.path.join(path, crspath+"LECTURE")
    if not os.path.isdir(LECTURE_FOLDER):
        os.mkdir(LECTURE_FOLDER)
    for root,dirs, files in os.walk(LECTURE_FOLDER):
        for file in files:
            basename, extension = file.rsplit('.', 1)
            _file=basename.split('-_')[0]+"."+extension
            lecturesfile.append({"f":quote(str(file)),"n":_file})    
    if session=={}:
        pass
    elif session.get('profile') is None :
        pass
    elif session.get('profile') == {} :
        pass        
    else:
        seat=session['profile'].get('Seat')
        classno=session['profile']['Classno']
        if (book["createdById"]==str(session['profile']['id'])) or (crsclassno==classno) :
            path = current_app.config['HW_UPLOAD_FOLDER']
            LECTURE_FOLDER = os.path.join(path, crspath+"LECTURE")
            if not os.path.isdir(LECTURE_FOLDER):
                os.mkdir(LECTURE_FOLDER)
    
            UPLOAD_FOLDER = os.path.join(path, crspath)
            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)  
            for root,dirs, files in os.walk(UPLOAD_FOLDER):
                for file in files:
                    basename, extension = file.rsplit('.', 1)
                    bn=basename.split('-_')
                    _file=bn[0]+"."+extension
                    fseat=""
                    if len(bn)>1: fseat=bn[1][:2]
                    if f"-_{seat}" in file:
                        filenames.append({"f":"#","n":_file})
                    elif session['profile']['Role']<"8":
                        filenames.append({"f":quote(str(file)),"n":f"{_file} {fseat}"})
    return render_template("view.html", book=book,lecturesfile=lecturesfile,filenames=filenames)
    
@crud.route('/<id>/downloadall')
def download_all(id):
    book = get_model().read(id)
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
    book = get_model().read(id)
    crspath=book["Path"]
    seat=session['profile']['Seat']
    #return render_template("view.html", book=book)
    # Get current path os.getcwd()
    path = current_app.config['HW_UPLOAD_FOLDER']
    # file Upload
    UPLOAD_FOLDER = os.path.join(path, crspath)
    FilePath=UPLOAD_FOLDER+"/"+filename
    basename, extension = filename.rsplit('.', 1)
    _file=basename.split('-_')[0]+"."+extension    
    return send_file(FilePath,
            mimetype = 'zip',
            attachment_filename= _file,
            as_attachment = True)
    # Delete the zip file if not needed

@crud.route('/<id>/downloadlecture/<filename>')
def download_lecturefile(id,filename):
    book = get_model().read(id)
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
    book = get_model().read(id)
    crspath=book["Path"]
    seat=session['profile']['Seat']
    path = current_app.config['HW_UPLOAD_FOLDER']
    LECTURE_FOLDER = os.path.join(path, crspath+"LECTURE")
    if not os.path.isdir(LECTURE_FOLDER):
        os.mkdir(LECTURE_FOLDER)
    UPLOAD_FOLDER = os.path.join(path, crspath)
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    if session['profile']['Role']<"8":
        UPLOAD_FOLDER=LECTURE_FOLDER
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return render_template("view.html", book=book)
        files = request.files.getlist('files[]')
        for file in files:
            upload_hw_file(file,UPLOAD_FOLDER,seat)
        flash('File(s) successfully uploaded')
        return redirect(f"/lessons/{id}")
        #return render_template("view.html", book=book)



# [START add]
@crud.route('/add', methods=['GET', 'POST'])
@login_required_auth
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        path = current_app.config['HW_UPLOAD_FOLDER']
        image_url = upload_image_file(request.files.get('image'),path)

        if image_url:
            data['imageUrl'] = image_url

        # If the user is logged in, associate their profile with the new book.
        if 'profile' in session:
            data['createdById'] = session['profile']['id']

        book = get_model().create(data)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Add", book={})
# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
@login_required_auth
def edit(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        path = current_app.config['HW_UPLOAD_FOLDER']
        image_url = upload_image_file(request.files.get('image'),path)

        if image_url:
            data['imageUrl'] = image_url

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Edit", book=book)


@crud.route('/<id>/delete')
@login_required_auth
def delete(id):
    book = get_model().read(id)
    crspath=book["Path"]
    if (book["createdById"]==str(session['profile']['id']))  :

        path = current_app.config['HW_UPLOAD_FOLDER']
        UPLOAD_FOLDER = os.path.join(path, crspath)
        for root,dirs, files in os.walk(UPLOAD_FOLDER):
           for file in files:      
               os.remove(UPLOAD_FOLDER+"/"+file)
        get_model().delete(id)        
    return redirect(url_for('.list'))

@crud.route('/<id>/cleanclasswork')
@login_required_auth
def cleanclasswork(id):
    book = get_model().read(id)
    crspath=book["Path"]
    if (book["createdById"]==str(session['profile']['id']))  :
        path = current_app.config['HW_UPLOAD_FOLDER']
        UPLOAD_FOLDER = os.path.join(path, crspath)
        for root,dirs, files in os.walk(UPLOAD_FOLDER):
           for file in files:      
               os.remove(UPLOAD_FOLDER+"/"+file)
        #get_model().delete(id)        
    return redirect(url_for('.list'))
