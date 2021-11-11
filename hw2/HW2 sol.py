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

import numpy as np
import pandas as pd
from timeit import Timer
from collections import defaultdict
import re
np.random.seed(0)

# +
# sample_list = [(1, 3, 5), (0, 1, 2), (1, 9, 8)]
# op = []
# for m in range(len(sample_list)):
#     li = [sample_list[m]]
#         for n in range(len(sample_list)):
#             if (sample_list[m][0] == sample_list[n][0] and
#                     sample_list[m][3] != sample_list[n][3]):
#                 li.append(sample_list[n])
#         op.append(sorted(li, key=lambda dd: dd[3], reverse=True)[0])
# res = list(set(op))
# -

# ## Concisely describe what task the code above accomplishes.
# From the constructed list, firstly, this sippnet selects one tupleand search the others in turn with the same first element and different last element, or only itself if none of others meets the requirement.	<br/>
# Then it sorts the selected tuples/tuple by the last elements decending order and picks up the top one. Append that top one into the `op` list.	<br/>
# Lastly, make the `op` list as a set, remove all the duplicate elements and turn it to a list again
#
# ## Modifing for sippnet
# * The indentation before the second `for` loop is not appropriate
# ```Python
# # Modified indentation
#     for n in range(len(sample_list)):
#         if (sample_list[m][0] == sample_list[n][0] and \
#             sample_list[m][3] != sample_list[n][3]):
#         li.append(sample_list[n])
#     op.append(sorted(li, key=lambda dd: dd[3], reverse=True)[0])
# ```
# * The 3 index of `sample_list[m][3] != sample_list[n][3]` is out of range.
# Since there are only three elements in a tuple, `(1,3,5)`for instance, the index ranges from 0 to 2. So that if the last element is needed, the code should be modified as `sample_list[m][2] != sample_list[n][2]`
# * The second for loop could start from `m+1` rather than `0` for more efficiency.
#
# ## The modified snippet can be shown as below

sample_list = [(1, 3, 5), (0, 1, 2), (1, 9, 8)]
op = []
for m in range(len(sample_list)):
    li = [sample_list[m]] # [(1, 3, 5)], ...
    for n in range(m+1, len(sample_list)):
        if (sample_list[m][0] == sample_list[n][0] and \
                sample_list[m][2] != sample_list[n][2]):
            li.append(sample_list[n])
    op.append(sorted(li, key=lambda dd: dd[2], reverse=True)[0])
res = list(set(op))
res

sample_list = [(1, 3, 5), (0, 1, 2), (1, 9, 8)]
op = []
for m in range(len(sample_list)):
    li = [sample_list[m]] # [(1, 3, 5)], ...
    for n in range(m+1, len(sample_list)):
        if (sample_list[m][0] == sample_list[n][0] and \
                sample_list[m][2] != sample_list[n][2]):
            li.append(sample_list[n])
    op.append(sorted(li, key=lambda dd: dd[2], reverse=True)[0])
res = list(set(op))
res


# ## Question 1 - List of Tuples
#
# Write a function that uses NumPy and a list comprehension to generate a random list of `n` k-tuples containing integers ranging from `low` to `high`. Choose an appropriate name for your function, and reasonable default values for `k`, `low`, and `high`.
#
# Use `assert` to test that your function returns a list of tuples.

# every tuple in the list is random generated from low to high and is sorted.
def list_of_tuples(n, k, low, high):
    size = k
    tup_list = []
    for i in range(n):
        tup = tuple(np.sort(np.random.randint(low, high, size)))
        tup_list.append(tup)
    return tup_list


# +
low = 10
high = 20
n = 5 # number of tuples
k = 10 # number of elements for each tuple
tup_list = list_of_tuples(n, k, low, high)
print(tup_list)

assert type(tup_list) == list
for i in range(len(tup_list)):
    assert type(tup_list[i]) == tuple


# -

# ## Question 2 - Refactor the Snippet [40 points]
# In this question, you will write functions to accomplish the goal you concisely described in part “a” of the warm up.
#
# a. Encapsulate the code snippet from the warmup into a function that parameterizes the role of 0 and 3 and is otherwise unchanged. Choose appropriate names for these paramters.
#
# b. Write an improved version of the function form part a that implements the suggestions from the code review you wrote in part b of the warmup.
#
# c. Write a function from scratch to accomplish the same task as the previous two parts. Your solution should traverse the input list of tuples no more than twice. Hint: consider using a dictionary or a default dictionary in your solution.
#
# d. Use the function you wrote in question 1 to generate a list of tuples as input(s), run and summarize a small Monte Carlo study comparing the execution times of the three functions above (a-c).

# a)
def sort_list(sample_list, same_idx, diff_idx, sort_idx):
    # same_idx for the index of required same value 
    # diff_idx for the index of required different value  
    # sort_idx for the sorting reference index
    # sample_list = [(1, 3, 5), (0, 1, 2), (1, 9, 8)]
    op = []
    for m in range(len(sample_list)):
        li = [sample_list[m]]
        for n in range(len(sample_list)):
            if (sample_list[m][same_idx] == sample_list[n][same_idx] and
                    sample_list[m][diff_idx] != sample_list[n][diff_idx]):
                li.append(sample_list[n])
        op.append(sorted(li, key=lambda dd: dd[sort_idx], reverse=True)[0])
    res = list(set(op))
    return res


sample_list = tup_list
same_idx = 0
diff_idx = 2
sort_idx = 1
result = sort_list(sample_list, same_idx, diff_idx, sort_idx)
print(result)


# b)
def sort_list_modified(sample_list, same_idx, diff_idx, sort_idx):
    # same_idx for the index of required same value 
    # diff_idx for the index of required different value  
    # sort_idx for the sorting reference index
    # sample_list = [(1, 3, 5), (0, 1, 2), (1, 9, 8)]
    op = []
    for m in range(len(sample_list)):
        li = [sample_list[m]]
        for n in range(m+1, len(sample_list)):
            if (sample_list[m][same_idx] == sample_list[n][same_idx] and \
                    sample_list[m][diff_idx] != sample_list[n][diff_idx]):
                li.append(sample_list[n])
        op.append(sorted(li, key=lambda dd: dd[sort_idx], reverse=True)[0])
    return list(set(op))


# c)
def sort_list_df(sample_list, same_idx, diff_idx, sort_idx):
    # same_idx for the index of required same value 
    # diff_idx for the index of required different value  
    # sort_idx for the sorting reference index
    # sample_list = [(1, 3, 5), (0, 1, 2), (1, 9, 8)]
    sample_df = pd.DataFrame(sample_list)
    op = pd.DataFrame(columns=range(len(sample_list[0])))

    for idx in range( len(sample_df) ):
        same_col = sample_df[same_idx]
        diff_col = sample_df[diff_idx]
        select_index = [idx]
        for idx_2 in range(idx+1, len(sample_df)):
            if same_col[idx] == same_col[idx_2] and \
            diff_col[idx] != diff_col[idx_2]:
                select_index.append(idx_2)
        select_rows = sample_df.loc[select_index,:] # select rows meets the criteria
        sr = select_rows.sort_values(by=sort_idx, ascending=False).iloc[[0],:]  # sort rows by selected column value
        op = pd.concat([op, sr], ignore_index=True)
    return op.drop_duplicates()


# c_002
def sort_list_df_2(sample_list, same_idx, diff_idx, sort_idx):
    # same_idx for the index of required same value 
    # diff_idx for the index of required different value  
    # sort_idx for the sorting reference index
    # sample_list = [(1, 3, 5), (0, 1, 2), (1, 9, 8)]
    sample_df = pd.DataFrame(sample_list)
    op = pd.DataFrame(columns=range(len(sample_list[0])))
    
    same_idx_val = sample_df[same_idx]
    same_value = same_idx_val.drop_duplicates().values # find the set of values on same_index col.
    for val in same_value:
        rows_same_idx = sample_df[sample_df[same_idx]==val]
        # ignore the rows have same value on diff_idx
        rows_diff_index = rows_same_idx.drop_duplicates(subset=[diff_idx])
        sr = rows_diff_index.sort_values(by=sort_idx, ascending=False).iloc[[0],:]
        op = pd.concat([op, sr], ignore_index=True)
    return op.drop_duplicates()


# +
# d)
low = 5
high = 50
n = 500
k = 100
sample_list = list_of_tuples(n, k, low, high)

same_idx = 0
diff_idx = 2
sort_idx = 1

# timing with ndarray input: -------------------------------------------------
time_nda = defaultdict(list)

for f in [sort_list, sort_list_modified, sort_list_df_2]:
    
    tm_list = []

    t = Timer('f(sample_list, same_idx, diff_idx, sort_idx)', globals={'f': f, 'sample_list': sample_list, \
                                                                       'same_idx': same_idx, 'diff_idx': diff_idx, 'sort_idx': sort_idx})
    tm = t.repeat(repeat=3, number=10)

    time_nda['Function'].append(f.__name__)
    time_nda['min, s'].append(np.min(tm))
    time_nda['median, s'].append(np.median(tm))
    time_nda['mean, s'].append(np.mean(tm))

time_nda = pd.DataFrame(time_nda)
for c, d in zip(time_nda.columns, time_nda.dtypes):
    if d == np.dtype('float64'):
        time_nda[c] = time_nda[c].map(lambda x: '%5.6f' % x)
time_nda
# -

# ## Question 3 - [30 points]
#
# In this question you will use Pandas to read, clean, and append several data files from the National Health and Nutrition Examination Survey NHANES. We will use the data you prepare in this question as the starting point for analyses in one or more future problem sets. For this problem, you should use the four cohorts spanning the years 2011-2018. You can find links to different NHANES cohorts here.
#
# * Use Python and Pandas to read and append the **demographic datasets** keeping only columns containing the **unique ids (SEQN), age (RIDAGEYR), race and ethnicity (RIDRETH3), education (DMDEDUC2), and marital status (DMDMARTL)**, along with the following variables related to the survey weighting: **(RIDSTATR, SDMVPSU, SDMVSTRA, WTMEC2YR, WTINT2YR)**. 
# * Add an additional column identifying to which cohort each case belongs. Rename the columns with literate variable names using all lower case and convert each column to an appropriate type. Finally, save the resulting data frame to a serialized “round-trip” format of your choosing (e.g. pickle, feather, or parquet).
#
#

# ================
# a)
demo_1112_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/DEMO_G.XPT")
demo_1314_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/DEMO_H.XPT")
demo_1516_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.XPT")
demo_1718_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/DEMO_J.XPT")

# +
demo_df_list = [demo_1112_df, demo_1314_df, demo_1516_df, demo_1718_df]
cohort_list = ['1112', '1314', '1516', '1718']

# create a block dataframe
demo_comb_df = pd.DataFrame(columns = ('SEQN', 'RIDAGEYR', 'RIDRETH3', 'DMDEDUC2', 'DMDMARTL', \
                               'RIDSTATR', 'SDMVPSU', 'SDMVSTRA', 'WTMEC2YR', 'WTINT2YR'))

for idx in range(len(demo_df_list)):
    df = demo_df_list[idx]
    df_select = df.loc[:,['SEQN', 'RIDAGEYR', 'RIDRETH3', 'DMDEDUC2', 'DMDMARTL', \
                               'RIDSTATR', 'SDMVPSU', 'SDMVSTRA', 'WTMEC2YR', 'WTINT2YR']]
    df_select['cohort'] = cohort_list[idx] 
    
    demo_comb_df = pd.concat([demo_comb_df, df_select], ignore_index=True) # concatenate each cohort

demo_comb_df = demo_comb_df.rename(columns={'SEQN': 'unique_ids', 'RIDAGEYR':'age', 'RIDRETH3':'race_and_ethnicity', \
                        'DMDEDUC2':'education', 'DMDMARTL':'marital_status'})
demo_comb_df= demo_comb_df.convert_dtypes() # Convert the DataFrame to use best possible dtypes.
demo_comb_df.to_pickle("demo_comb_df.pkl")
# -

demo_comb_df





# ================
# b)
oral_1112_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/OHXDEN_G.XPT")
oral_1314_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/OHXDEN_H.XPT")
oral_1516_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/OHXDEN_I.XPT")
oral_1718_df = pd.read_sas("https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/OHXDEN_J.XPT")

# +
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
print("the number of cases in the demographic final dataframe is %d"%(num_of_case_demo))
print("the number of cases in the oral health and dentition data final dataframe is %d"%(num_of_case_oral))






