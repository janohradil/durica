from dataclasses import dataclass
import os
from datetime import datetime
from pathlib import Path
from pprint import pprint
import pandas as pd
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Dependency to provide the current year
def get_year():
    """Return the current year as a dictionary."""
    current_year = datetime.now().year
    return {"year": current_year}

def get_image_paths(image_dir: str, exclude_substr: list[str]=['orig', 'diela', 'tools.png', '.ico']):
    # List image file paths
    images = os.listdir(image_dir)
    cond = lambda img: not any(substr in img for substr in exclude_substr)
    image_paths = [f"/static/img/{img}" for img in images if cond(img)]
    return image_paths


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    import re
    import unicodedata
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


class Obrazok(SQLModel):
    name: str
    path: str


class Produkt(SQLModel):
    kod: str
    nazov: str
    rozmer: str
    cena: int
    popis: str | None = Field(default=None)
    obrazok: Obrazok | None = Field(default=None)


def cena_na_centy(cena: str) -> int:
    return int(float(cena.replace(',', '.'))*100)


def produkty_slovnik(produkty: list[Produkt]) -> dict[str, Produkt]:
    return {produkt.kod: produkt for produkt in produkty}


def kodove_skupiny(produkty: dict[str, Produkt]) -> dict[str, str]:
    return dict(cl = "Celoročné dekoračné nápisy",
                vd = "Spomienkové dekoračné nápisy",
                vn = "Vianočné dekoračné nápisy")


def nacitaj_vsetky_produkty(subor: str = 'produkty.csv') -> list[Produkt]:
    df = pd.read_csv(subor, sep=';', header=0)
    produtky = [Produkt(kod=row['kod_produktu'], 
                    nazov=row['nazov'], 
                    rozmer=row['rozmer'], 
                    cena=cena_na_centy(row['cena']),
                    popis=row.get('popis')
                    ) for _, row in df.iterrows()]
    produtky = produkty_slovnik(produtky)
    # pprint(produtky.items())
    return produtky