from http import HTTPStatus
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fast_api_tutorial.api.dto import UserResponse, UserListResponse, CreateUserRequest
from fast_api_tutorial.persistence.models import PaginationParameters
from fast_api_tutorial.exceptions import (
    NotFoundError,
    DuplicateFieldError,
    UserNotFoundError,
    FieldAlreadyInUseError,
)
from fast_api_tutorial.api.dependencies import (
    T_UnitOfWork,
    T_CurrentUser,
    T_PasswordHasher,
    T_DeleteAccountAuthorization,
    T_UpdateAccountAuthorization,
)

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(
    user: CreateUserRequest,
    password_hasher: T_PasswordHasher,
    uow: T_UnitOfWork,
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
def get_users(uow: T_UnitOfWork, offset: int = 0, limit: int = 5):
    pagination = PaginationParameters(limit=limit, offset=offset)
    with uow:
        return {"users": uow.user_repository.get_paginated(pagination)}


@user_router.get("/{user_id}/", response_model=UserResponse)
def get_user(user_id: int, uow: T_UnitOfWork):
    with uow:
        try:
            return uow.user_repository.get(user_id)
        except NotFoundError:
            raise UserNotFoundError()


@user_router.put("/{user_id}/", response_model=UserResponse)
def update_user(
    user_id: int,
    user: CreateUserRequest,
    password_hasher: T_PasswordHasher,
    uow: T_UnitOfWork,
    current_user: T_CurrentUser,
    authorization: T_UpdateAccountAuthorization,
):
    if not authorization.has_permission(actor_id=current_user.id):
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
    uow: T_UnitOfWork,
    current_user: T_CurrentUser,
    authorization: T_DeleteAccountAuthorization,
):
    if not authorization.has_permission(actor_id=current_user.id):
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
