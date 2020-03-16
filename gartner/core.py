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
    
