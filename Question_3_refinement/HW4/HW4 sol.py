# -*- coding: utf-8 -*-
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

# ## Question 0 - Topics in Pandas [25 points]
#
# For this question, please pick a topic - such as a function, class, method, recipe or idiom related to the pandas python library and create a short tutorial or overview of that topic. The only rules are below.
# - Pick a topic not covered in the class slides.
# - Do not knowingly pick the same topic as someone else.
# - Use bullet points and titles (level 2 headers) to create the equivalent of 3-5 “slides” of key points. They shouldn’t actually be slides, but please structure your key points in a manner similar to the class slides (viewed as a notebook).
# Include executable example code in code cells to illustrate your topic.
# You do not need to clear your topic with me. If you want feedback on your topic choice, please discuss with me or a GSI in office hours.

# ## Windows Rolling
# - Return a rolling object allowing summary functions to be applied to windows of length n.
# - By default, the result is set to the right edge of the window. This can be changed to the center of the window by setting `center=True`.
# - Each points' weights could be determined by `win_type` shown in [windows function](https://docs.scipy.org/doc/scipy/reference/signal.windows.html#module-scipy.signal.windows), or evenly weighted as default.

import numpy as np
import pandas as pd
from os.path import exists
import re

rng = np.random.default_rng(9 * 2021 * 28)
n=100
a = rng.binomial(n=1, p=0.5, size=n)
b = 1 - 0.5 * a + rng.normal(size=n)
c = 0.8 * a + rng.normal(size=n) 
df = pd.DataFrame({'a': a, 'b': b, 'c': c})
df['c'].plot()

# - Calculating the mean in centered windows with a window length of 10 and windows type of 'triangular'

df['c'].rolling(10, center=True, win_type='triang').mean().plot()

# - Except existing functions like `sum`, `mean` and `std`, you could also use the self defined funciton by `agg.()`

df['c'].rolling(10).agg(lambda x: max(x)).plot()

# ## Question 1 - NHANES Table 1 [35 points]
#
# As discussed previously in class, academic papers reporting on human subjects typically include a “table 1” summarizing the demographics of the subjects included. This table is typically stratified into columns by a key exposure, outcome, or other important variable.
#
# When there are subjects with missing outcomes, it is common to include a table like described above examining the (marginal) relationships between missingness and key demographics. This helps an interested reader reason about possible selection bias stemming from those for whom the outcome is observed being different in some ways from those for whom it is not.
#
# In this activity, we will construct a balance table comparing demogarphics for those who are or are not missing the oral health examination in the NHANES data prepared in Problem Set 2, Question 3.

# ### part a)
# Revise your solution to PS2 Question 3 to also include gender (RIAGENDR) in the demographic data.
#
# Update (October 14): Include your data files in your submission and with extension .pickle, .feather or .parquet and include a code cell here that imports those files from the local directory (the same folder as your .ipynb or .py source files).

# Modify the levels for categorical variables from [https://github.com/jbhender/Stats507_F21/blob/main/ps/ps2_solution.ipynb]

# levels for categorical variables
demo_cat = {
    'gender': {1: 'Male', 2: 'Female'},
    'race': {1: 'Mexican American',
             2: 'Other Hispanic',
             3: 'Non-Hispanic White',
             4: 'Non-Hispanic Black',
             6: 'Non-Hispanic Asian',
             7: 'Other/Multiracial'
             },
#     'education': {1: 'Less than 9th grade',
#                   2: '9-11th grade (Includes 12th grade with no diploma)',
#                   3: 'High school graduate/GED or equivalent',
#                   4: 'Some college or AA degree',
#                   5: 'College graduate or above',
#                   7: 'Refused',
#                   9: "Don't know"
#                   },
    'marital_status': {1: 'Married',
                       2: 'Widowed',
                       3: 'Divorced',
                       4: 'Separated',
                       5: 'Never married',
                       6: 'Living with partner',
                       77: 'Refused',
                       99: "Don't know"
                       },
    'exam_status': {1: 'Interviewed only',
                    2: 'Both interviewed and MEC examined'
                    }
    }

# +
demo_file = './demo_comb_df.pkl'
if exists(demo_file):
    demo_comb_df = pd.read_pickle(demo_file)
else:
    # ================
    #  PS2 Question 3, also include gender (RIAGENDR) in the demographic data
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
        df_select = df.loc[:,['SEQN', 'RIDAGEYR', 'RIAGENDR', 'RIDRETH3', 'DMDEDUC2', 'DMDMARTL', \
                                   'RIDSTATR', 'SDMVPSU', 'SDMVSTRA', 'WTMEC2YR', 'WTINT2YR']]
        df_select['cohort'] = cohort_list[idx] 

        demo_comb_df = pd.concat([demo_comb_df, df_select], ignore_index=True) # concatenate each cohort

    demo_comb_df = demo_comb_df.rename(columns={'SEQN': 'unique_ids', 'RIDAGEYR':'age', 'RIAGENDR':'gender',
                                                'RIDRETH3':'race', 'DMDEDUC2':'education', 'RIDSTATR': 'exam_status',
                                                'DMDMARTL':'marital_status'})
    demo_comb_df= demo_comb_df.convert_dtypes() # Convert the DataFrame to use best possible dtypes.
    
    # categorical variables
    for col, d in demo_cat.items():
        demo_comb_df[col] = pd.Categorical(demo_comb_df[col].replace(d))
    demo_comb_df['cohort'] = pd.Categorical(demo_comb_df['cohort'])
    
    # Save the resulting data frame to picle
    demo_comb_df.to_pickle("demo_comb_df.pkl")
    
demo_comb_df
# -

# ### part b)
# The variable OHDDESTS contains the status of the oral health exam. Merge this variable into the demographics data.
#
# Use the revised demographic data from part a and the oral health data from PS2 to create a clean dataset with the following variables:
#
# - id (from SEQN)
# - gender
# - age
# - under_20 if age < 20
# - college - with two levels:
# ‘some college/college graduate’ or
# ‘No college/<20’ where the latter category includes everyone under 20 years of age.
# - exam_status (RIDSTATR)
# - ohx_status - (OHDDESTS) <br/>
# <br/>
# Create a categorical variable in the data frame above named ohx with two levels “complete” for those with `exam_status == 2` and `ohx_status == 1` or “missing” when `ohx_status` is missing or corresponds to “partial/incomplete.”

ohx_cat = {
    'ohx_status': {1: 'Complete', 2: 'Partial', 3: 'Not Done'}
    }

oral_comb_file = './oral_comb_df.pkl'
if exists(oral_comb_file):
    oral_comb_df = pd.read_pickle(oral_comb_file)
else:
    # ================
    #  PS2 Question 3, also include gender (RIAGENDR) in the demographic data
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
# oral_comb_df

# +
oral_df = oral_comb_df[['SEQN', 'OHDDESTS']]
oral_df = oral_df.rename(columns={'SEQN': 'unique_ids', 
                                  'OHDDESTS':'ohx_status'})

# categorical variables
for col, d in ohx_cat.items():
    oral_df[col] = pd.Categorical(oral_df[col].replace(d))
oral_df
# -

demo_df = demo_comb_df[['unique_ids', 'gender','age', 
                        'education', 'exam_status']]
merge_demo_oral = pd.merge(demo_df, oral_df, on=['unique_ids'], 
                           how='left')
merge_demo_oral

# how to add column between columns
merge_demo_oral['under_20'] = merge_demo_oral['age'].agg(lambda x : bool(x<20))
merge_demo_oral

# +
college_cat = {
    'college': {4: 'some college/college graduate', 
                  5: 'some college/college graduate', 
                  1: 'No college/<20',
                  2: 'No college/<20',
                  3: 'No college/<20',
                  7: 'No college/<20',
                  9: 'No college/<20',
                  np.nan: 'No college/<20'
               }
    }

merge_demo_oral = merge_demo_oral.rename(columns={'education': 'college'})

# replace by category
for col, d in college_cat.items():
    merge_demo_oral[col] = pd.Categorical(merge_demo_oral[col].replace(d))

merge_demo_oral = merge_demo_oral[['unique_ids', 'gender', 'age', 'under_20',
                                   'college', 'exam_status', 'ohx_status'
                                   ]]
merge_demo_oral

# +
# how to and operate two columns and get the results
# exam_status == 2
temp_1 = merge_demo_oral[['exam_status']] == 'Both interviewed and MEC examined' 
# ohx_status == 1
temp_2 = merge_demo_oral[['ohx_status']] == 'Complete'

temp_2 = temp_1.join(temp_2, how='outer')
# True for those with exam_status == 2 and ohx_status == 1
# False for others
merge_demo_oral['ohx'] = temp_2.exam_status & temp_2.ohx_status

# Replace status name
ohx_cat = {
    'ohx': {True: 'Complete', False: 'Missing'}
    }

# categorical variables
for col, d in ohx_cat.items():
    merge_demo_oral[col] = pd.Categorical(merge_demo_oral[col].replace(d))
merge_demo_oral
# -

# ### part c)
# Remove rows from individuals with `exam_status != 2`as this form of missingness is already accounted for in the survey weights. 
# **Report the number of subjects removed and the number remaining.**

# total rows
total_rows_num = len(merge_demo_oral)
# how to drop the rows
drop_demo_oral = merge_demo_oral.drop(merge_demo_oral[merge_demo_oral.exam_status 
                                                       != 'Both interviewed and MEC examined'].index)
ramain_rows_num = len(drop_demo_oral)
print('the number of subjects removed is {} and the number remaining is {}.'
      .format(total_rows_num - ramain_rows_num, ramain_rows_num))

# ### part d)
# Construct a table with ohx (complete / missing) in columns and each of the following variables **summarized** in rows:
#
# - age
# - under_20
# - gender
# - college
# <br/>
#
# For the rows corresponding to categorical variable in your table, each cell should provide a count (n) and a percent (of the row) as a nicely formatted string. For the continous variable age, report the mean and standard deviation [Mean (SD)] for each cell.
#
# Include a column ‘p-value’ giving a p-value testing for a mean difference in age or an association beween each categorical varaible and missingness. Use a chi-squared test comparing the 2 x 2 tables for each categorical characteristic and OHX exam status and a t-test for the difference in age.
#
# **Hint*: Use scipy.stats for the tests.

# create the blank df to fill in columns
ohx_assoc_df = pd.DataFrame()
column_list = ['ohx', 'age', 'under_20', 'gender', 'college']
ohx_assoc_df[column_list] = drop_demo_oral[column_list]
ohx_assoc_df

temp = ohx_assoc_df.copy()
# temp.set_index(['gender', 'under_20'],inplace=True)
temp

# how to reconstruct temp to df
df = pd.DataFrame(np.random.rand(7, 2), 
                  index=[["gender", "gender", "college", "college", "under_20", "under_20", 'age'], 
                         ["Female", "Male", "No college/<20", "some college/college graduate", "True", "False", "/"], 
                         ],
                  columns = [["complete", "missing"]]       
                 )
df.columns.names = ["ohx_status"]
df

# ## Question 2 - Monte Carlo Comparison [40 points]
# In this question you will use your functions from problem set 1, question 3 for construcing binomial confidence intervals for a population proprotion in a Monte Carlo study comparing the performance of the programmed methods.
#
# In the instructions that follow, let n refer to sample size and p to the population proportion to be estimated.
#
# Choose a nominal confidence level of 80, 90 or 95% to use for all parts below.
#
# You may wish to collect your confidence interval functions in a separate file and import them for this assignment. See here for helpful discussion.
#
# Update, October 14 - Make sure to correct any mistakes in your functions from PS1, Q3. It is also acceptable to revise your functions to use vectorized operations to make the Monte Carlo study more efficient.

# ### part a) Level Calibration














