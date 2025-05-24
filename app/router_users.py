from math import ceil
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.user.service import UserService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/healthcheck")
async def healthcheck():
    return {
        "status": "ok",
    }


@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request, page: int = 1, per_page: int = 10):
    users = await UserService.find_all()
    total_users = len(users)
    total_pages = ceil(total_users / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = users[start:end]
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "users": paginated_users,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_users": total_users,
        },
    )


@router.get("/{user_id:int}/", response_class=HTMLResponse)
async def user(request: Request, user_id: int):
    user = await UserService.find_one_or_none(id=user_id)
    if not user:
        return templates.TemplateResponse(
            "user.html",
            {
                "request": request,
                "user": None,
                "error": "User not found",
            },
        )
    return templates.TemplateResponse(
        "user.html",
        {
            "request": request,
            "user": user,
        },
    )


@router.get("/random/", response_class=HTMLResponse)
async def random_user(request: Request):
    user = await UserService.get_random_user()
    return templates.TemplateResponse(
        "random_user.html",
        {
            "request": request,
            "user": user,
        },
    )
