from cmath import log
from decimal import Decimal
from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth import logout as lout
from django.contrib.auth.models import User
from django.templatetags.static import static
from datetime import datetime
from django.conf import settings
from .models import *
from django.utils import timezone
from django.http import JsonResponse
from .utils import *
import requests
import time

TopCryptos = [('bitcoin', 'BTC'), ('ethereum', 'ETH'), ('tether', 'USDT'), ('cardano', 'ADA'), ('xrp', 'XRP'), ('solana', 'SOL')]

class Asset:
    def __init__(self, name=None, amt=None, symbol=None, img=None, val=None, id=None):
        self.symbol = symbol
        self.amt = amt
        self.img = img
        self.val = val
        self.name = name
        self.id = id

class BuyOption:
    def __init__(self, name=None, symbol=None, img=None, price=None, id=None):
        self.symbol = symbol
        self.img = img
        self.price = price
        self.name = name
        self.id = id

class LeaderboardEntry:
    def __init__(self, name=None, portfolio_value=None):
        self.name = name
        self.portfolio_value = portfolio_value

def logoutInvalids(request):
    if(not request.user.is_authenticated):
        return
    if(request.user.email.endswith("ucla.edu") == False and settings.ALLOWED_EMAILS.find(request.user.email) == -1):
        lout(request)

def getUserInfo(request):
    if(not request.user.is_authenticated):
        return(None)
    try:
        user_info = UserInfo.objects.get(email__exact=request.user.email)
    except:
        user_info = UserInfo.objects.create_user_info(request.user.email)
    return(user_info)

def floatToStr(val):
    return(f'{Decimal(val):,}')

def makeDict(request, needsAssetInfo=False, needsTopCryptoInfo=False, needsLeaderboard=False, needsLeaders=False):
    user_info = getUserInfo(request)
    try:
        popup = request.session['popup']
    except:
        popup = None
    request.session['popup'] = None
    dic = {'popup': popup}
    dic['season_start'] = settings.SEASON_START.strftime("%m/%d/%Y")
    if(needsLeaders):
        leaders = list(Leader.objects.all())
        socials = [leader.socials for leader in leaders]
        for i in range(0, len(socials)):
            socials[i] = socials[i].split(";")
            for x in range(0, len(socials[i])):
                socials[i][x] = socials[i][x].split('\\')
                socials[i][x][0] = static("website/images/socials/" + socials[i][x][0] + ".png")
        print(socials)
        dic['leaders'] = zip(leaders, [static("website/images/leaders/" + leader.name.replace(" ", "").lower() + ".png") for leader in leaders], socials)
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
                topCryptos.append(BuyOption(id = crypto[0], symbol = crypto[1], img=static("website/images/icon/{s}.png".format(s=crypto[1].lower()))))
                try:
                    v = inf['priceUsd']
                    topCryptos[-1].val = floatToStr(round(Decimal(v), 2))
                    topCryptos[-1].name = inf['name']
                except:
                    topCryptos[-1].val = "ERR"
                    topCryptos[-1].name = "ERR"
        dic['topCryptos'] = topCryptos
    if(needsAssetInfo):
        if(user_info != None):
            totalAssetValue = 0
            assets = []
            if(user_info.assets != ""):
                for e in user_info.assets.split(";"):
                    divider = e.find("/")
                    assets.append(Asset(id= e[:divider], amt=Decimal(e[divider+1:])))
            infos = getInfos([asset.id for asset in assets])['data']
            for i in range(0, len(assets)):
                asset = assets[i]
                inf = None
                for d in infos:
                    if(d['id'] == asset.id):
                        inf = d
                        break
                try:
                    asset.name = inf['name']
                    asset.symbol = inf['symbol']
                    val = round(Decimal(asset.amt) * (Decimal(inf['priceUsd'])), 2)
                    totalAssetValue += Decimal(val)
                    val = str(round(val, 2))
                    asset.val = floatToStr(val)
                    asset.img = static("website/images/icon/{s}.png".format(s=asset.symbol.lower()))
                except:
                    asset.symbol = "err"
                    asset.val = "err"
                    asset.img = static("website/images/icon/{s}.png".format(s=asset.symbol.lower()))
                    continue
            dic['assets'] = assets
            symbolsToAmounts = ""
            for asset in assets:
                symbolsToAmounts += asset.symbol + "-" + str(asset.amt) + ";"
            if(len(symbolsToAmounts) > 0):
                symbolsToAmounts = symbolsToAmounts[:len(symbolsToAmounts)-1]
            dic['symbolsToAmounts'] = symbolsToAmounts
            totalAssetValue = round(Decimal(totalAssetValue), 2)
            tAV = floatToStr(totalAssetValue)
            dic['totalAssetValue'] = tAV
            portfolioValue = floatToStr(round(Decimal(user_info.cash), 2) + totalAssetValue)
            dic['portfolioValue'] = portfolioValue
    if(needsLeaderboard):
        dic['minutesTilReset'] = 60 - datetime.utcnow().minute
        dic['secondsTilReset'] = 60 - datetime.utcnow().second
        leaderboardOrder = UserInfo.objects.all().order_by('-leaderboard_portfolio_value')
        leaderboard = []
        rank = None
        for i in range(0, len(leaderboardOrder)):
            if(request.user.is_authenticated):
                if(request.user.email == leaderboardOrder[i].email):
                    rank = i+1
            email = leaderboardOrder[i].email
            if(leaderboardOrder[i].anonymous):
                name = "Anonymous User"
            else:
                user = User.objects.get(email__exact=email)
                name = user.first_name + " " + user.last_name
            leaderboard.append(LeaderboardEntry(name, floatToStr(str(round(leaderboardOrder[i].leaderboard_portfolio_value, 2)))))
        dic['rank'] = rank
        dic['leaderboardOrder'] = leaderboard
        if(user_info != None):
            dic['alltimechange'] = floatToStr(round(user_info.leaderboard_portfolio_value*100/user_info.added_cash, 2)-100)
            phistory = user_info.price_history
            ri = phistory.rfind(";")
            if(ri >= 0):
                tphist = phistory[:ri]
                ri = tphist.rfind(";")
                if(ri >= 0):
                    dic['changesincelast'] = floatToStr(round(user_info.leaderboard_portfolio_value*100/Decimal(tphist[ri+1:]), 2) - 100)
                else:
                    dic['changesincelast'] = dic['alltimechange']
            if('changesincelast' not in dic):
                dic['changesincelast'] = 'N/A'
            phistory = phistory.split(";")
            dic['price_history'] = ";".join([str(round(float(p), 2)) for p in phistory])
    if(user_info != None):
        dic['anonymous'] = user_info.anonymous
        dic['money'] = floatToStr(round(Decimal(user_info.cash), 2))
        if(user_info.light_mode):
            dic['colormode'] = 'light'
        else:
            dic['colormode'] = 'dark'
    else:
        dic['colormode'] = 'dark'
    dic['api_base_url'] = settings.API_BASE_URL
    dic['static_url'] = static("")
    return(dic)

# Create your views here.
def home(request):
    logoutInvalids(request)
    dic = makeDict(request)

    return(render(request, 'website/home.html', dic))

def leaderboardpage(request):
    logoutInvalids(request)
    dic = makeDict(request, needsLeaderboard=True)
    return(render(request, 'website/leaderboards.html', dic))

def startpage(request):
    logoutInvalids(request)
    dic = makeDict(request, needsLeaderboard=True)
    print("here")
    return(render(request, 'website/start.html', dic))

def aboutpage(request):
    logoutInvalids(request)
    dic = makeDict(request)
    return(render(request, 'website/about.html', dic))

def leadershippage(request):
    logoutInvalids(request)
    dic = makeDict(request, needsLeaders=True)
    return(render(request, 'website/leadership.html', dic))

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
        request.session['popup'] = "Invalid Logout"
    return(redirect('/'))

def attemptedlogin(request):
    logoutInvalids(request)
    if(request.user.is_authenticated):
        request.session['popup'] = "Logged In!"
    else:
        request.session['popup'] = "Invalid Login"
    return(redirect('/'))

def somethingWentWrong(request):
    request.session['popup'] = "Something Went Wrong, Try Again"
    return(redirect('/'))

def accountSettings(request, settings):
    logoutInvalids(request)
    user_info = getUserInfo(request)
    if(not request.user.is_authenticated):
        return(redirect('/'))
    new_settings = settings.split(";")
    print(new_settings)
    if(new_settings[0] == 'false'):
        user_info.updateAnonymous(False)
    else:
        user_info.updateAnonymous(True)
    if(new_settings[1] == 'false'):
        user_info.updateLightMode(False)
    else:
        user_info.updateLightMode(True)
    request.session['popup'] = "Updated Settings!"
    return(redirect('/'))

def attemptBuy(request, searchid, amount):
    amount = Decimal(amount)
    logoutInvalids(request)
    if(not request.user.is_authenticated):
        request.session['popup'] = "Log in first"
        return(redirect('/'))
    user_info = getUserInfo(request)
    if(user_info == None):
        request.session['popup'] = "Error occurred while buying"
        return(redirect('/portfolio'))
    i = getInfo(searchid)['data']
    price = Decimal(i['priceUsd'])
    if(price == 0):
        request.session['popup'] = "Couldn't buy that little, try buying more"
        return(redirect('/portfolio'))
    try:
        cost = price * amount
    except OverflowError:
        request.session['popup'] = "Couldn't buy that much, try buying less"
        return(redirect('/portfolio'))
    if(user_info.cash > cost):
        user_info.addCash(-cost)
        if(user_info.assets != ""):
            assets = user_info.assets.split(";")
        else:
            assets = []
        added = False
        for x in range(0, len(assets)):
            asset = assets[x]
            ind = asset.find("/")
            id = asset[:ind]
            a = Decimal(asset[ind+1:])
            if(id == i['id']):
                assets[x] = id + "/" + str(a + amount)
                added = True
                break
        if(not added):
            assets.append(i['id'] + "/" + str(amount))
        assets.sort()
        user_info.updateAssets(";".join(assets))
        request.session['popup'] = "Successful Buy!"
    else:
        request.session['popup'] = "Not enough funds"
    return(redirect('/portfolio'))

def attemptSell(request, searchid, amount):
    amount = Decimal(amount)
    logoutInvalids(request)
    if(not request.user.is_authenticated):
        request.session['popup'] = "Log in first"
        return(redirect('/'))
    user_info = getUserInfo(request)
    if(user_info == None):
        request.session['popup'] = "Error occurred while selling"
        return(redirect('/portfolio'))
    i = getInfo(searchid)['data']
    price = Decimal(i['priceUsd'])
    if(price == 0):
        request.session['popup'] = "Couldn't sell that little, try selling more"
        return(redirect('/portfolio'))
    if(user_info.assets != ""):
        assets = user_info.assets.split(";")
    else:
        assets = []
    for x in range(0, len(assets)):
        asset = assets[x]
        ind = asset.find("/")
        id = asset[:ind]
        a = Decimal(asset[ind+1:])
        if(i['id'] == id):
            if(a >= amount):
                user_info.addCash(amount * price)
                assets[x] = id + "/" + str(a-amount)
            else:
                request.session['popup'] = "Not enough funds"
                return(redirect('/portfolio'))
    nAssets = []
    for asset in assets:
        ind = asset.find("/")
        a = Decimal(asset[ind+1:])
        if(a > 0):
            nAssets.append(asset)
    nAssets.sort()
    user_info.updateAssets(";".join(nAssets))
    request.session['popup'] = "Successful Sell!"
    return(redirect('/portfolio'))    

def findCrypto(term):
    response_data = requests.get((settings.API_BASE_URL + "?search={t}").format(t=term)).json()
    return(response_data)

#REST FEATURES:

def searchCryptos(request, term):
    response_data = requests.get((settings.API_BASE_URL + "?search={t}").format(t=term)).json()
    try:
        for data in response_data['data']:
            break
        return(JsonResponse(response_data))
    except:
        return(JsonResponse({'data' : []}))

def getPriceHistory(request, id, ti, interval):
    t = int(round(time.time() * 1000))
    response_data = requests.get('https://api.coincap.io/v2/assets/{i}/history?interval={inter}&start={s}&end={e}'.format(i=id, inter=interval, s=str(t-int(ti)*3600000), e=str(t))).json()
    try:
        for data in response_data['data']:
            break
        return(JsonResponse(response_data))
    except:
        return(JsonResponse({'data' : []}))