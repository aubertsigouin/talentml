# -*- coding: utf-8 -*-
"""
This a python wrapper around Gartner API. 
"""

from flatten_json import flatten

import pandas as pd
import numpy as np

import requests

import math
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

def filter_1D_dict(d, string, by = 'value'):
    """
    Keep elements of a unested json structure
    if key startswing a specified string 

    Example :

    d = {
        'location_city' : 10, 
        'location_state' : 20, 
        'salary': 10
    }

    filter_dict_keys(d, by = 'key', string='location')
    »  ['location_city', 'location_state']
    """
    if by == 'key':
        return([k for k,v in d.items() if k.startswith(string)])
    else:
        return([v for k,v in d.items() if k.startswith(string)])

def json_to_tabular(json, root_path, n_of_row):
    """
    Convert a json data structure to a tabular structure. The nested JSON
    is flatten to a 1D dictionary. The key label correspond to the
    data path in the unested JSON. Each row is specified in the key label. 
    This row index a used the filter the unested JSON. 

    Example : 

    json = {
        'response' : '200',
        'responsetype' : 'JSON',
        'data' : [
            {'id' : 120334, 'salary' : {'projected':10000, 'real':85000}},
            {'id' : 120335, 'salary' : {'projected':20000, 'real':88000}}
        ]
    }

    json_to_tabular(json=json, root_path='data_', n_of_row=2)
    » id	salary_projected	salary_real
    0	120334	10000	85000
    1	120335	20000	88000
    """
    flat = flatten(json)
    values = [filter_1D_dict(d=flat, string =root_path+f'{row}_') for row in range(n_of_row)]
    cols = [filter_1D_dict(d=flat, string = root_path+f'{row}', by= 'key') for row in range(n_of_row)]
    if n_of_row>1:
        cols = [col[len(root_path)+2:] for col in cols[0]]
    df = pd.DataFrame(values)
    df = df.iloc[:,:62]
    df.columns = cols[:62]
    return(df)


class WantedQuery():
    """
    A wrapper around Garner Talent Neuron (Wanted) API V5.
    """

    data_path = 'response_jobs_job_'
    base_url = 'https://tnrp-api.gartner.com/wantedapi/v5.0/jobs?'

    def __init__(self, responsetype='json', descriptiontype='long', function = '',
                 pagesize='100', query=None, skill=None, date=None, passkey=None):
        self.full_url = self.base_url + '&'.join([f'{k}={v}' for k,v in locals().items() if v and k!='self'])
        #print(self.full_url)

    def call(self):
        response = requests.get(self.full_url).json()
        self.num_found = int(response['response']['numfound'])
        self.indexes = bins_split(self.num_found, 100)
        self.url_batches = [self.full_url.replace(self.base_url, self.base_url+f'pageindex={n+1}&') for n in range(len(self.indexes))]

    def get_data(self):
        self.call()
        if self.num_found > 2000:
            warnings.warn("Your account is limited to the first '2000' documents.")
            self.url_batches = self.url_batches[:20]

        df_l=[]
        for idx, url in enumerate(self.url_batches):
            r = requests.get(url).json()
            df_l.append(json_to_tabular(r, root_path = self.data_path, n_of_row = int(self.indexes[idx])))

        return(pd.concat(df_l).reset_index(drop=True))