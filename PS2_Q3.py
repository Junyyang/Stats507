# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# ## Extract code from PS2, Q3

import numpy as np
import pandas as pd
from timeit import Timer
from collections import defaultdict
import re
np.random.seed(0)

# +
# ================
# a)
demo_1112_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/DEMO_G.XPT")
demo_1314_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/DEMO_H.XPT")
demo_1516_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.XPT")
demo_1718_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/DEMO_J.XPT")

demo_df_list = [demo_1112_df, demo_1314_df, demo_1516_df, demo_1718_df]
cohort_list = ['1112', '1314', '1516', '1718']

# create a block dataframe
demo_comb_df = pd.DataFrame(columns = ('SEQN', 'RIDAGEYR', 'RIAGENDR', 'RIDRETH3', 'DMDEDUC2', 'DMDMARTL', \
                               'RIDSTATR', 'SDMVPSU', 'SDMVSTRA', 'WTMEC2YR', 'WTINT2YR'))

for idx in range(len(demo_df_list)):
    df = demo_df_list[idx]
    df_select = df.loc[:,['SEQN', 'RIDAGEYR', 'RIAGENDR','RIDRETH3', 'DMDEDUC2', 'DMDMARTL', \
                               'RIDSTATR', 'SDMVPSU', 'SDMVSTRA', 'WTMEC2YR', 'WTINT2YR']]
    df_select['cohort'] = cohort_list[idx] 
    
    demo_comb_df = pd.concat([demo_comb_df, df_select], ignore_index=True) # concatenate each cohort

demo_comb_df = demo_comb_df.rename(columns={'SEQN': 'unique_ids', 'RIDAGEYR':'age', 'RIAGENDR':'gender', 'RIDRETH3':'race_and_ethnicity', \
                        'DMDEDUC2':'education', 'DMDMARTL':'marital_status'})
demo_comb_df= demo_comb_df.convert_dtypes() # Convert the DataFrame to use best possible dtypes.
demo_comb_df.to_pickle("demo_comb_df.pkl")

# +
# ================
# b)
oral_1112_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/OHXDEN_G.XPT")
oral_1314_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/OHXDEN_H.XPT")
oral_1516_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/OHXDEN_I.XPT")
oral_1718_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/OHXDEN_J.XPT")

oral_df_list = [oral_1112_df, oral_1314_df, oral_1516_df, oral_1718_df]
cohort_list = ['1112', '1314', '1516', '1718']

# create a block dataframe
TC_list = []
dictionary = {}

for col in oral_1112_df.columns:
    if 'TC' in col:
        TC_list.append(col)
TC_list  # find all the column name has 'TC' and 'CTC'
oral_comb_df = pd.DataFrame(columns = ['SEQN', 'OHDDESTS'] + TC_list )

# concatenate four modified dataframes
for idx in range(len(oral_df_list)):
    df = oral_df_list[idx]
    df_select = df.loc[:, ['SEQN' , 'OHDDESTS'] + TC_list] 
    df_select['cohort'] = cohort_list[idx] 
    oral_comb_df = pd.concat([oral_comb_df, df_select], ignore_index=True) # concatenate each cohort

# Rename the columns with literate variable names
for col in TC_list:
    num_str = re.findall("\d+",col)[0]  # find the digit in string
    if 'CTC' in col:
        dictionary.update({col:"coronal_cavities_"+num_str})
    else:
        dictionary.update({col:"tooth_counts_"+num_str})
oral_comb_df = oral_comb_df.rename(columns=dictionary)

# Convert the DataFrame to use best possible dtypes.
oral_comb_df= oral_comb_df.convert_dtypes() 
# Save the resulting data frame to picle
oral_comb_df.to_pickle("oral_comb_df.pkl")
# -

# ================
# c) report the number of cases there are in the two datasets above.
num_of_case_demo = len(demo_comb_df)
num_of_case_oral = len(oral_comb_df)
print("the number of cases in the demographic final dataframe is %d"%(num_of_case_demo)):
print("the number of cases in the oral health and dentition data final dataframe is %d"%(num_of_case_oral))




