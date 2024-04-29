from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.v1.model.user_model import User as UserModel
from app.v1.schema.token_schema import TokenData
from app.v1.utils.settings import Settings

settings = Settings()

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expire

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

# Validar password
def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)

# Encriptar password
def get_password_hash(password):
    return pwd_context.hash(password)

# Obtener usuario de la base de datos
def get_user(username: str):
    return UserModel.filter((UserModel.email == username) | (UserModel.username == username)).first()

# Autenticar el usuario
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
    
# Creando token de acceso
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# generando el token
def generate_token(username, password):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email \username or password",
                            headers={"www-Authenticate": "Bearer"})
    access_token_expires = timedelta(minute=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

# Obteniendo usuario actual
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


