from fastapi import Depends
from sqlalchemy.orm import Session 
from pydantic import EmailStr
from email_validator import validate_email, EmailNotValidError

from server.src.database import get_db
import server.src.user.models as user_models
import server.src.auth.exceptions as exceptions
import server.src.auth.utils as utils


def get_user_by_email(db: Session, email: EmailStr):
    user = db.query(user_models.User).filter(user_models.User.email == email).first()
    return user


def get_password_by_email(db: Session, email: EmailStr):
    user = db.query(user_models.User).filter(user_models.User.email == email).first()
    return user.password


def get_current_active_user(db: Session, is_activate: bool):
    user = db.query(user_models.User).filter(user_models.User.is_activate == is_activate).first()
    return user


def check_code(db:Session, verification_code: str):
    user = db.query(user_models.User).filter(user_models.User.verification_code==verification_code).first()
    return user


def authenticate_user(db: Session, email: str, password: str):
    try:
        validation = validate_email(email)
        email = validation.email
    except EmailNotValidError as e:
        raise exceptions.EmailNotValidException()
    
    user = db.query(user_models.User).filter(user_models.User.email == email).first()
    if not user:
        return False
    if not utils.verify_password(password, user.password):
        return False
    return user
    
    