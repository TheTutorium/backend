from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import UserManager
from ..models import UserModel
from .Middlewares import authenticate

user_api_router = APIRouter(prefix="/users", tags=["users"])


class WebhookUser(BaseModel):
    object: str
    type: str
    data: Dict[str, Any]


@user_api_router.get("/is-tutor")
async def is_tutor(
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    user = UserManager.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "isTutor": user.is_tutor,
    }


@user_api_router.get("/details", response_model=UserModel.User)
def read_detailed_user(
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    user = UserManager.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_api_router.get("/{user_id}", response_model=UserModel.UserRead)
def read_user(
    user_id: str,
    db: Session = Depends(get_db),
    _: Any = Depends(authenticate),
):
    user = UserManager.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_api_router.get("/", response_model=list[UserModel.User])
def read_users(
    db: Session = Depends(get_db),
    _: Any = Depends(authenticate),
):
    users = UserManager.get_users(db)
    return users


@user_api_router.put("/", response_model=UserModel.User)
def update_user(
    user_update: UserModel.UserUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    updated_user = UserManager.update_user(db, user_id, user_update)
    return updated_user


@user_api_router.post("/webhook")
async def webhook(weebhook_user: WebhookUser, db: Session = Depends(get_db)):
    if weebhook_user.type == "user.created":
        return UserManager.create_user(
            db,
            user=UserModel.UserCreate(
                created_at=datetime.utcnow(),
                email=weebhook_user.data["email_addresses"][0]["email_address"],
                first_name=weebhook_user.data["first_name"],
                id=weebhook_user.data["id"],
                last_name=weebhook_user.data["last_name"],
                profile_pic=weebhook_user.data["profile_image_url"],
                updated_at=datetime.utcnow(),
            ),
        )
    if weebhook_user.type == "user.updated":
        pass
    if weebhook_user.type == "user.deleted":
        pass
