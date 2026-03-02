from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..database.connection import get_db_session
from ..database.crud import UserCRUD
from ..models.user import User, UserBase, UserResponse
from ..utils.auth import hash_password

router = APIRouter()


def get_user_crud(session: Session = Depends(get_db_session)):
    return UserCRUD(session)


@router.post("/user/create", tags=["User"], response_model=UserResponse)
async def create_user(user: UserBase, crud: UserCRUD = Depends(get_user_crud)):
    # Hash password
    hashed_password = hash_password(user.password)
    user_data = UserBase(username=user.username, password=hashed_password)
    return crud.create_user(user_data)


@router.get("/user/list", tags=["User"], response_model=list[UserResponse])
def list_users(crud: UserCRUD = Depends(get_user_crud)):
    return crud.get_all_users()
