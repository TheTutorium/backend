from typing import Any, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import UserManager
from ..models import UserModel
from ..utils.Middleware import authenticate

user_api_router = APIRouter(prefix="/users", tags=["users"])


class WebhookUser(BaseModel):
    object: str
    type: str
    data: Dict[str, Any]


@user_api_router.get("/all-tutors/", response_model=list[UserModel.PublicUserRead])
def get_all_tutors(
    db: Session = Depends(get_db),
    _: Any = Depends(authenticate),
):
    return [_aggregate(db, tutor=tutor) for tutor in UserManager.get_all_tutors(db)]


@user_api_router.get("/detailed/", response_model=UserModel.UserRead)
def get_detailed(
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return UserManager.get(db, user_id=user_id)


@user_api_router.get("/is-tutor/", response_model=bool)
async def is_tutor(
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return UserManager.is_tutor(db, user_id=user_id)


@user_api_router.get("/{user_id}/", response_model=UserModel.PublicUserRead)
def get(
    user_id: str,
    db: Session = Depends(get_db),
    _: Any = Depends(authenticate),
):
    user = UserManager.get(db, user_id=user_id)
    return _aggregate(db, tutor=user) if user.is_tutor else user


@user_api_router.put("/", response_model=UserModel.UserRead)
def update(
    user_update: UserModel.UserUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return UserManager.update(db, user_id=user_id, user_update=user_update)


@user_api_router.post("/webhook")
async def webhook(
    weebhook_user: WebhookUser,
    db: Session = Depends(get_db),
):
    if weebhook_user.type == "user.created":
        return UserManager.create(
            db,
            user_create=UserModel.UserCreate(
                description="",
                email=weebhook_user.data["email_addresses"][0]["email_address"],
                first_name=weebhook_user.data["first_name"],
                id=weebhook_user.data["id"],
                is_tutor=False,
                last_name=weebhook_user.data["last_name"],
                profile_pic=weebhook_user.data["profile_image_url"],
            ),
        )
    if weebhook_user.type == "user.updated":
        if weebhook_user.data.get("profile_image_url") is None:
            return
        return UserManager.update(
            db,
            user_id=weebhook_user.data["id"],
            user_update=UserModel.UserUpdate(
                profile_pic=weebhook_user.data["profile_image_url"]
            ),
        )
    if weebhook_user.type == "user.deleted":
        UserManager.delete(db, user_id=weebhook_user.data["id"])


def _aggregate(db: Session, tutor: UserModel.User):
    return UserModel.PublicUserRead(
        **tutor.dict(),
        hours_given=UserManager.get_hours_given_of_tutor(db, tutor_id=tutor.id),
        rating=UserManager.get_rating_of_tutor(db, tutor_id=tutor.id),
    )
