# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:18:49 2020

@author: AubertSigouin-Lebel
"""

import pandas as pd

def parse(json):
    df = pd.DataFrame()
    df['dates_first_seen'] = pd.to_datetime([job['dates']['firstseen'] for job in json['response']['jobs']['job']])
    df['dates_refreshed'] = pd.to_datetime([job['dates']['refreshed'] for job in json['response']['jobs']['job']])
    df['dates_posted'] = pd.to_datetime([job['dates']['posted'] for job in json['response']['jobs']['job']])
    df['ids'] = [job['id'] for job in json['response']['jobs']['job']]
    df['hash_number'] = [job['hash'] for job in json['response']['jobs']['job']]
    df['ref_number'] = [job['refnumber'] for job in json['response']['jobs']['job']]
    df['is_staffing'] = [job['isstaffing'] for job in json['response']['jobs']['job']]
    df['is_third_party'] = [job['isthirdparty'] for job in json['response']['jobs']['job']]
    df['is_inappropriate'] = [job['isinappropriate'] for job in json['response']['jobs']['job']]
    df['is_bulk'] = [job['isbulk'] for job in json['response']['jobs']['job']]
    df['is_aggregator'] = [job['isaggregator'] for job in json['response']['jobs']['job']]
    df['is_free'] = [job['isfree'] for job in json['response']['jobs']['job']]
    df['is_classified_occupation'] = [job['isclassifiedoccupation'] for job in json['response']['jobs']['job']]
    df['is_classified_industry'] = [job['isclassifiedindustry'] for job in json['response']['jobs']['job']]
    df['is_current'] = [job['iscurrent'] for job in json['response']['jobs']['job']]
    df['title_name'] = [job['title']['value'] for job in json['response']['jobs']['job']]
    df['title_id'] = [job['title']['titleid'] for job in json['response']['jobs']['job']]
    df['semi_clean_title_id'] = [job['title']['semicleantitleid'] for job in json['response']['jobs']['job']]
    df['clean_title_id'] = [job['title']['cleantitleid'] for job in json['response']['jobs']['job']]
    df['clean_title_id'] = [job['title']['cleantitleid'] for job in json['response']['jobs']['job']]
    df['description'] = [job['description']['value'] for job in json['response']['jobs']['job']]
    df['occupation_code'] = [job['description']['value'] for job in json['response']['jobs']['job']]
    df['occupation_label'] = [job['occupation']['occupation']['label'] for job in json['response']['jobs']['job']]
    df['occupation_revision'] = [job['occupation']['occupation']['revision'] for job in json['response']['jobs']['job']]
    df['industry_code'] = [job['industry']['code'] for job in json['response']['jobs']['job']]
    df['industry_label'] = [job['industry']['label'] for job in json['response']['jobs']['job']]
    df['function_id'] = [job['function']['id'] for job in json['response']['jobs']['job']]
    df['function_name'] = [job['function']['label'] for job in json['response']['jobs']['job']]
    df['employer_id'] = [job['employer']['id'] for job in json['response']['jobs']['job']]
    df['employer_name'] = [job['employer']['name'] for job in json['response']['jobs']['job']]
    df['employer_super_alias_id'] = [job['employer']['superaliasid'] for job in json['response']['jobs']['job']]
    df['city_code'] = [job['locations']['location'][0]['city']['code'] for job in json['response']['jobs']['job']]
    df['city_name'] = [job['locations']['location'][0]['city']['label'] for job in json['response']['jobs']['job']]
    df['state_code'] = [job['locations']['location'][0]['state']['code'] for job in json['response']['jobs']['job']]
    df['state_name'] = [job['locations']['location'][0]['state']['label'] for job in json['response']['jobs']['job']]
    df['county_code'] = [job['locations']['location'][0]['county']['code'] for job in json['response']['jobs']['job']]
    df['county_name'] = [job['locations']['location'][0]['county']['label'] for job in json['response']['jobs']['job']]
    df['msa_code'] = [job['locations']['location'][0]['msa']['code'] for job in json['response']['jobs']['job']]
    df['msa_name'] = [job['locations']['location'][0]['msa']['label'] for job in json['response']['jobs']['job']]
    df['wib_code'] = [job['locations']['location'][0]['wib']['code'] for job in json['response']['jobs']['job']]
    df['wib_name'] = [job['locations']['location'][0]['wib']['label'] for job in json['response']['jobs']['job']]
    df['latitude'] = [float(job['locations']['location'][0]['position']['latitude']) for job in json['response']['jobs']['job']]
    df['longitude'] = [float(job['locations']['location'][0]['position']['longitude']) for job in json['response']['jobs']['job']]
    df['salary_id'] = [job['salaries']['salary'][0]['id'] for job in json['response']['jobs']['job']]
    df['salary_type'] = [job['salaries']['salary'][0]['type'] for job in json['response']['jobs']['job']]
    df['salary_value'] = [int(job['salaries']['salary'][0]['value']) for job in json['response']['jobs']['job']]
    df['jobtype_0_id'] = [job['jobtypes']['jobtype'][0]['id'] for job in json['response']['jobs']['job']]
    df['jobtype_0_name'] = [job['jobtypes']['jobtype'][0]['label'] for job in json['response']['jobs']['job']]
    df['jobtype_1_id'] = [job['jobtypes']['jobtype'][1]['id'] for job in json['response']['jobs']['job']]
    df['jobtype_0_name'] = [job['jobtypes']['jobtype'][1]['label'] for job in json['response']['jobs']['job']]
    df['tags'] = [job['tags'] for job in json['response']['jobs']['job']]
    df['source_job_id'] = [job['sources']['source'][0]['jobid'] for job in json['response']['jobs']['job']]
    df['source_id'] = [job['sources']['source'][0]['id'] for job in json['response']['jobs']['job']]
    df['source_tags'] = [job['sources']['source'][0]['tags'] for job in json['response']['jobs']['job']]
    df['source_type'] = [job['sources']['source'][0]['type'] for job in json['response']['jobs']['job']]
    df['source_name'] = [job['sources']['source'][0]['name'] for job in json['response']['jobs']['job']]
    df['source_url'] = [job['sources']['source'][0]['url'] for job in json['response']['jobs']['job']]
    df['source_valid_link'] = [job['sources']['source'][0]['validlink'] for job in json['response']['jobs']['job']]
    return(df)