from flask import render_template, url_for, flash, redirect, request, Blueprint,\
send_from_directory
from PKDD import db
from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title= 'PKDD-99 Statistics')


@main.route('/download')
def download():
    return send_from_directory('static/cleaned_csvs', 'cleaned_csvs.zip', as_attachment=True)

