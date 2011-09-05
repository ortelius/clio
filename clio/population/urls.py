from django.conf.urls.defaults import *

urlpatterns = patterns('clio.population.views',
    # Example:
    # (r'^clio/', include('clio.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^query/download$', 'download_data'),
    (r'^query/', 'query'),
    (r'^$', 'index'),
)

