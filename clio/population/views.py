from django.shortcuts import render_to_response
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.encoding import smart_str, smart_unicode
from django.template import RequestContext

from clio.common.models import Location 
from clio.population.forms import MainPopulationQueryForm 
from clio.population.models import PopulationCondition, Occupation, MainDataEntry 


# Ajax call from template picks up matching locations with this function
def locationlookup(request):
    lresults = []
    temp = []
    if request.method == "GET":
        if request.GET.has_key(u'q'):
            value = request.GET[u'q']
            model_results = MainDataEntry.objects.filter(location__name__istartswith="%s" % value).select_related().distinct()
            for x in MainDataEntry.objects.filter(location__name__istartswith=value).distinct():
                if smart_str(x.location.location.name) not in lresults:
                    lresults.append(smart_str(x.location.location.name))
    json = simplejson.dumps(lresults)
    return HttpResponse(json, mimetype='application/json')


# Search function for Population data
@login_required
def popsearch(request):
    if request.GET.get('search'):
        form = MainPopulationQueryForm(request.GET)
        search = request.GET.get('search')

        # ---- Date Filter ----
        start_date = request.GET.get('start_date') 
        end_date = request.GET.get('end_date')
        if start_date == 'None':
            start_date = None
        if end_date == 'None':
            end_date = None

        if 'all_time_frames' not in request.GET and 'page' not in request.GET:
            start_date = "%s-%s-%s" % (request.GET.get('start_date_year'),
                                      request.GET.get('start_date_month'),
                                      request.GET.get('start_date_day'))
            end_date = "%s-%s-%s" % (request.GET.get('end_date_year'),
                                      request.GET.get('end_date_month'),
                                      request.GET.get('end_date_day'))
        if start_date and end_date:
            datefilter = Q(begin_date__range=(start_date,end_date)) | Q(end_date__range=(start_date,end_date))
            results = MainDataEntry.objects.filter(datefilter).select_related().order_by('id')
        else:
            results = MainDataEntry.objects.select_related().order_by('id')


        # **** Not Yet Implemented in the Form ****
        """
        # ---- Source Filter ----
        if request.GET.get('source_type'):
            source_input = request.GET.get('source_type')
            source_filter = Q(source__name__icontains=source_input)
            results = results.filter(source_filter)
        else:
            source_input = None 
        
        # ---- Age Filter ----
        if request.GET.get('minage'):
            minage = request.GET.get('minage')
        else:
            minage = 0
        if request.GET.get('maxage'):
            maxage = request.GET.get('maxage')
        else:
            maxage = 100
        agefilter = Q(age_start__isnull=False) & Q(age_end__isnull=False) & Q(age_start__gte=minage) & Q(age_end__lte=maxage)
        
        # ---- Gender Filter ----
        if request.GET.get('genders'):
            if request.GET.get('genders') == 'e':
                genders = "e"
                genderfilter = ~Q(population_gender='None')
            else:
                genders = request.GET.get('genders')
                genderfilter = Q(population_gender=genders)
        else:
            genders = ""
        """       

        # ---- Location Filter ----
        locations_list = []
        location_results = []
        search_locations = None
        # TODO: Handle for locations *selected* in the form vs ones typed in the search box
        if request.GET.get('locations'):
            search_locations = request.GET.get('locations')
            locations_list = search_locations.split(",")
            for loc in locations_list:
                if len(loc.strip()) > 0:
                    # Need to check this methodology with John/Karim
                    locations = Location.objects.filter(full_name__contains=loc)
                    for y in results.filter(location__in=locations).select_related().order_by('id'):
                        location_results.append(y)
            results = location_results

        # Setup the Paginator 
        paginator = Paginator(results,50)
        try:
            page = request.GET.get('page','1')
        except ValueError:
            page = 1
        try:
            results = paginator.page(page)
        except (EmptyPage, InvalidPage):
            results = paginator.page(paginator.num_pages)

        return render_to_response("population_search_results.html",
            {
                "locations_list":locations_list,
                "search_locations":search_locations,
                "start_date":start_date,
                "end_date":end_date,
                #"source_input":source_input,
                "results":results,
                "search":search,
                "form": form,
                "paginator": paginator,
            },context_instance=RequestContext(request))
    else:
        form = MainPopulationQueryForm() 
        results = []
        locations_list = []
        searchlocations = ""
        startdate = ""
        enddate = ""
        sourceinput = ""
        search = ""
        genders = ""
        minage =""
        maxage = ""
    return render_to_response("population.html",
        {
            "locations_list":locations_list,
            "searchlocations":searchlocations,
            "startdate":startdate,
            "enddate":enddate,
            "sourceinput":sourceinput,
            "genders":genders,
            "minage":minage,
            "maxage":maxage,
            "results":results,
            "search":search,
            "form": form,
        },context_instance=RequestContext(request))
