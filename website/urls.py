from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('forums/<int:page>', views.forums, name='forums'),
	path('forums/', views.forums, name='forumsbase'),
	path('accounts/', include('allauth.urls')),
	path('login', views.loginpage, name="login"),
	path('logout', views.logoutpage, name="logout"),
	path('loginattempt', views.attemptedlogin, name="attemptedlogin"),
]