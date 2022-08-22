from django.urls import path, re_path, include
from django.shortcuts import redirect
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('about', views.about, name='about'),
	re_path(r'accounts/social/.*', views.somethingWentWrong, name='somethingwentwrong'),
	path('accounts/', include('allauth.urls')),
	path('home', lambda request: redirect('/', permanent=True)),
	path('portfolio', views.portfoliopage, name="portfolio"),
	path('logout', views.logoutpage, name="logout"),
	path('loginattempt', views.attemptedlogin, name="attemptedlogin"),
	path('updatesettings/<str:settings>', views.accountSettings, name="updatesettings"),
	path('search/<str:term>', views.searchCryptos, name="searchCryptos"),
]