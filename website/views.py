from cmath import log
from django.shortcuts import redirect, render
from django.contrib.auth import logout as lout
from .models import *

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

# Create your views here.
def home(request):
    logoutInvalids(request)
    user_info = getUserInfo(request)
    #redirects lead to the home page, manage popup to inform user of the action that just occured
    try:
        popup = request.session['popup']
    except:
        popup = None
    request.session['popup'] = None
    dic = {'popup': popup}
    if(user_info != None):
        dic['anonymous'] = user_info.anonymous
    else:
        dic['anonymous'] = None
    return(render(request, 'website/home.html', dic))

def portfoliopage(request):
    logoutInvalids(request)
    user_info = getUserInfo(request)
    try:
        popup = request.session['popup']
    except:
        popup = None
    request.session['popup'] = None
    dic = {'popup': popup}
    if(user_info != None):
        dic['anonymous'] = user_info.anonymous
    else:
        dic['anonymous'] = None
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
    try:
        popup = request.session['popup']
    except:
        popup = None
    request.session['popup'] = None
    dic = {'popup': popup}
    if(user_info != None):
        dic['anonymous'] = user_info.anonymous
    else:
        dic['anonymous'] = None
    return(render(request, 'website/about.html', dic))