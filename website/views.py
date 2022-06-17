from cmath import log
from django.shortcuts import redirect, render
from django.contrib.auth import logout as lout

def logoutInvalids(request):
    if(not request.user.is_authenticated):
        return
    print(request.user.email)
    if(request.user.email.find("ucla.edu") == -1):
        lout(request)

# Create your views here.
def home(request):
    logoutInvalids(request)

    #redirects lead to the home page, manage popup to inform user of the action that just occured
    try:
        popup = request.session['popup']
    except:
        popup = None
    request.session['popup'] = None

    return(render(request, 'website/home.html', {'popup': popup}))

def forums(request):
    logoutInvalids(request)
    return(render(request, 'website/forums.html'))

def loginpage(request):
    logoutInvalids(request)
    return(render(request, 'website/login.html'))

def logoutpage(request):
    if(request.user.is_authenticated):
        lout(request)
        request.session['popup'] = "logout"
    else:
        request.session['popup'] = "invalidlogout"
    return(redirect('/'))

def attemptedlogin(request):
    logoutInvalids(request)
    if(request.user.is_authenticated):
        request.session['popup'] = "login"
    else:
        request.session['popup'] = "invalidlogin"
    return(redirect('/'))