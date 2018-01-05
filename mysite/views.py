from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from mysite.utils import *


class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


def json_data(request):
    data_dict = create_data_dict()
    return sql_to_downloadable_json_response(data_dict, 'data')


def initiatives(request):
    initiatives_dict = create_initiatives_dict()
    return JsonResponse(initiatives_dict)


def initiatives_json(request):
    initiatives_dict = create_initiatives_dict()
    return sql_to_downloadable_json_response(initiatives_dict, 'initiatives')


def filtered_initiatives(request):
    initiatives_dict = create_filtered_initiatives_dict()
    return JsonResponse(initiatives_dict)

def filtered_initiatives_json(request):
    initiatives_dict = create_filtered_initiatives_dict()
    return sql_to_downloadable_json_response(initiatives_dict, 'initiatives')


def initiatives_excel(request):
    column_names = ['Name', 'Category', 'Program']
    sql_columns_needed = ('name', 'impact_initiative_type', 'program_affiliation')
    return sql_to_downloadable_csv_response(column_names, sql_columns_needed,
                                            'impact_db.t_impact_initiatives_July2017', 'initiatives')


def contacts(request):
    return JsonResponse(create_contacts_dict())


def contacts_json(request):
    return sql_to_downloadable_json_response(create_contacts_dict(), 'contacts')


def contacts_excel(request):
    column_names = ['Distinct Email', 'Country']
    sql_columns_needed = ('email', 'country')
    return sql_to_downloadable_csv_response(column_names, sql_columns_needed,
                                            'MARKETING_DB.t_all_contacts', 'contacts')


def engagements(request):
    engagements_dict = create_engagements_dict()
    return JsonResponse(engagements_dict)


def engagements_json(request):
    return sql_to_downloadable_json_response(create_engagements_dict(), 'engagements')


def engagements_excel(request):
    column_names = ['Name', 'City', 'Country', 'Event Type']
    sql_columns_needed = ('event_name', 'city', 'country', 'event_type')
    return sql_to_downloadable_csv_response(column_names, sql_columns_needed,
                                            'globalsu_db.t_all_historical_events', 'events')


def community(request):
    community_dict = create_community_dict(create_contacts_dict(), get_engagements())
    return JsonResponse(community_dict)


def community_json(request):
    community_dict = create_community_dict(create_contacts_dict(),
                                           get_engagements())
    return sql_to_downloadable_json_response(community_dict, 'community')


def education(request):
    education_dict = create_education_dict()
    return JsonResponse(education_dict)


def education_json(request):
    return sql_to_downloadable_json_response(create_education_dict(),
                                             'education')


def education_excel(request):
    column_names = ['Program', 'People Educated']
    return dict_to_downloadable_csv_response(
        create_education_dict()['people_educated'], column_names, 'education')


def overview(request):
    return JsonResponse(create_overview_dict())


def overview_json(request):
    return sql_to_downloadable_json_response(create_overview_dict(),
                                             'overview')


def overview_excel(request):
    column_names = ['Metric', 'Value']
    return dict_to_downloadable_csv_response(create_overview_dict(),
                                             column_names, 'overview')

