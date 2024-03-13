from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', include('pages.urls')),
    path('articles/', include('articles.urls')),
]
