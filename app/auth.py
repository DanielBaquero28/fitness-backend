from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import database, models
from dotenv import load_dotenv
from app.database import get_db

from app.settings import settings

# Load env variables
load_dotenv()

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT config
#SECRET_KEY = os.getenv("SECRET_KEY", "myultrasecretkey123")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# OAuth2 token extractor
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Hash plain-text password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT token generation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def get_current_user(
        token: str = Security(oauth2_scheme),
        db: Session = Depends(get_db)
):
    print("Here 2")
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )

    print(f"\n--. Incoming Token ---\n{token}\n")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded Payload: {payload}")        

        username : str = payload.get("sub")
        print(f"Extracted Username from Token: {username}")

        # Doesn't specifiy a username
        if username is None:
            print("Username not found in token payload!")
            raise credentials_exception
    except JWTError as e:
        print(f"JWT Decode Error: {e}")
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == username).first()

    # Doesn't exist the user in the database
    if user is None:
        print(f"No user found in database for username: {username}")
        raise credentials_exception
    
    print(f"User found in database: {user.username}")
    return user