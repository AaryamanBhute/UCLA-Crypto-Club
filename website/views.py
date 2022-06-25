from cmath import log
from django.shortcuts import redirect, render
from django.contrib.auth import logout as lout
from .models import *

def logoutInvalids(request):
    if(not request.user.is_authenticated):
        return
    if(request.user.email.endswith("ucla.edu") == False):
        lout(request)

# Create your views here.
def home(request):
    logoutInvalids(request)
    if(request.user.is_authenticated):
        print(request.user.socialaccount_set.all()[0])
    #redirects lead to the home page, manage popup to inform user of the action that just occured
    try:
        popup = request.session['popup']
    except:
        popup = None
    request.session['popup'] = None

    return(render(request, 'website/home.html', {'popup': popup}))

def forums(request, page = None):
    if(page == None):
        return(redirect('/forums/1'))

    logoutInvalids(request)
    nextpage = page + 1

    if(page == 1):
        lastpage = None
    else:
        lastpage = page - 1

    posts = []
    for i in range(page*10-9, page*10 + 1):
        try: 
            posts.append(Post.objects.get(id=i))
        except:
            nextpage = None
            break

    return(render(request, 'website/forums.html', {'page': page}))

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