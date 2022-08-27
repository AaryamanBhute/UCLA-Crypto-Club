from django.urls import path, re_path, include
from django.shortcuts import redirect
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	re_path(r'accounts/social/.*', views.somethingWentWrong, name='somethingwentwrong'),
	path('accounts/', include('allauth.urls')),
	path('home', lambda request: redirect('/', permanent=True)),
	path('portfolio', views.portfoliopage, name="portfolio"),
	path('leadership', views.leadershippage, name="leadership"),
	path('leaderboards', views.leaderboardpage, name="leaderboards"),
	path('start', views.startpage, name="start"),
	path('about', views.aboutpage, name="about"),
	path('logout', views.logoutpage, name="logout"),
	path('loginattempt', views.attemptedlogin, name="attemptedlogin"),
	path('updatesettings/<str:settings>', views.accountSettings, name="updatesettings"),
	path('sell/<str:searchid>/<str:amount>', views.attemptSell, name="attemptSell"),
	path('buy/<str:searchid>/<str:amount>', views.attemptBuy, name="attemptBuy"),
	path('search/<str:term>', views.searchCryptos, name="searchCryptos"),
	path('search/history/<str:id>/<str:ti>/<str:interval>', views.getPriceHistory, name="priceHistory"),
]