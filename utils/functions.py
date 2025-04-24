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


def get_color_name(color_code: str):
    from enum import Enum

    class Color(Enum):
        biela   = 'bie'
        hnedá   = 'hne'
        béžová  = 'bez'
        zlatá   = 'zla'
        modrá   = 'mod'
        fialová = 'fia'
        zelená  = 'zel'
        ružová  = 'ruz'
        červená  = 'cer'

    try:
        return Color(color_code)
    except ValueError:
       return Color.biela

def get_image_colors(kod_produktu: str,
                     image_dir: str = 'static/img/produkty',
                     exclude_substr: list[str]=['orig', 'diela', 'tools.png', '.ico', '_z.']
                     ) -> list[str]:
    # List image file paths
    images = os.listdir(image_dir)
    cond = lambda img: not any(substr in img for substr in exclude_substr)
    image_colors = [get_color_name(f"{img[6:9]}") for img in images if cond(img) and kod_produktu in img]
    # print(image_colors)
    return image_colors


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



class Produkt(SQLModel):
    kod: str
    nazov: str
    rozmer: str
    cena: int
    popis: str | None = Field(default=None),
    special_kod: str | None = Field(default=None),
    farby: list[str] | None = Field(default=None),
    # obrazky_orig: list[str] | None = Field(default=None),
    obrazky_male: list[str] | None = Field(default=None)


def cena_na_centy(cena: str) -> int:
    return int(float(cena.replace(',', '.'))*100)


def farba_na_farby(farba: list[str]) -> list[str]:
    # print(farba)
    if farba[0] != '' or len(farba) > 1:
        farby = farba
    else:
        farby = "biela,béžová,zlatá".split(',')
    return farby


def produkty_slovnik(produkty: list[Produkt]) -> dict[str, Produkt]:
    return {produkt.kod: produkt for produkt in produkty}


def kodove_skupiny(produkty: dict[str, Produkt]) -> dict[str, str]:
    return dict(cl = "Celoročné dekoračné nápisy",
                vd = "Spomienkové dekoračné nápisy",
                vn = "Vianočné dekoračné nápisy",
                hu = "Maďarské dekoračné nápisy")


def nacitaj_vsetky_produkty(subor: str = 'produkty.csv') -> list[Produkt]:
    df = pd.read_csv(subor, sep=',', header=0).fillna('')
    # df['farba'] = df['farba'].str.split(',')
    # print(df)
    # print(obrazky)
    produtky = [Produkt(kod=row['kod_produktu'],
                        nazov=row['nazov'],
                        rozmer=row['rozmer'],
                        cena=cena_na_centy(row['cena']),
                        popis=row.get('popis') or None,
                        special_kod=row.get('special_kod') or None,
                        farby = [farba.name for farba in get_image_colors(kod_produktu=row['kod_produktu'])],
                        # obrazky_orig = [f'static/img/produkty/{row["kod_produktu"]}_{farba}.jpg' for farba in get_image_colors(kod_produktu=row['kod_produktu'])],
                        obrazky_male = [f'img/produkty/{row["kod_produktu"]}_{farba.value}_z.jpg' 
                                        for farba in get_image_colors(kod_produktu=row['kod_produktu'])]
                        ) for _, row in df.iterrows()]
    produtky = produkty_slovnik(produtky)
    # pprint(produtky.items())
    return produtky
