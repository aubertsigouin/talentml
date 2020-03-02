# -*- coding: utf-8 -*-
"""
This a python wrapper around Gartner API. 
"""

import pandas as pd


class OnetDB():
    """
    A helper to extract data from O*NET
    """

    base_url = 'https://www.onetcenter.org/'

    def __init__(self):
        self.directory = {
            'technology_skills_competencies' : 'dl_files/frameworks/Technology_Skills_Competencies.xlsx'
            }
        #print(self.full_url)

    def call(self, f):
        response = pd.read_excel(self.base_url+f)
        return(response['Unnamed: 1'][2:])

    # def get_data(self):
    #     self.call()
    #     if self.num_found > 2000:
    #         warnings.warn("Your account is limited to the first '2000' documents.")
    #         self.url_batches = self.url_batches[:20]

    #     df_l=[]
    #     for idx, url in enumerate(self.url_batches):
    #         r = requests.get(url).json()
    #         df_l.append(json_to_tabular(r, root_path = self.data_path, n_of_row = int(self.indexes[idx])))

    #     return(pd.concat(df_l).reset_index(drop=True))