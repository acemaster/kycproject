from django.conf.urls import include, url
from main import views

urlpatterns = [
	url(r'^$',views.home),
	url(r'^signup/$',views.signup),
	url(r'^signin/$',views.signin),
	url(r'^signout/$',views.signout),
	url(r'^uploadprints/$',views.uploadpaper),
	url(r'^dashboard/$',views.dashboard),
	url(r'^viewuser/(?P<uid>[A-Za-z0-9.-]+)$',views.viewuser),
	url(r'^viewapplication/(?P<aid>[A-Za-z0-9.-]+)$',views.viewapplication),
]