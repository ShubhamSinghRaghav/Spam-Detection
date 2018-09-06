#from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls import url
#from django.urls import path
from Detector import views as detector_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'SpamDetector.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #path('admin/', admin.site.urls),
    #path('', detector_views.index, name='index') ,
	url(r'^admin/', admin.site.urls),
    url(r'^$', detector_views.index, name='index') ,

]
