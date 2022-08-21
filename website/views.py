from cmath import log
from django.shortcuts import redirect, render
from django.contrib.auth import logout as lout
from django.conf import settings
from .models import *
from django.utils import timezone
import time
import requests

class Asset:
    def __init__(self, coin=None, amt=None, img=None, val=None):
        self.coin = coin
        self.amt = amt
        self.img = img
        self.val = val

def strToDatetime(s):
    i = s.find("-")
    year = s[:i]
    s = s[i+1:]
    i = s.find("-")
    month = s[:i]
    s = s[i+1:]
    i = s.find(" ")
    day = s[:i]
    s = s[i+1:]
    i = s.find(":")
    hour = s[:i]
    s = s[i+1:]
    i = s.find(":")
    minute = s[:i]
    s = s[i+1:]
    second = s
    try:
        second = second[:second.find(".")]
    except:
        pass
    return(datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), 0))

def timeSinceLastAccess():
    time = LastApiAccess.objects.all()[0]
    last_access = str(time.time)
    last_access = last_access[:last_access.find("+")]
    now = str(timezone.now())
    now = now[:now.find("+")]
    last_access_datetime = strToDatetime(last_access)
    now_datetime = strToDatetime(now)
    tdelta = now_datetime - last_access_datetime
    return(tdelta.total_seconds())

def updateLastAccess():
    time = LastApiAccess.objects.all()[0]
    time.time = timezone.now()
    time.save()

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

def makeDict(request, needsAssetInfo=False):
    user_info = getUserInfo(request)
    try:
        popup = request.session['popup']
    except:
        popup = None
    request.session['popup'] = None
    dic = {'popup': popup}
    if(needsAssetInfo):
        if(user_info != None):
            assets = []
            for e in user_info.assets.split(";"):
                divider = e.find("/")
                assets.append(Asset(e[:divider], e[divider+1:]))
            dic['assets'] = assets
        else:
            dic['assets'] = None
    else:
        dic['assets'] = None
    if(user_info != None):
        dic['anonymous'] = user_info.anonymous
        dic['money'] = user_info.cash
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
    while(timeSinceLastAccess() < 1):
        time.sleep(0.5)
    updateLastAccess()
    if(not request.user.is_authenticated):
        request.session['popup'] = "Log In First!"
        return(redirect('/'))
    dic = makeDict(request, True)
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