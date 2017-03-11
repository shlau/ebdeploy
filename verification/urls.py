from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^login$', views.login_view, name='login'),
        url(r'^logout$', views.logout, name='logout'),
        url(r'^loggedin$', views.loggedin, name='loggedin'),
        url(r'^register/$', views.register, name='register'),
        url(r'^register/complete$', views.registration_complete, name='registration_complete'),
        url(r'^homepage$', views.homepage, name='homepage'),
]
