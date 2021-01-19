####################################################################################
### Anggi Agista
### email : agista.mailrespon@gmail.com
#####################################################################################
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('netto/', include('netto.urls')),
    path('', views.home),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]

urlpatterns += staticfiles_urlpatterns()