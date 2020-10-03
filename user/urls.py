from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/user$', views.UserRegister,name='User_Register'),
    url(r'^/user/auth',views.UserLogin,name='User_Login'),
    url(r'^sites/list/(?P<user>=[\w.@+-]+)$', views.ShowUserNote, name='ShowUserNote'),
    url(r'^sites/(?P<user>=[\w.@+-]+)$', views.SaveUserNote, name='SaveUserNote'),
]
