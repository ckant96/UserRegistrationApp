from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/user$', views.UserRegister,name='User_Register'),
    url(r'^/user/auth',views.UserLogin,name='User_Login'),
    url(r'^sites/list/(?user={})$', views.ShowUserNote, name='ShowUserNote'),
    url(r'^sites/(?user=\d+)$', views.SaveUserNote, name='SaveUserNote'),
]
