from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.conf import settings
from sources.models import *
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext

def open_src_file(request, path, ext):
  file_path = '%s/sources/%s.%s' % (settings.STATIC_ROOT, path, ext)

  #if ext.lower() == "pdf":
  return HttpResponse(open(file_path, 'rb').read(), mimetype='application/pdf')
  #else:

def sourceinfo(request):
	source = request.GET.get('source')

	s = BaseSourceObject.objects.get(pk=int(source))

	return render_to_response("sourceinfo.html",{"source":s},
        context_instance=RequestContext(request))
