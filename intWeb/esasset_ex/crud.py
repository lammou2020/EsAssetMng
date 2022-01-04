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
import intWeb.esasset_ex.models_sql
from flask import g

crud = Blueprint('crud', __name__)

@crud.route("/")
def home():
    books = intWeb.esasset_ex.models_sql.ReadAccs()
    return render_template(
        "esasset_ex/index.html",
        books=books,
    )

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

@crud.route('/JSON/db/<tablename>')
@login_required_auth
def JSON_DB(tablename):
    book = get_assest_model().readAllFromTable(tablename)
    return jsonify(book)

def convert_timestamp(item_date_object):
    if isinstance(item_date_object, (date, datetime)):
        return item_date_object.timestamp()

@crud.route('/JSON/file/<tablename>')
@login_required_auth
def JSON_DBFILE(tablename):
    book = get_assest_model().readAllFromTable(tablename)
    xml =json.dumps(book,default=convert_timestamp)
    return Response(xml, mimetype='text/json',content_type="text/plain;charset=UTF-8")

