from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from APP import views
urlpatterns = [
    path('admin/', admin.site.urls),
    #主页
    path('',views.login,name='login'),
    #引入APP的urls
    path('fly/', include(('APP.urls', "fly"), namespace='fly')),
]
