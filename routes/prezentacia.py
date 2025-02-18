from dataclasses import asdict
import os
import shutil
from fastapi import APIRouter, File, Form, HTTPException, Request, Depends, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.route import router
from config.database import client, db, collection_name
from schema.schemas import list_serial, individual_serial_odpoved, individual_serial_portfolio
from datetime import datetime
from utils.functions import get_year, get_image_colors, slugify, nacitaj_vsetky_produkty, kodove_skupiny

router_prezentacia = APIRouter(tags=["prezentacia"])

# Static and template directories
router_prezentacia.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Directory where images are stored
IMAGE_DIR = "static/img"


@router_prezentacia.get("/", response_class=HTMLResponse)
async def home(request: Request, current_year: dict = Depends(get_year)):
    produkty = nacitaj_vsetky_produkty('utils/produkty.csv')
    kod_skupiny = kodove_skupiny(produkty)
    # print(kod_skupiny)
    # for produkt in produkty:
    #     db.produkty.insert_one(asdict(produkt))
    return templates.TemplateResponse("home.html", {"request": request, 
                                                    "produkty": produkty, 
                                                    "kodove_skupiny": kod_skupiny,
                                                    **current_year})


@router_prezentacia.get("/produkt/{prod_id}", response_class=HTMLResponse)
async def produkt_info(request: Request, prod_id: str):
   produkty = nacitaj_vsetky_produkty('utils/produkty.csv')
   produkt = produkty.get(prod_id)
   print(produkt)
   return templates.TemplateResponse("produkt.html", {"request": request, 
                                                      "produkt": produkt})


@router_prezentacia.delete("/produkt/{prod_id}", response_class=HTMLResponse)
async def produkt_info(request: Request, prod_id: str):
   return ""



@router_prezentacia.get("/obrazok/{prod}", response_class=HTMLResponse)
async def obrazok(request: Request, prod: str):
    # Construct the full path to the image
    file_path = f"static/img/produkty/{prod}"
    product = {}
    product['id'] = file_path.rsplit("/", 1)[1]
    product['obrazok'] = file_path
    # print(product_id)
    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")

    # Determine the media type based on the file extension
    _, ext = os.path.splitext(prod)
    media_type = "image/jpeg" if ext.lower() == ".jpg" or ext.lower() == ".jpeg" else "image/png" if ext.lower() == ".png" else "image/gif" if ext.lower() == ".gif" else "application/octet-stream"
    
    return templates.TemplateResponse("obrazok.html", {"request": request, "product": product})


@router_prezentacia.delete("/obrazok/{prod}", response_class=HTMLResponse)
async def obrazok(request: Request, prod: str):
    return "<div class='non-visible'></div>"


@router_prezentacia.get('/vyroba', response_class=HTMLResponse)
async def info_o_vyrobe(request: Request):
    return templates.TemplateResponse("vyroba.html", {"request": request})


@router_prezentacia.get('/o-nas', response_class=HTMLResponse)
async def info_o_vyrobe(request: Request):
    return templates.TemplateResponse("o-nas.html", {"request": request})


@router_prezentacia.get('/kategorie', response_class=HTMLResponse)
async def info_o_vyrobe(request: Request):
    return templates.TemplateResponse("kategorie.html", {"request": request})

@router_prezentacia.get('/kategorie/celorocne', response_class=HTMLResponse)
async def info_o_vyrobe(request: Request):
    return templates.TemplateResponse("kategorie_celorocne.html", {"request": request})

@router_prezentacia.get("/zlavy", response_class=HTMLResponse)
async def zlavy_view(request: Request):
    return templates.TemplateResponse("zlavy.html", {"request": request})


@router_prezentacia.delete("/zlavy", response_class=HTMLResponse)
async def obrazok(request: Request):
    return templates.TemplateResponse("button_zlavy.html", {"request": request})


@router_prezentacia.get("/pouzitie", response_class=HTMLResponse)
async def zlavy_view(request: Request):
    return templates.TemplateResponse("pouzitie.html", {"request": request})


@router_prezentacia.get("/portfolio", response_class=HTMLResponse)
async def portfolio_view(request: Request, current_year: dict = Depends(get_year)):
    """Return the portfolio page."""
    return templates.TemplateResponse("portfolio.html", {"request": request, **current_year})

@router_prezentacia.get("/portfolio_short", response_class=HTMLResponse)
async def portfolio_view(request: Request, current_year: dict = Depends(get_year)):
    """Return the portfolio page."""
    portfolio_data = list_serial(db.portfolio_data.find(), res_func='individual_serial_portfolio')
    # print(portfolio_data)
    return templates.TemplateResponse("portfolio_short.html", {"request": request, "portfolio_data": portfolio_data, **current_year})

@router_prezentacia.get("/portfolio/items", response_class=HTMLResponse)
async def portfolio_items(request: Request, current_year: dict = Depends(get_year)):
    """
    Return the portfolio items page.

    The page displays a list of portfolio items, including images and descriptions.

    The data is currently hard-coded for demonstration purposes. In the future, it
    should be replaced with a database query.
    """
    def remove_before_slash(value):
        if '/' in value:
            return value.split('/', 1)[1]
        return value

    data = list_serial(db.portfolio_data.find(), res_func='individual_serial_portfolio')
    for projekt in data:
        projekt['slug'] = os.path.join('projekty', slugify(projekt['title']))
        db.portfolio_data.update_one({'title': projekt['title']}, {'$set': {'slug': projekt['slug']}})
        projekt['slug_id'] = remove_before_slash(projekt['slug'])
    return templates.TemplateResponse("partials/portfolio_items.html", {"request": request, "portfolio_data": data, **current_year})


@router_prezentacia.get("/projekty/{slug}", response_class=HTMLResponse)
async def projekt(request: Request, slug: str, current_year: dict = Depends(get_year)):
    projekt = individual_serial_portfolio(db.portfolio_data.find_one({'slug': f'projekty/{slug}'}))
    return templates.TemplateResponse("projekt.html", {"request": request, "data": projekt, **current_year})


@router_prezentacia.get("/portfolio/{slug}", response_class=HTMLResponse)
async def projekt(request: Request, slug: str, current_year: dict = Depends(get_year)):
    return templates.TemplateResponse(f"portfolio/{slug}.html", {"request": request, **current_year})

@router_prezentacia.get("/kontakt", response_class=HTMLResponse)
async def contact_view(request: Request, current_year: dict = Depends(get_year)):
    """Return the contact page."""
    return templates.TemplateResponse("kontakt.html", {"request": request, **current_year})

@router_prezentacia.post("/kontakt")
async def kontakt(fname: str = Form(...), lname: str = Form(...), phone: str = Form(...), email: str = Form(...), message: str = Form(...)):
    db.odpovede.insert_one({"fname": fname, 
                            "lname": lname, 
                            "phone": phone, 
                            "email": email, 
                            "message": message, 
                            "date": datetime.now()
                            })
    response_content = f"<p>Ďakujem veľmi pekne {fname} {lname} za zanechanie správy! Vaša správa \"{message}\" bola zaznamenaná.</p><p>telefónne číso: {phone}</p><p>email: {email}</p>"
    return HTMLResponse(content=response_content)


@router_prezentacia.get("/galeria", response_class=HTMLResponse)
async def galeria(request: Request):
    # List image file paths
    images = os.listdir(IMAGE_DIR)
    image_paths = get_image_colors(image_dir=IMAGE_DIR)
    image_paths_carousel = [img for img in image_paths if '_small' not in img]
    print(image_paths_carousel)
    return templates.TemplateResponse("galeria.html", {"request": request, "images": image_paths, "images_carousel": image_paths_carousel})

@router_prezentacia.get("/galeria/items", response_class=HTMLResponse)
async def gallery_items(request: Request):
    images = os.listdir(IMAGE_DIR)
    image_paths = get_image_colors(image_dir=IMAGE_DIR)
    image_paths_carousel = [img for img in image_paths if '_small' not in img]
    # print(image_paths_carousel)
    return templates.TemplateResponse("partials/gallery_items.html", {"request": request, "images": image_paths})

@router_prezentacia.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"{IMAGE_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"info": "Image uploaded successfully"}

