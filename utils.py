import jwt
from datetime import datetime, timedelta, timezone
from app_sql.settings.config import TOKEN_EXPIRATION_TIME_MINUTES, ALGORITHM,SECRET_KEY
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
from app_sql.settings.config import SECRET_KEY, ALGORITHM
from app_sql.db.models import User
from app_sql.db.database import Session
#argon2 supports salting - same password differnt hash for users wil be create

#wrapper with dcorator it looses information (name and docstring) hence difficult to 
#investigate any issues to mitigate it we use below lib as best practice everything is passed 
#in the wrapper so we can investigate
from functools import wraps

def auth_user_same_as(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # root and info are positional arguments and kwargs can change
        info = args[1]
        user = get_authenticated_user(info.context)
        uid = kwargs.get('user_id')

        if user.id != uid:
          raise GraphQLError('User is not same, you cannot do')
        
        return func(*args, **kwargs)
    
    return wrapper

def auth_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # root and info are positional arguments and kwargs can change
        info = args[1]
        # we will be validating token by decoding it and JWT not expired
        get_authenticated_user(info.context)
        return func(*args, **kwargs)
    return wrapper

def admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # root and info are positional arguments and kwargs can change
        info = args[1]
        user = get_authenticated_user(info.context)

        if user.role != 'admin':
          raise GraphQLError('only admin has right to add a admin user')
        
        return func(*args, **kwargs)
    
    return wrapper

def get_authenticated_user(context):
    request_object = context.get('request')
    if not request_object:
        raise GraphQLError('Request object is missing in context')

    # Log the headers for debugging
    print("Headers:", request_object.headers)
    
    auth_header = request_object.headers.get('Authorization')

    token = auth_header.split(" ")

    if auth_header and token[0] == 'Bearer' and len(token)==2:
        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], tz=timezone.utc):
                raise GraphQLError('Token expired')
            
            session = Session()
            user = session.query(User).filter(User.email == payload.get('sub')).first()

            if not user:
                raise GraphQLError('Could not authenticate user')
            
            return user
        except jwt.exceptions.PyJWTError:
            raise GraphQLError('Invalid Authentication Token')
        except Exception as e:
            raise GraphQLError('Could not authenticate')
    else:
        raise GraphQLError('Missing Auth token')
    
def generate_token(email):
    #now + token_lifespan
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)

    payload = {
        "sub": email,
        "exp": expiration_time
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def hash_password(pwd):
    ph = PasswordHasher()
    return ph.hash(pwd)

def verify_password(pwd_hash,pwd):
    ph = PasswordHasher()
    try:
        ph.verify(pwd_hash, pwd)
    except VerifyMismatchError:
        raise GraphQLError('Invalid password')
