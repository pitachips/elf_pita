"""elf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from legolas import views


from django.conf.urls import patterns, url



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),

    ## store 관련 url
    url(r'^store_list/$', views.store_list, name='store_list'),
    url(r'^store_detail/(?P<pk>[0-9]+)/$', views.store_detail, name='store_detail'),
    url(r'^store_detail/(?P<pk>[0-9]+)/menu/$', views.store_menu, name='store_menu'),
    url(r'^store_new/$', views.store_new, name='store_new'),
    url(r'^store_edit/(?P<pk>[0-9]+)/$', views.store_edit, name='store_edit'),

    ## review 관련 url
    url(r'^store/(?P<store_id>[0-9]+)/review_new/$', views.review_new, name='review_new'),
    url(r'^store/(?P<store_id>[0-9]+)/review_edit/(?P<review_id>[0-9]+)$', views.review_edit, name='review_edit'),

    ##comment 관련 url
    url(r'store/(?P<store_id>[0-9]+)/review/(?P<review_id>[0-9]+)/comment_new/$', views.comment_new, name='comment_new'),

    # accounts 관련 url include
    url(r'^accounts/', include('accounts.urls')),


    #업체엑셀정보 import를 위한 url
    #url(r'^import_sheet/', views.import_sheet, name="import_sheet"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
