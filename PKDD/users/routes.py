from flask import render_template, url_for, flash, redirect, request, Blueprint,\
send_from_directory
from PKDD import db
from flask import Blueprint


users = Blueprint('users', __name__)

@users.route('/login')
def login():
    return render_template('login.html', title= 'PKDD-99 Statistics - Login')