from sqlalchemy.orm import Session
from . import models, schemas

from passlib.context import CryptContext
import secrets
import string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))  # for a 20-character password
    hashed_password = get_password_hash(password)
    db_user = models.User(email=user.email, name=user.name,
                          surname=user.surname, patronymic=user.patronymic,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user, password


def get_register_request(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RegisterRequest).offset(skip).limit(limit).all()


def create_register_request(db: Session, register_request: schemas.RegisterRequestCreate):
    db_register_request = models.RegisterRequest(**register_request.dict())
    db.add(db_register_request)
    db.commit()
    db.refresh(db_register_request)
    return db_register_request


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
