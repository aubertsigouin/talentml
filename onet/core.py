# -*- coding: utf-8 -*-
"""
This a python wrapper around Gartner API. 
"""

import pandas as pd


class OnetDB():
    """
    A helper to extract data from O*NET
    """

    def __init__(self):
        self.links_directory = {
            'abilities' : 'https://www.onetcenter.org/dl_files/database/db_24_2_excel/Abilities.xlsx',
            'hot_technologies' : '../data/hot_technologies/Hot_Technologies_.xls'
            
            }
        #print(self.full_url)

    def build_hot_technologies(self):
        df = pd.read_excel(self.links_directory['hot_technologies']).iloc[2:,:].reset_index(drop=True)
        tech_dict = {}
        clean_names = df['Hot Technologies']
        for x in range(len(df)):
            tech_dict[clean_names.iloc[x]] = {'aliases': list(set(df.iloc[x].values))}

        return(tech_dict)

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