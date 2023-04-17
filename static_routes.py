from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")
router = APIRouter()

# Redirect root path to "/en"
@router.get("/")
async def root():
    return RedirectResponse(url="/en")

@router.get("/logo")
async def logo():
    return FileResponse("./static/jpeg/logo.png")
@router.get("/road")
async def image_road():
    return FileResponse("./static/jpeg/road.png")

@router.get("/eng_logo")
async def flag_eng():
    return FileResponse("./static/jpeg/eng_logo.png")

@router.get("/it_logo")
async def flag_it():
    return FileResponse("./static/jpeg/it_logo.png")

@router.get("/css")
async def css():
    return FileResponse("./static/file.css")