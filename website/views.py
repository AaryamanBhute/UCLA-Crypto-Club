from cmath import log
from django.shortcuts import redirect, render
from django.contrib.auth import logout as lout
from django.conf import settings
from .models import *
import pyEX as p

class Asset:
    def __init__(self, coin=None, amt=None, img=None, val=None):
        self.coin = coin
        self.amt = amt
        self.img = img
        self.val = val

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

def makeDict(request):
    user_info = getUserInfo(request)    
    try:
        popup = request.session['popup']
    except:
        popup = None
    request.session['popup'] = None
    dic = {'popup': popup}
    if(user_info != None):
        assets = []
        for e in user_info.assets.split(";"):
            divider = e.find("/")
            #coin = e[:divider]
            #print(coin)
            #d = settings.IEX.quote(symbol=coin)
            assets.append(Asset(e[:divider], e[divider+1:]))
        dic['anonymous'] = user_info.anonymous
        dic['money'] = user_info.cash
        dic['assets'] = assets
    else:
        dic['anonymous'] = None
        dic['money'] = None
        dic['assets'] = None
    return(dic)

# Create your views here.
def home(request):
    logoutInvalids(request)
    dic = makeDict(request)
    return(render(request, 'website/home.html', dic))

def portfoliopage(request):
    logoutInvalids(request)
    dic = makeDict(request)
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
    print(user_info.anonymous)
    return(redirect('/'))

def about(request):
    logoutInvalids(request)
    user_info = getUserInfo(request)
    #redirects lead to the home page, manage popup to inform user of the action that just occured
    dic = makeDict(request)
    return(render(request, 'website/about.html', dic))