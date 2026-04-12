"""Защищённые роутеры — доступны только аутентифицированным пользователям."""

from fastapi import APIRouter

from ..dependencies import CurrentUser  # type: ignore[import]
from ..models import ItemResponse, UserResponse  # type: ignore[import]

router = APIRouter(tags=["protected"])

# "База данных" элементов (in-memory)
fake_items_db: list[dict] = [
    {"id": 1, "title": "Секретный документ #1", "owner": "alice"},
    {"id": 2, "title": "Секретный документ #2", "owner": "alice"},
    {"id": 3, "title": "Личные заметки", "owner": "bob"},
]


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: CurrentUser) -> UserResponse:
    """Получить информацию о текущем пользователе.

    Этот эндпоинт защищён: FastAPI вызовет get_current_user()
    (через CurrentUser = Annotated[UserInDB, Depends(get_current_user)])
    и вернёт 401 если токен невалиден.
    """
    return UserResponse(
        username=current_user.username,
        is_active=current_user.is_active,
    )


@router.get("/items", response_model=list[ItemResponse])
def read_items(current_user: CurrentUser) -> list[ItemResponse]:
    """Получить список элементов текущего пользователя.

    Каждый пользователь видит только свои элементы (авторизация).
    """
    # Фильтрация по владельцу — простая авторизация
    user_items = [
        item for item in fake_items_db if item["owner"] == current_user.username
    ]
    return [ItemResponse(**item) for item in user_items]
