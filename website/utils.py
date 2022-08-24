from datetime import date
from django.conf import settings
import requests

def weeksSinceStart():
    return((date.today()-settings.SEASON_START).days//7)

def getInfo(name):
    r = requests.get((settings.API_BASE_URL + "/{n}").format(n=name)).json()
    return(r)

def getInfos(ids):
    r = requests.get((settings.API_BASE_URL + "?ids={n}").format(n=",".join(ids))).json()
    return(r)