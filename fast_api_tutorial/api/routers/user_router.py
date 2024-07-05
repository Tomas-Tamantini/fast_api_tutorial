from http import HTTPStatus
from fastapi import Depends, APIRouter
from fastapi.exceptions import HTTPException
from fast_api_tutorial.schemas import (
    User,
    CreateUserRequest,
    UserResponse,
    UserListResponse,
)
from fast_api_tutorial.persistence.unit_of_work import UnitOfWork
from fast_api_tutorial.exceptions import (
    NotFoundError,
    DuplicateFieldError,
    UserNotFoundError,
    FieldAlreadyInUseError,
)
from fast_api_tutorial.security import PasswordHasher
from fast_api_tutorial.api.dependencies import (
    get_unit_of_work,
    get_current_user,
    get_password_hasher,
)

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(
    user: CreateUserRequest,
    uow: UnitOfWork = Depends(get_unit_of_work),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
):
    user = user.with_hashed_password(hash_method=password_hasher.hash_password)
    with uow:
        try:
            uow.user_repository.add(user)
            uow.commit()
            return uow.user_repository.get_from_email(user.email)
        except DuplicateFieldError as e:
            raise FieldAlreadyInUseError(e.field)


@user_router.get("/", response_model=UserListResponse)
def get_users(
    page: int = 1, size: int = 5, uow: UnitOfWork = Depends(get_unit_of_work)
):
    with uow:
        return {"users": uow.user_repository.get_paginated(page=page, size=size)}


@user_router.get("/{user_id}/", response_model=UserResponse)
def get_user(user_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    with uow:
        try:
            return uow.user_repository.get(user_id)
        except NotFoundError:
            raise UserNotFoundError()


@user_router.put("/{user_id}/", response_model=UserResponse)
def update_user(
    user_id: int,
    user: CreateUserRequest,
    uow: UnitOfWork = Depends(get_unit_of_work),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not enough permissions to update this user.",
        )
    user = user.with_hashed_password(hash_method=password_hasher.hash_password)
    with uow:
        try:
            uow.user_repository.update(user_id, user)
            uow.commit()
            return uow.user_repository.get(user_id)
        except NotFoundError:
            raise UserNotFoundError()
        except DuplicateFieldError as e:
            raise FieldAlreadyInUseError(e.field)


@user_router.delete("/{user_id}/", status_code=HTTPStatus.NO_CONTENT)
def delete_user(
    user_id: int,
    uow: UnitOfWork = Depends(get_unit_of_work),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not enough permissions to delete this user.",
        )
    with uow:
        try:
            uow.user_repository.delete(user_id)
            uow.commit()
        except NotFoundError:
            raise UserNotFoundError()
