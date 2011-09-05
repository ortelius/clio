import csv

from django.shortcuts import render_to_response
from django.db.models import Q
from django.http import *
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import simplejson
from django.utils.encoding import smart_str, smart_unicode
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from government.models import *
from government.forms import GovernmentSearchForm

# Ajax call from template picks up matching locations with this function
def locationlookup(request):
    lresults = []
    temp = []
    if request.method == "GET":
        if request.GET.has_key(u'q'):
            value = request.GET[u'q']
            locations = Location.objects.filter(full_name__istartswith=value).distinct().values('name').order_by('name')
            for x in locations:
                lresults.append(x['name'])
    json = simplejson.dumps(lresults)
    return HttpResponse(json, mimetype='application/json')

# Search function for Government/Politics data
@login_required
def govtsearch(request):

    if request.GET.get('search'):
        form = GovernmentSearchForm(request.GET)
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

        # ---- Source Filter
        """
        if request.GET.get('sourceinput'):
            sourceinput = request.GET.get('sourceinput')
        else:
            sourceinput = ""
        """

        # ---- Location Filter ----
        locations_list = []
        location_results = []
        search_locations = None
        # TODO: Handle for locations *selected* in the form vs ones typed in the search box
        locations = request.GET.get('locations')
        if locations == 'None':
            locations = None
        if locations:
            search_locations = request.GET.get('locations')
            locations_list = search_locations.split(",")
            for loc in locations_list:
                if len(loc.strip()) > 0:
                    # Need to check this methodology with John/Karim
                    locations = Location.objects.filter(full_name__contains=loc)
                    for y in results.filter(location__in=locations).select_related().order_by('id'):
                        location_results.append(y)
            results = location_results

        """
        # check if they want to limit by any of the other fields:
        if request.GET.getlist('continent')[0] != '':
            print "Limiting by continent"
            results = results.filter(location__location__geographically_in__name__in=request.GET.getlist('continent'))

        if request.GET.getlist('empire')[0] != '':
            print "Limiting by empire"
            results = results.filter(location__location__pk__in=request.GET.getlist('empire'))

        if request.GET.getlist('nation_state')[0] != '':
            print "Limiting by nation_state"
            print request.GET.getlist('nation_state')
            results = results.filter(location__location__pk__in=request.GET.getlist('nation_state'))

        if request.GET.getlist('semi_sovereign')[0] != '':
            print "Limiting by semi_sveriegn"
            results = results.filter(location__location__pk__in=request.GET.getlist('semi_sovereign'))

        if request.GET.getlist('non_sovereign')[0] != '':
            print "Limiting by non_sveriegn"
            results = results.filter(location__location__pk__in=request.GET.getlist('non_sovereign'))
        """
    
        result_start_date = None
        result_end_date = None

        #result_start_date = results.order_by('begin_date')[0].begin_date
        #result_end_date = results.order_by('end_date')[0].begin_date

        print result_start_date

        if 'export' in request.GET:
            if request.GET.get('export') == 'CSV':
                # Create the HttpResponse object with the appropriate CSV header.
                response = HttpResponse(mimetype='text/csv')
                response['Content-Disposition'] = 'attachment; filename=politic_results.csv'
                writer = csv.writer(response)
                writer.writerow(['ID', 'Source', 'Begin Date', 'End Date', 'Location'])
                for result in results:
                    print result.pk
                    writer.writerow([result.pk, result.source, result.begin_date, result.end_date, result.location])

                return response

        paginator = Paginator(results,20)
        try:
            page = request.GET.get('page','1')
        except ValueError:
            page = 1
        try:
            results = paginator.page(page)
        except (EmptyPage, InvalidPage):
            results = paginator.page(paginator.num_pages)

        return render_to_response("government_search_results.html",
            {
                "result_start_date": result_start_date,
                "result_end_date": result_end_date,
                "locations_list":locations_list,
                "search_locations":search_locations,
                "start_date":start_date,
                "end_date":end_date,
                #"source_input":source_input,
                "results":results,
                "search":search,
                "form": form,
                "paginator": paginator,
                "dataset": request.GET.get('dataset'),
                "show_continent": 'continent' in request.GET,
                "show_remarks": 'remarks' in request.GET,
                "show_confederation": 'confederation' in request.GET,
                "show_country_codes": 'country_codes' in request.GET,
                "show_placename": 'placename' in request.GET,
                "show_alternate_placenames": 'alternate_placenames' in request.GET,
                "show_uncertainty": 'uncertainty' in request.GET,
            },context_instance=RequestContext(request))

    else:
        form = GovernmentSearchForm()
        results = []
        locations_list = []
        searchlocations = ""
        startdate = ""
        enddate = ""
        sourceinput = ""
        search = ""


    return render_to_response("government.html",
        {
            "locations_list":locations_list,
            "searchlocations":searchlocations,
            "startdate":startdate,
            "enddate":enddate,
            "sourceinput":sourceinput,
            "results":results,
            "search":search,
            "form": form,
        },context_instance=RequestContext(request))
