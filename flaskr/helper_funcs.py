from .models import SiteUser
from flask import flash

def validate_unique_credentials(user:SiteUser) -> bool:
    answer = True
    matching_name_user = SiteUser.objects(name=user.name).first()
    if matching_name_user and matching_name_user.id != user.id:
        flash('Name already in use', 'error')
        answer = False
    
    matching_email_user = SiteUser.objects(address=user.address).first()
    if matching_email_user and matching_email_user.id != user.id:
        flash('Email already in use', 'error')
        answer = False
    
    return answer

#?------------------------------------------------------------

from base64 import b64encode
from werkzeug.utils import secure_filename
from os import path

def create_Base64_image_str(f) -> str: 
    filename = secure_filename(f.filename)
    base64_data = b64encode(f.read()).decode("utf-8")
    
    extension = path.splitext(filename)[1][1:]
    content_type = f"image/{extension}"
    return f"data:{content_type};base64,{base64_data}"

#?------------------------------------------------------------

from typing import Union
from flaskr import bcrypt

def encrypt_user_psw(psw:Union[str, None]) -> Union[str, None]:
    if psw: return bcrypt.generate_password_hash(psw).decode('utf-8')

#?------------------------------------------------------------

from flaskr import bcrypt

def check_psw(encrypted_psw: str, unencrypted_psw: str) -> bool:
    return bcrypt.check_password_hash(encrypted_psw, unencrypted_psw)