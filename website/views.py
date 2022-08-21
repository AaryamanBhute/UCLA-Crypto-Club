from cmath import log
from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth import logout as lout
from django.templatetags.static import static
from django.conf import settings
from .models import *
from django.utils import timezone
import time
import requests

TopCryptos = [('bitcoin', 'BTC'), ('ethereum', 'ETH'), ('tether', 'USDT'), ('cardano', 'ADA'), ('xrp', 'XRP'), ('solana', 'SOL')]

class Asset:
    def __init__(self, name=None, amt=None, symbol=None, img=None, val=None):
        self.symbol = symbol
        self.amt = amt
        self.img = img
        self.val = val
        self.name = name

class BuyOption:
    def __init__(self, name=None, symbol=None, img=None, price=None):
        self.symbol = symbol
        self.img = img
        self.price = price
        self.name = name

def logoutInvalids(request):
    if(not request.user.is_authenticated):
        return
    if(request.user.email.endswith("ucla.edu") == False):
        lout(request)

def getUserInfo(request):
    if(not request.user.is_authenticated):
        return(None)
    try:
        user_info = UserInfo.objects.get(email__exact=request.user.email)
    except:
        user_info = UserInfo.objects.create_user_info(request.user.email)
    return(user_info)

def getInfo(name):
    r = requests.get("http://api.coincap.io/v2/assets/{n}".format(n=name)).json()
    return(r)
def getInfos(names):
    r = requests.get("http://api.coincap.io/v2/assets?ids={n}".format(n=",".join(names))).json()
    return(r)

def floatToStr(val):
    val = str(val)
    ind = val.find(".")
    counter = 0
    while(ind > 0):
        if(counter == 3):
            counter = 0
            val = val[:ind] + "," + val[ind:]
        ind -= 1
        counter += 1
    return(val)

def makeDict(request, needsAssetInfo=False, needsTopCryptoInfo=False):
    user_info = getUserInfo(request)
    try:
        popup = request.session['popup']
    except:
        popup = None
    request.session['popup'] = None
    dic = {'popup': popup}
    if(needsAssetInfo):
        if(user_info != None):
            totalAssetValue = 0
            assets = []
            for e in user_info.assets.split(";"):
                divider = e.find("/")
                assets.append(Asset(e[:divider], int(e[divider+1:])))
            infos = getInfos([asset.name for asset in assets])['data']
            for i in range(0, len(assets)):
                asset = assets[i]
                inf = None
                for d in infos:
                    if(d['id'] == asset.name):
                        inf = d
                        break
                if(inf == None):
                    asset.symbol = "err"
                    asset.val = "err"
                    asset.img = static("website/images/icon/{s}.png".format(s=asset.symbol.lower()))
                    continue
                asset.symbol = inf['symbol']
                val = str(asset.amt * round(float(inf['priceUsd']), 2))
                totalAssetValue += float(val)
                val = val[:val.find(".")+3]
                asset.val = floatToStr(val)
                asset.img = static("website/images/icon/{s}.png".format(s=asset.symbol.lower()))
            dic['assets'] = assets
            tAV = floatToStr(totalAssetValue)
            dic['totalAssetValue'] = tAV[:tAV.find(".")+2]
            portfolioValue = floatToStr(user_info.cash + totalAssetValue)
            dic['portfolioValue'] = portfolioValue[:portfolioValue.find(".")+2]
        else:
            dic['assets'] = None
            dic['totalAssetValue'] = None
            dic['portfolioValue'] = None
    else:
        dic['assets'] = None
    if(needsTopCryptoInfo):
        topCryptos = []
        info = getInfos([crypto[0] for crypto in TopCryptos])['data']
        for crypto in TopCryptos:
            inf = None
            for d in info:
                if(d['id'] == crypto[0]):
                    inf = d
                    break
            if(inf != None):
                topCryptos.append(BuyOption(crypto[0], crypto[1], static("website/images/icon/{s}.png".format(s=crypto[1].lower()))))
                try:
                    v = inf['priceUsd']
                    topCryptos[-1].val = v[:v.find(".") + 3]
                except:
                    topCryptos[-1].val = "ERR"
        dic['topCryptos'] = topCryptos
    else:
        dic['topCryptos'] = None
    if(user_info != None):
        dic['anonymous'] = user_info.anonymous
        dic['money'] = floatToStr(round(float(user_info.cash), 2))
    else:
        dic['anonymous'] = None
        dic['money'] = None
    return(dic)

# Create your views here.
def home(request):
    logoutInvalids(request)
    dic = makeDict(request)

    return(render(request, 'website/home.html', dic))

def portfoliopage(request):
    logoutInvalids(request)
    if(not request.user.is_authenticated):
        request.session['popup'] = "Log In First!"
        return(redirect('/'))
    dic = makeDict(request, True, True)
    return(render(request, 'website/portfolio.html', dic))

def logoutpage(request):
    if(request.user.is_authenticated):
        lout(request)
        request.session['popup'] = "Logged Out!"
    else:
        request.session['popup'] = "Invalid Logout!"
    return(redirect('/'))

def attemptedlogin(request):
    logoutInvalids(request)
    if(request.user.is_authenticated):
        request.session['popup'] = "Logged In!"
    else:
        request.session['popup'] = "Invalid Login!"
    return(redirect('/'))

def somethingWentWrong(request):
    request.session['popup'] = "Something Went Wrong, Try Again!"
    return(redirect('/'))

def accountSettings(request, settings):
    logoutInvalids(request)
    user_info = getUserInfo(request)
    if(not request.user.is_authenticated):
        return(redirect('/'))
    new_settings = settings.split(";")
    if(new_settings[0] == 'false'):
        user_info.anonymous = False
    else:
        user_info.anonymous = True
    user_info.save()
    request.session['popup'] = "Updated Settings!"
    return(redirect('/'))

def about(request):
    logoutInvalids(request)
    user_info = getUserInfo(request)
    #redirects lead to the home page, manage popup to inform user of the action that just occured
    dic = makeDict(request)
    return(render(request, 'website/about.html', dic))