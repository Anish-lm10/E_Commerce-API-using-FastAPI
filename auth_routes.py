from fastapi import APIRouter, Depends
from typing import Annotated
from datetime import timedelta, datetime
from database import SessionLocal, engine
from schemas import SignupModel, LoginModel, Token
from models import User
from fastapi import HTTPException, status
from werkzeug.security import check_password_hash, generate_password_hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


session = SessionLocal(bind=engine)

SECRET_KEY = "d0b280fd3f8778bdb5d6eda8d740d4c841367990114d8202ecea21ccec88c45e"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# dependencies
db_dependency = Annotated[Session, Depends(get_db)]


# Sign up Starts
@auth_router.post(
    "/signup", response_model=SignupModel, status_code=status.HTTP_201_CREATED
)
async def signup(user: SignupModel):
    """
    ## Registrating a User
    This requires following
    - "username": Integer
    - "email": String
    - "password": String
    - "is_active": Boolean
    - "is_staff": Boolean
    """

    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already Exists"
        )

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username Already Exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    session.add(new_user)
    session.commit()
    return new_user


# SignUp Ends


# Token route and login starts (JWT)
@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    ## Login and generates Token
    This field requires
    - username:String
    - password: String
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not Validate User"
        )

    token = create_access_token(user.username, user.u_id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(username: str, password: str):
    db_user = session.query(User).filter(User.username == username).first()
    if db_user and check_password_hash(db_user.password, password):
        return db_user
    return None


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate"
        )


# Token route and login ends

user_dependency = Annotated[dict, Depends(get_current_user)]


@auth_router.get("/")
async def hello_auth(user: user_dependency):
    """
    ## Sample hello
    This is to check routes
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed"
        )
    return {"message": "hello auth"}
