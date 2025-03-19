from flask import render_template, url_for, flash, redirect, request, Blueprint,\
current_app
from flask.helpers import send_from_directory
from PKDD import db
from flask import Blueprint
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
@main.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


@main.route('/download', methods=['GET'])
@login_required
def download():
    path = current_app.config['UPLOAD_DIRECTORY']
    return send_from_directory(path, 'cleaned_csvs.zip', as_attachment=True)


