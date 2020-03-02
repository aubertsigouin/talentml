# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 10:08:42 2020

@author: AubertSigouin-Lebel
"""

import pandas as pd

def generate_urls(params, delimiter='&'):
    """
    Generate a list of url based on parameters and delimiter

    Example :

    generate_urls(['https://www.aljazeera.com', 'news', '2020', '01'], '/')
    »  'https://www.aljazeera.com/news/2020/01'
    """
    return(delimiter.join(params))

def generate_dates(start, end, str_format = '%Y-%m-%d', delimiter='-'):
    """
    Generate a list of dates following a specific string format
    1. Creates one long list, from start to end, then
    2. Creates a list of sequences of two dates (1 starting 1 day before before the other), finally
    3. Creates one unified list containingg dates joint by a delimiter

    Example :

    generate_dates('2020-01-02','2020-01-15')
    »  ['2020-01-02-2020-01-03',
        '2020-01-03-2020-01-04',
        '2020-01-04-2020-01-05',
        '2020-01-05-2020-01-06',
        '2020-01-06-2020-01-07',
        '2020-01-07-2020-01-08']
    """

    total_range = pd.date_range(start=start,end=end).strftime(str_format)
    seqs = list(zip(total_range[:-1], total_range[1:]))
    return([delimiter.join(seq) for seq in seqs])
