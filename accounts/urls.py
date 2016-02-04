from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import login, logout

from accounts import views
from accounts.forms import LoginForm

urlpatterns = [
    url(r'^signup1/$', views.signup1, name="signup1"),
    url(r'^signup2/$', views.signup2, name="signup2"),
    url(r'^login/$', login, kwargs={'authentication_form': LoginForm, }, name="auth_login"),
    url(r'^logout/$', logout, name="auth_logout"),
    url(r'^profile/$', views.profile, name="core_profile"),


    ## user_detail 관련 url
    url(r'^user_detail/(?P<pk>[0-9]+)/$', views.user_detail, name='user_detail'),
    url(r'^user_detail_follwer/(?P<pk>[0-9]+)/$', views.user_detail_follower, name='user_detail_follower'),
    url(r'^user_detail_following/(?P<pk>[0-9]+)/$', views.user_detail_following, name='user_detail_following'),
    url(r'^user_detail_bookmark/(?P<pk>[0-9]+)/$', views.user_detail_bookmark, name='user_detail_bookmark'),
]