import site, os

site.addsitedir('/home/ubuntu/clio/lib/python2.7/site-packages/')
site.addsitedir('/home/ubuntu/clio/')
site.addsitedir('/home/ubuntu/clio/clio')
os.environ['DJANGO_SETTINGS_MODULE'] = 'clio.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
