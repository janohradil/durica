from datetime import date
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models.odpoved import Odpoved
from config.database import collection_name, client, db
from schema.schemas import list_serial
from bson import ObjectId


router = APIRouter(tags=["odpovede"])
templates = Jinja2Templates(directory="templates")

@router.get("/odpovede", response_class=HTMLResponse)
async def ziskaj_odpovede(request: Request) -> HTMLResponse:
    """
    Get all responses from the database.
    
    Returns:
        HTMLResponse: A rendered HTML template with the responses.
    """
    try:
        odpovede = list_serial(collection_name.find())
        # print(odpovede)
    except Exception as e:
        print("error", e)
    else:
        return templates.TemplateResponse("odpovede.html", {"request": request, "odpovede": odpovede})


@router.post("/odpovede")
async def posli_odpoved(request: Request):
    data = await request.form()
    fname = data.get("fname")
    lname = data.get("lname")
    comp_name = data.get("comp_name")
    ico =  data.get("ico")
    dic = data.get("dic")
    platca_dph = data.get("platca_dph")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")
    odpoved = Odpoved(fname=fname, 
                      lname=lname, 
                      comp_name=comp_name,
                      ico=ico,
                      dic=dic,
                      platca_dph=platca_dph,
                      phone=phone, 
                      email=email, 
                      message=message, 
                      date=date.today())
    odpoved_id = collection_name.insert_one(odpoved.model_dump())
    return {"id": str(odpoved_id.inserted_id)}


@router.get("/spravy", response_class=HTMLResponse)
async def zobraz_spravy(request: Request):
    """Zobraz všetky správy."""
    odpovede = db.odpovede.find()
    print(odpovede)
    return templates.TemplateResponse("odpovede.html", {"request": request, "odpovede": list_serial(odpovede)})

