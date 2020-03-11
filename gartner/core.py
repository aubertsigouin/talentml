# -*- coding: utf-8 -*-
"""
A python wrapper around Gartner Talent Analytics Platform. 

Typical use :
    
wq = WantedQuery(
    passkey=API_KEY, 
    function=function, 
    query=query,
    date=date
)

df = wq.get_data()

Read API documentation for parameter information

"""

from .parse import parse

import pandas as pd
import numpy as np
from sklearn import preprocessing

import requests
import warnings

def bins_split(first_operand, second_operand):
    """
    Create a list of n second operand of a division.
    n is determined by the results of the floor division.
    The remainder of the division is appended at the end.

    Example :

    bins_split(33, 10)
    »  ['10', '10', '10', '3']
    """

    if first_operand < second_operand:
        return([str(first_operand)])
    else:
        floor_division = int(np.floor(first_operand/second_operand))
        remainders = str(first_operand % (floor_division*second_operand))
        second_operands_bin = [str(second_operand) for x in range(floor_division)]
        second_operands_bin.append(remainders)
        return(second_operands_bin)

class WantedQuery():
    """
    A wrapper around Garner Talent Neuron (Wanted) API V5.
    """

    data_path = 'response_jobs_job_'
    base_url = 'https://tnrp-api.gartner.com/wantedapi/v5.0/jobs?'

    def __init__(self, responsetype='json', descriptiontype='long', function = '',
                 pagesize='100', query=None, skill=None, date=None, passkey=None):
      
        self.full_url = self.base_url + '&'.join([f'{k}={v}' for k,v in locals().items() if v and k!='self'])
        print("""Full URL : \n{} """.format(self.full_url.replace(' ', '%22')))

    def call(self):
        response = requests.get(self.full_url).json()
        self.num_found = int(response['response']['numfound'])
        self.page_index = int(response['response']['pageindex'])
        self.page_size = int(response['response']['pagesize'])
        self.facets = response['response']['facets']
        self.indexes = bins_split(self.num_found, 100)
        self.url_batches = [self.full_url.replace(self.base_url, self.base_url+f'pageindex={n+1}&') for n in range(len(self.indexes))]

    def get_data(self):
        self.call()
        if self.num_found > 2000:
            warnings.warn("Your account is limited to the first '2000' documents.")
            self.url_batches = self.url_batches[:20]
        data = []
        for idx, url in enumerate(self.url_batches):
            response = requests.get(url).json()
            data.append(parse(response))

        return(pd.concat(data).reset_index(drop=True))
    

class WantedDB():
    def __init__(self, df:pd.DataFrame):
        self.id = df['id']
        self.hash = df['hash']
        self.ref_number = df['refnumber']
        self.is_staffing = df['isstaffing']
        self.is_anonymous = df['isanonymous']
        self.is_third_party = df['isthirdparty']
        self.is_inappropriate = df['isinappropriate']
        self.is_buk = df['isbulk']
        self.is_aggregator = df['isaggregator']
        self.is_free = df['isfree']
        self.is_classified_occupation = df['isclassifiedoccupation']
        self.is_classified_industry = df['isclassifiedindustry']
        self.is_current = df['iscurrent']
        self.dates_first_seen = pd.to_datetime(df['dates_firstseen'])
        self.dates_posted = pd.to_datetime(df['dates_posted'])
        self.dates_refreshed = pd.to_datetime(df['dates_refreshed'])
        self.title_name = df['title_value']
        self.title_id = df['title_titleid']
        self.clean_title_id = df['title_cleantitleid']
        self.semi_clean_title_id = df['title_semicleantitleid']
        self.description = df['description_value']
        self.occupation_code = df['occupation_occupation_code']
        self.occupation_label = df['occupation_occupation_label']
        self.occupation_revision = df['occupation_occupation_revision']
        self.industry_code = df['industry_code']
        self.industry_label = df['industry_label']
        self.function_id = df['function_id']
        self.function_name = df['function_label']
        self.employer_id = df['employer_id']
        self.employer_name = df['employer_name']
        self.employer_super_alias_id = df['employer_superaliasid']
        self.city_code = df['locations_location_0_city_code']
        self.city_name = df['locations_location_0_city_label']
        self.state_code = df['locations_location_0_state_code']
        self.state_name = df['locations_location_0_state_label']
        self.county_code = df['locations_location_0_county_code']
        self.county_name = df['locations_location_0_county_label']
        self.wib_id = df['locations_location_0_wib_id']
        self.wib_code = df['locations_location_0_wib_code']
        self.wib_name = df['locations_location_0_wib_label']
        self.msa_code = df['locations_location_0_msa_code']
        self.msa_name = df['locations_location_0_msa_label']
        self.latitude = df['locations_location_0_position_latitude'].astype(float)
        self.longitude = df['locations_location_0_position_longitude'].astype(float)
        self.salary_id = df['salaries_salary_0_id']
        self.salary_type = df['salaries_salary_0_type']
        self.salary_value = df['salaries_salary_0_value'].astype(int)
        self.jobtype_0_id = df['jobtypes_jobtype_0_id']
        self.jobtype_0_name = df['jobtypes_jobtype_0_label']
        self.jobtype_1_id = df['jobtypes_jobtype_1_id']
        self.jobtype_1_name = df['jobtypes_jobtype_1_label']
        self.tags = df['tags']
        self.source_id = df['sources_source_0_id']
        self.source_job_id = df['sources_source_0_jobid']
        self.source_tags = df['sources_source_0_tags']
        self.source_type = df['sources_source_0_type']
        self.source_name = df['sources_source_0_name']
        self.source_url = df['sources_source_0_url']
        self.source_valid_link = df['sources_source_0_validlink']
        self.df = df
    
    def city_postings(self, scaler='MinMaxScaler'):
        city_count = pd.DataFrame(self.city_name.value_counts())
        
        scaler = getattr(preprocessing, scaler)(feature_range=(0.1,0.9))
        scaled_count = scaler.fit_transform(city_count.values.reshape(-1,1))
        
        city_count['count_scaled'] = scaled_count
        city_count['mean_y'] = [self.latitude[self.city_name==city].mean() for city in city_count.index]
        city_count['mean_x'] = [self.longitude[self.city_name==city].mean() for city in city_count.index]
        city_count = city_count.rename(columns={'locations_location_0_city_label':'count'})
        
        return(city_count.drop('Unavailable'))