from datetime import datetime, timedelta, timezone
from jose import jwt
import bcrypt

SECRET_KEY = "SUPER_SECRET_WORKER_KEY_2026" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Переводим строки в байты перед сравнением
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def get_password_hash(password: str) -> str:
    # Генерируем соль и хешируем пароль
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Возвращаем как обычную строку, чтобы SQLAlchemy мог сохранить это в БД
    return hashed_bytes.decode('utf-8')