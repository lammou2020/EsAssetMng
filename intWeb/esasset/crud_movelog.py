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


crud_movelog = Blueprint('crud', __name__)

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




@crud_movelog.route("/")
@login_required_auth
def home():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_assest_model().list(cursor=token)
    return render_template(
        "esasset/index.html",
        books=books,
        next_page_token=next_page_token)



@crud_movelog.route('/api/JSON/pushItemnoMoveLog', methods=['GET', 'POST'])
@login_required_auth
def pushItemMoveLogJson():
    data=request.get_json()
    if 'profile' in session:
        data['createdById'] = session['profile']['id']
    print(data)
    book = get_assest_model().createItemMoveLog(data)
    return jsonify( book)


@crud_movelog.route('/api/JSON/getItemnoMoveLog_by_itemno/<itemno>', methods=['GET', 'POST'])
@login_required_auth
def getItemMoveLogJson(itemno):
    book = get_assest_model().ItemMoveLoglist_by_itemno(itemno)
    return jsonify( book)

