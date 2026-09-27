from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from sqlalchemy.orm import Session

import jwt

from jwt.exceptions import InvalidTokenError


from app.database import get_db

from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserResponse,
    Token
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    data: UserCreate,
    db: Session = Depends(get_db)
):

    existing_username = (
        db.query(User)
        .filter(
            User.username == data.username
        )
        .first()
    )

    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    existing_email = (
        db.query(User)
        .filter(
            User.email == data.email
        )
        .first()
    )

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(
            data.password
        )
    )


    db.add(user)

    db.commit()

    db.refresh(user)


    return user


@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.username == form_data.username
        )
        .first()
    )


    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )


    if not verify_password(
        form_data.password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )


    access_token = create_access_token(
        {
            "sub": str(user.id),
            "username": user.username
        }
    )


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials"
    )


    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except InvalidTokenError:

        raise credentials_exception


    user = (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )


    if user is None:
        raise credentials_exception


    return user


@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(
        get_current_user
    )
):

    return current_user