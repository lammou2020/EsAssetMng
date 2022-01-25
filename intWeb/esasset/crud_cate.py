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


crud_cate = Blueprint('crud', __name__)

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



def CheckOwnRecordErr(book,session):
    if session["profile"].get("id")==1 : return None
    if str(session["profile"].get("id")) != book["createdById"] :  return "no create user!"
    return None



@crud_cate.route("/itemCateGrid")
@login_required_auth
def itemCateGrid():
    items= get_assest_model().ItemCatlist()
    return render_template("esasset/itemCategory/grid.html", items=items)
    

@crud_cate.route('/itemCateGrid_/addbatch/<cnt>', methods=['GET', 'POST'])
@login_required_auth
def itemcataddbatch(cnt):
    items= get_assest_model().createItemCat_blank(int(cnt))
    return f"{cnt}"


@crud_cate.route('/itemCateGrid_/api/JSON/updateSet/<nothing>', methods=['GET', 'POST'])
@login_required_auth
def itemCateGridJsonUpdateSet(nothing):
    data=request.get_json()
    book = get_assest_model().updateItemCat_DataSet(data)
    return "update !"



@crud_cate.route('/itemCateGrid_/api/JSON/update/<itemcat_id>', methods=['GET', 'POST'])
@login_required_auth
def itemCateGridJsonUpdate(itemcat_id):
    data=request.get_json()
    book = get_assest_model().updateItemCat(data, itemcat_id)
    return jsonify( book)
    

@crud_cate.route('/itemCateGrid_/api/OUTJSON', methods=['GET', 'POST'])
@login_required_auth
def itemCateGridApiOUTJSON():
    items= get_assest_model().ItemCatlist()
    return jsonify(items)


