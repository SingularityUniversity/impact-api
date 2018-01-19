from django.db import connection
from django.http import JsonResponse, HttpResponse
import csv
from geopy.geocoders import Nominatim
import json
from os.path import expanduser

cities_json = expanduser('~/src/impact_api/cities.json')


def create_data_dict():
    community_dict = create_community_dict(create_contacts_dict(), get_engagements())
    initiatives_dict = create_initiatives_dict()
    education_dict = create_education_dict()
    data_dict = dict()
    data_dict['education'] = education_dict
    data_dict['community'] = community_dict
    data_dict['initiatives'] = initiatives_dict
    return data_dict


def sql_to_downloadable_json_response(dictionary, filename):
    response = JsonResponse(dictionary)
    response['Content-Disposition'] = 'attachment; filename={}.json'.format(filename)
    return response


def sql_to_downloadable_csv_response(column_names, sql_columns_needed, table_name, filename):
    sql_rows = custom_sql(table_name, sql_columns_needed)
    return generate_excel_response(sql_rows, column_names, filename)


def dict_to_downloadable_csv_response(dictionary, column_names, filename):
    rows = dictionary.items()
    return generate_excel_response(rows, column_names, filename)


def fill_count_dict(tuple_rows, key_column_index):
    count_dict = {}
    for row in tuple_rows:
        if row[key_column_index] in count_dict:
            count_dict[row[key_column_index]] += 1
        else:
            count_dict[row[key_column_index]] = 1
    return count_dict


def test_fill_count_dict():
    tuple_rows = (('1@1.com', 'US'), ('2@1.com', 'CA'), ('3@1.com', 'US'))
    results_dict = fill_count_dict(tuple_rows, 1)
    assert(results_dict == {"US": 2, "CA": 1})


def fill_initiatives_dict(impact_initiatives):
    initiatives_dict = dict()
    initiatives_dict['categories'] = [
        "New Organization",
        "R&D Project",
        "Organizational Innovation",
        "Enacted Policy",
        "Education & Awareness",
        "Mobilized Resources",
    ]

    initiatives_dict['programs'] = [
        "Global Solutions Program",
        "Executive Leadership Program",
        "Executive Programs",
        "Conferences",
        "Summits",
        "Custom Programs",
        "Other"
    ]

    initiatives_dict['records'] = []
    # initiatives_dict['programs'] = []
    # initiatives_dict['categories'] = []

    for initiative in impact_initiatives:
        initiative_dict = dict()

        initiative_dict['name'] = initiative[0]

        try:
            initiative_dict['category'] = initiatives_dict['categories'].index(initiative[1])
        except ValueError:
            # TODO clean this up in database
            # initiatives_dict['categories'].append(initiative[1])
            initiative_dict['category'] = 1 #('Pontos de Memoria', 'R&D', 'Other') change to R&D Project


        try:
            initiative_dict['program'] = initiatives_dict['programs'].index(initiative[2])
        except ValueError:
            #initiatives_dict['programs'].append(initiative[2])
            initiative_dict['program'] = 6


        initiatives_dict['records'].append(initiative_dict)

        initiatives_dict['no_of_initiatives'] = len(initiatives_dict['records'])
        initiatives_dict['no_of_categories'] = len(initiatives_dict['categories'])

    return initiatives_dict


def generate_excel_response(my_list, keys, filename):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(filename)

    writer = csv.writer(response)
    writer.writerow(keys)
    for row in my_list:
        writer.writerow(row)

    return response


def custom_sql(table, columns_needed=()):
    with connection.cursor() as cursor:
        if len(columns_needed) == 0:
            cursor.execute("select * from {}".format(table))
        elif len(columns_needed) == 1:
            cursor.execute("select {} from {}".format(columns_needed[0], table))
        else:
            sql_statement = "select " + columns_needed[0] + ", "

            for col in columns_needed[1:-1]:
                sql_statement += col
                sql_statement += ", "
            sql_statement += columns_needed[-1]
            sql_statement += " from {}".format(table)
            cursor.execute(sql_statement)

        rows = cursor.fetchall()
    return rows


def count_sql(tables):
    count = 0
    with connection.cursor() as cursor:
        for table in tables:
            cursor.execute("select count(*) from {}".format(table))
            count += cursor.fetchone()[0]

    return count


# returns the sum of values in the field of the table specified
def get_sum_of_field_values(table, field):
    with connection.cursor() as cursor:
        cursor.execute("select sum({}) from {}".format(field, table))
        sum_of_values = cursor.fetchone()[0]
    return sum_of_values


def get_engagements():
    engagements_dict = {}
    hq_rows = (('Singularity University HQ', 'Mountain View', 'US'),)
    country_hub_rows = (('Netherlands Hub', 'Eindhoven', 'Netherlands'),
                        ('Denmark Hub', 'Copenhagen', 'Denmark'),)
    chapters_rows = custom_sql('GLOBALSU_DB.t_chapters',
                               ('chapter_name', 'chapter_city', 'chapter_country'))

    events_rows = custom_sql('globalsu_db.t_all_historical_events', ('event_name', 'city', 'country', 'event_type'))
    no_of_chapters = len(chapters_rows)
    no_of_partners = len(country_hub_rows)
    fill_engagements(engagements_dict, hq_rows, 3)
    fill_engagements(engagements_dict, country_hub_rows, 2)
    fill_engagements(engagements_dict, chapters_rows, 1)

    no_of_engagements = fill_engagements(engagements_dict, events_rows, 0)
    # add_cities(engagements_dict)
    return engagements_dict, no_of_engagements, no_of_chapters, no_of_partners


def fill_engagements(engagements_dict, rows, location_code):
    no_of_engagements = count_sql(['globalsu_db.t_all_historical_events'])

    for row in rows:
        engagement = dict()
        engagement['name'] = row[0]
        engagement['city'] = row[1]
        if len(row) > 2:
            engagement['country'] = row[2]
        else:
            engagement['country'] = 'US'
        add_lat_and_long(engagement)
        if row[1] in engagements_dict:
            engagements_dict[row[1]]['engagements'].append(location_code)
        else:
            engagements_dict[row[1]] = engagement
            engagements_dict[row[1]]['engagements'] = [location_code]
    return no_of_engagements


def create_engagements_dict():
    return get_engagements()[0]


def create_initiatives_dict():
    impact_rows = ('name', 'impact_initiative_type', 'program_affiliation')

    impact_initiatives = custom_sql('impact_db.t_impact_initiatives_July2017', impact_rows)

    return fill_initiatives_dict(impact_initiatives)


def create_education_dict():
    education_dict = dict()
    attendee_field = 'total_attendees'
    education_dict['people_educated'] = {
            "Executive Programs": get_sum_of_field_values('analysis_db.t_ep_headcounts', attendee_field),
            "Global Solutions Program": get_sum_of_field_values('analysis_db.t_gsp_headcounts', attendee_field),
            "Summits": get_sum_of_field_values('analysis_db.t_international_summits_headcounts', attendee_field),
            "Conferences": get_sum_of_field_values('analysis_db.t_conferences_headcounts', attendee_field),
            "Custom Programs": get_sum_of_field_values('analysis_db.t_customs_headcounts', attendee_field),
            "Executive Leadership Program": get_sum_of_field_values('analysis_db.t_elp_headcounts', attendee_field),
          }
    education_dict['total_educated'] = sum(education_dict['people_educated'].values())
    return education_dict


def create_overview_dict():
    community_dict = create_community_dict(create_contacts_dict(), get_engagements())
    initiatives_dict = create_initiatives_dict()
    education_dict = create_education_dict()
    overview_dict = dict()
    overview_dict['no_of_people'] = community_dict['no_of_people']
    overview_dict['no_of_chapters'] = community_dict['no_of_chapters']
    overview_dict['no_of_locations'] = community_dict['no_of_locations']
    overview_dict['no_of_engagements'] = community_dict['no_of_engagements']
    overview_dict['total_educated'] = education_dict['total_educated']
    overview_dict['no_of_initiatives'] = initiatives_dict['no_of_initiatives']
    overview_dict['no_of_categories'] = initiatives_dict['no_of_categories']
    return overview_dict


def create_community_dict(contacts_dict, engagements_tuple):
    community_dict = dict()
    engagements_dict = engagements_tuple[0]
    no_of_engagements = engagements_tuple[1]
    # TODO clean up chapters data
    no_of_chapters = engagements_tuple[2]
    no_of_chapters = 73
    no_of_partners = engagements_tuple[3]

    community_dict['country_communities'] = contacts_dict
    community_dict['engagements'] = {}
    community_dict['engagements']['locations'] = []
    for engagement in engagements_dict.values():
        community_dict['engagements']['locations'].append(engagement)
    community_dict['engagements']['categories'] = ("Event", "Chapter",
                                                   "Regional Partnership", "Headquarters")
    community_dict['no_of_people'] = get_total_no_of_contacts()
    community_dict['no_of_chapters'] = no_of_chapters

    community_dict['no_of_locations'] = 1 + no_of_partners + no_of_chapters
    community_dict['no_of_engagements'] = no_of_engagements

    return community_dict


def add_lat_and_long(engagement):
    with open(cities_json) as json_data:
        cities = json.load(json_data)
    if engagement['country'] and engagement['city']:
        location_name = engagement['city'] + ', ' + engagement['country']
    elif engagement['city']:
        location_name = engagement['city']
    else:
        location_name = "Mountain View, US"
    try:
        city = cities[location_name]
        engagement['lat'] = city['lat']
        engagement['lon'] = city['lon']
    except KeyError:

        # if city name not found, Assign the event to mountain view location for now
        # print('city not found: ', location_name)
        engagement['city'] = 'Mountain View'
        engagement['country'] = 'US'
        engagement['lat'] = 37.3855745
        engagement['lon'] = -122.0820499


def add_cities(engagements):
    with open(cities_json) as json_data:
        cities = json.load(json_data)

    geolocator = Nominatim()
    for engagement in engagements.values():
        if engagement['country'] and engagement['city']:
            location_name = engagement['city'] + ', ' + engagement['country']
        elif engagement['city']:
            location_name = engagement['city']
        else:
            location_name = "Mountain View, US"
        if location_name not in cities:
            cities[location_name] = {}
            location = geolocator.geocode(location_name)
            if location:
                lat = location.latitude
                lon = location.longitude
            else:
                lat = 0
                lon = 0
            cities[location_name]['location'] = location_name
            cities[location_name]['lat'] = lat
            cities[location_name]['lon'] = lon

    with open(cities_json, 'w') as outfile:
        json.dump(cities, outfile)


def create_contacts_dict():
    contacts_rows = custom_sql('MARKETING_DB.t_all_contacts', ('Distinct email', 'Country'))
    return fill_count_dict(contacts_rows, 1)


def get_total_no_of_contacts():
    contacts = custom_sql('MARKETING_DB.t_all_contacts', ('Distinct email',))
    return len(contacts)


def test_filter_tuple_list():
    tuple_list = [('a', 'b', 'c'), ('a', 'b', 'c')]
    index_list = [0, 2]
    my_filtered_list = filter_tuple_list(tuple_list, index_list)
    assert(my_filtered_list == [['a', 'c'], ['a', 'c']])


def filter_tuple_list(tuple_list, index_list):
    my_list_of_lists = []
    tuple_len = len(tuple_list[0])
    for my_tuple in tuple_list:
        my_list = []
        for i in range(tuple_len):
            if i in index_list:
                my_list.append(my_tuple[i])
        my_list_of_lists.append(my_list)

    return my_list_of_lists


def fill_new_initiatives_dict(impact_initiatives):
    initiatives_dict = dict()

    fields = ('id', 'name', 'contact_name', 'contact_email', 'program',
              'type_of_initiative', 'summary', 'no_of_employees', 'url',)
    len_of_fields = len(fields)

    array_fields = ('ggc_focus', 'tech_focus', 'region_of_impact',)

    initiatives_dict['records'] = []

    for initiative in impact_initiatives:
        initiative_dict = dict()

        for idx, field in enumerate(fields):
            initiative_dict[field] = initiative[idx]

        for idx, field in enumerate(array_fields):
            # Change csv data into array of strings
            array = initiative[idx + len_of_fields].split(',')
            array = [x.strip(' ') for x in array]
            array = list(filter(None, array))
            if array:
                initiative_dict[field] = array
            else:
                initiative_dict[field] = []

            # Create options list
            field_options = field + '_options'
            for member in array:
                if member:
                    if field_options in initiatives_dict:
                        if member not in initiatives_dict[field_options]:
                            initiatives_dict[field_options].append(member)
                    else:
                        initiatives_dict[field_options] = [member]

        initiatives_dict['records'].append(initiative_dict)
    return initiatives_dict


def create_filtered_initiatives_dict():
    impact_rows = (
        'impact_initiative_id',
        'impact_initiative_name',
        'name_of_poc',
        'email',
        'rolled_program_affiliation',
        'impact_initiative_type',
        'summary',
        'num_of_employees',
        'homepage',

        'ggc_focus',
        'tech_focus',
        'region_of_impact',
    )

    required_fields = (
        'impact_initiative_name',
        'impact_initiative_type',
        'summary',
        'ggc_focus',
        'tech_focus',
        'homepage',
        'name_of_poc',
        'email',
        'rolled_program_affiliation',
    )

    conditions = []

    for field in required_fields:
        field += " <> ''"
        conditions.append(field)
    search_string = "where " + " and ".join(conditions)

    impact_initiatives = filter_sql(
        table='impact_db.t_impact_initiatives',
        columns_needed=impact_rows,
        search_string=search_string
    )

    return fill_new_initiatives_dict(impact_initiatives)


def test_create_filtered_initiatives_dict():
    print(create_filtered_initiatives_dict())


def filter_sql(table, columns_needed=(), search_string=''):

    with connection.cursor() as cursor:
        # Build sql statement based on number of columns needed
        columns_needed = columns_needed if len(columns_needed) > 0 else ('*',)
        sql_statement = "select {} from {}".format(", ".join(columns_needed), table)

        # Extend sql statement based on search parameters
        if search_string:
            sql_statement += " " + search_string

        cursor.execute(sql_statement)

        rows = cursor.fetchall()

    return rows


def test_filter_sql():
    table = 'impact_db.t_impact_initiatives_July2017'
    columns_needed = ('name', 'ggc_focus', 'tech_focus')
    search_string = "where impact_initiative_name <> '' and ggc_focus <> '' and tech_focus <> ''"

    # Test edge cases
    filter_sql(table)
    filter_sql(table, columns_needed=('impact_initiative_name',), search_string=search_string)

    # Print results of mainstream test case
    full_results = filter_sql(table, columns_needed=columns_needed)
    filtered_results = filter_sql(table, columns_needed, search_string=search_string)
    print("No of results: {}".format(len(full_results)))
    print("No of filtered results: {}".format(len(filtered_results)))
    print("{} results were filtered out".format(len(full_results) - len(filtered_results)))
