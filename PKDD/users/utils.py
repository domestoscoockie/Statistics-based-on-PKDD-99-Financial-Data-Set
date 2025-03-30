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
    try:
        # Get reCAPTCHA response
        response = request.form.get('g-recaptcha-response')
        
        # Check if response exists
        if not response:
            current_app.logger.error("No reCAPTCHA response received")
            abort(401, description="Please complete the reCAPTCHA")
            
        # Verify with Google
        verify_response = requests.post(
            url='https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': current_app.config['RECAPTCHA_SECRET_KEY'],
                'response': response,
                'remoteip': request.remote_addr
            }
        ).json()
        
        # Log verification response for debugging
        current_app.logger.info(f"reCAPTCHA verification response: {verify_response}")
        
        if not verify_response.get('success', False):
            current_app.logger.error(f"reCAPTCHA verification failed: {verify_response}")
            abort(401, description="reCAPTCHA verification failed")
            
    except Exception as e:
        current_app.logger.error(f"reCAPTCHA error: {str(e)}")
        abort(401, description="Error verifying reCAPTCHA")