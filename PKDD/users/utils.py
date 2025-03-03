import os
import secrets
from flask import url_for, current_app, request, abort
from flask_mail import Message
from PKDD import mail
from PKDD.users.users_models import User
import requests

def send_reset_email(user: User):
    token = user.get_token()
    msg = Message('Password Reset Request',
                  sender=os.getenv('EMAIL_USERNAME'),
                    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_password_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def send_delete_account_email(user: User):
    token = user.get_token()
    msg = Message('Account Deletion Request',
                  sender=os.getenv('EMAIL_USERNAME'),
                    recipients=[user.email])
    msg.body = f'''To delete your account, visit the following link:
{url_for('users.delete_account', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)



def recaptcha_register_verify():
    response = request.form['g-recaptcha-response']
    verify_response = requests.post(
    url=f'{current_app.config['RECAPTCHA_VERIFY_URL']}?secret={current_app.config['RECAPTCHA_KEY']}&response={response}'
    ).json()
    if verify_response['success'] == False:
        abort(401)