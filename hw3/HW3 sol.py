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
import matplotlib.pyplot as plt
from scipy.stats import norm, binom, beta
from os.path import exists

# ## Question 0 - RECS and Replicate Weights [15 points]
#
# In this problem set, you will analyze data from the 2009 and 2015 Residential Energy Consumpion Surveys RECS put out by the US Energy Information Agency. In this warm up question, you will:
#
# - find URLs from which to download the data for subsequent questions,
# - determine variables you will need by examining the codebooks, and
# - familiarize yourself with the replicate weight method used for computing standard errors and constructing confidence intervals.
#
# ### Data Files
# Find links to the 2009 and 2015 RECS microdata files and report them here. In the 2009 data year the replicate weights (see below) are distributed in a separate file. Find and report the link to that file as well.

# > 2009 RECS microdata files [link](https://www.eia.gov/consumption/residential/data/2009/csv/recs2009_public.csv) <br/> 
# https://www.eia.gov/consumption/residential/data/2009/csv/recs2009_public.csv <br/>
# The replicate weights of 2009 data [link](https://www.eia.gov/consumption/residential/data/2009/csv/recs2009_public_repweights.csv) 
# https://www.eia.gov/consumption/residential/data/2009/csv/recs2009_public_repweights.csv<br/>
# 2015 RECS microdata files [link](https://www.eia.gov/consumption/residential/data/2015/csv/recs2015_public_v4.csv) 	
# https://www.eia.gov/consumption/residential/data/2015/csv/recs2015_public_v4.csv<br/>

# +
# ==================
# data acquirement
RECS_2009_file, RECS_2015_file = 'RECS_2009.csv', 'RECS_2015.csv'
RECS_09_RepW = 'RepWeights_2009.csv'

if exists(RECS_2009_file):
    recs09_df = pd.read_csv(RECS_2009_file)
else:
    recs09_df = pd.read_csv(
        'https://www.eia.gov/consumption/residential/data/2009/csv/recs2009_public.csv'
    )
    recs09_df.to_csv(RECS_2009_file)
    
if exists(RECS_2015_file):
    recs15_df = pd.read_csv(RECS_2015_file)
else:
    recs15_df = pd.read_csv(
        'https://www.eia.gov/consumption/residential/data/2015/csv/recs2015_public_v4.csv'
    )
    recs15_df.to_csv(RECS_2015_file)

# In the 2009 data year the replicate weights (see below) are distributed in a separate file
if exists(RECS_09_RepW):
    repw09_df = pd.read_csv(RECS_09_RepW)
else:
    repw09_df = pd.read_csv(
        'https://www.eia.gov/consumption/residential/data/2009/csv/recs2009_public_repweights.csv'
    )
    repw09_df.to_csv(RECS_09_RepW)

recs15_df.head()
# -

# ### Variables
# Using the **codebooks** for the assoicated data files, determine what variables you will need to answer the following question. Be sure to include variables like the unit id and sample weights.
#
# > Estimate the average number of heating and cooling degree days (base temperature 65 °F) for residences in each Census region for both 2009 and 2015.
#

# Variables required: <br/>
# DOEID:	Unique identifier for each respondent <br/>
# REGIONC:	Census Region <br/>
# DIVISION:	Census Division <br/>
# REPORTABLE_DOMAIN:	Reportable states and groups of states <br/>
# TYPEHUQ:	Type of housing unit <br/>
# NWEIGHT:	Final sample weight <br/>
# HDD65:	Heating degree days in 2009, base temperature 65F <br/>
# CDD65:	Cooling degree days in 2009, base temperature 65F <br/>

HDD_09_mean = (recs09_df
               .groupby('REGIONC')
               [['HDD65']]
               .mean())
HDD_09_mean

HDD_15_mean = (recs15_df
               .groupby('REGIONC')
               [['HDD65']]
               .mean())
HDD_15_mean

# ### Weights and Replicate Weights
# Residences participating in the RECS surveys are not an independent and identically distributed sample of residences from the population of all US residences in the survey years. Instead, a complex sampling procedure is used. The details of the sampling process are beyond the scope of this course and assignment. However, you do need to know that residences in the surveys are weighted and to make use of those weights in your solution. Moreover, these surveys include **balanced repeated replicate (brr) weights** to facilitate computation of standard errors and, in turn, construction of confidence intervals.
#
# On the same page as the data, you will find a link explaining how to use the **replicate weights**. <br/>
# Report that link here:

# > How to use replicate weights [link](https://www.eia.gov/consumption/residential/methodology/2009/pdf/using-microdata-022613.pdf) <br/>
# https://www.eia.gov/consumption/residential/methodology/2009/pdf/using-microdata-022613.pdf

# then, citing the linked document, briefly explain how the **replicate weights** are used to estimate **standard errors** for **weighted point estimates**. 
#
# The standard error of an estimator is **the square root of that estimator’s variance**. Please note that I am asking you about the standard error and not the relative standard error. In your explanation please retype the **key equation** making sure to document what each variable in the equation is. 
#
# Don’t forget to include the Fay coefficient and its value(s) for the specific replicate weights included with the survey data.

# The standard error is given by the estimated variance of $\tilde{\theta}$, could be mean of samples. The formula can be written as <br/>
# $$ \hat{V}(\tilde{\theta}) = \frac{1}{R (1 - \epsilon)^2} \sum_{r=1}^R (\hat{\theta}_r - \hat{\theta})$$
# where $R = 244$ for 2009 RECS microdata file and $R = 96$ for 2015 RECS microdata files, $\epsilon$ is the Fay coefficient $\epsilon = 0.5$. $\hat{\theta}$ is calculated w.r.t final weights while $\hat{\theta}_r$ is deduced by substituting final weights with replicate weights for each $r.

# ## Question 1 - Data Preparation [20 points]
# In this question you will use Pandas to download, read, and clean the RECS data needed for subsequent questions. Use pandas to read data directly from the URLs you documented in the warmup when local versions of the files are not available. After download and/or clearning, write local copies of the datasets. Structure your code to use exists from the (built-in) sys module so the data are only downloaded when not already available locally.
#
#

# ### part a)
# Separately for 2009 and 2015, construct datasets containing just the minimal necessary variables identified in the warmup, excluding the replicate weights.  <br/>
# Choose an appropriate format for each of the remaining columns, particularly by creating categorical types where appropriate.
#
#

recs09_dfc = recs09_df.copy()
recs09_mini = recs09_dfc[['DOEID', 'REGIONC', 'HDD65', 'CDD65', 'NWEIGHT']]
recs09_mini['DOEID'] = pd.to_numeric(recs09_mini['DOEID'])
recs09_mini['CDD65'] = pd.to_numeric(recs09_mini['CDD65'])
recs09_mini['HDD65'] = pd.to_numeric(recs09_mini['HDD65'])
recs09_mini['NWEIGHT'] = pd.to_numeric(recs09_mini['NWEIGHT'])
recs09_mini['REGIONC'] = pd.Categorical(recs09_mini['REGIONC']) 

recs09_mini

recs15_dfc = recs15_df.copy()
recs15_mini = recs15_dfc[['DOEID', 'REGIONC', 'HDD65', 'CDD65', 'NWEIGHT']]
recs15_mini['DOEID'] = pd.to_numeric(recs15_mini['DOEID'])
recs15_mini['HDD65'] = pd.to_numeric(recs15_mini['HDD65'])
recs15_mini['CDD65'] = pd.to_numeric(recs15_mini['CDD65'])
recs15_mini['NWEIGHT'] = pd.to_numeric(recs15_mini['NWEIGHT'])
recs15_mini['REGIONC'] = pd.Categorical(recs15_mini['REGIONC']) 

# ### part b)
# Separatley for 2009 and 2015, construct datasets containing just the **unique case ids** and the **replicate weights** (not the primary final weight) in a **“long” format** with one weight and residence per row.

recs15_UCID_RW = recs15_df[['DOEID']+['BRRWT' + str(i) for i in range(1,97)]]
recs15_UCID_RW_long = pd.melt(recs15_UCID_RW, id_vars = ['DOEID'], \
    value_name='Rep_Weight')
recs15_UCID_RW_long

repw09_mini = repw09_df[['DOEID'] + \
    ['brr_weight_' + str(i) for i in range(1,245)]]
recs09_UCID_RW_long = pd.melt(repw09_mini, id_vars = ['DOEID'], \
    value_name='NWEIGHT')
recs09_UCID_RW_long


# ## Question 2 - Construct and report the estimates [45 points]
# ### part a)
# Estimate the **average number of heating and cooling degree days** for 
# residences in **each Census region** for both 2009 and 2015. You should 
# construct both **point estimates (using the weights)** and **95% confidece 
# intervals (using standard errors estiamted with the repliacte weights)**. 
# Report your results in a nicely formatted table.
#
# For this question, you should use pandas DataFrame methods wherever possible. 
# Do not use a module specifically supporting survey weighting.

def w_avg(df, val, weights):
    v = df[val]
    w = df[weights]
    return (v * w).sum() / w.sum()


# +
# ========================
# for 2009 HDD

# point estimates (using the weights) 
HDD09_wm = (recs09_mini
               .groupby('REGIONC')
               [['HDD65']]
               .agg(w_avg,  'HDD65', 'NWEIGHT')
              )

sum_diff = HDD09_wm.copy()
sum_diff['HDD65'] = 0
R = 244
eps = 0.5

# 95% confidece intervals (using standard errors estiamted with the 
# repliacte weights)
for r in range(1,R+1):
    recs09_mini['Rep_Weight'] = repw09_mini[['brr_weight_' + str(r)]]
    HDD09_repw = (recs09_mini
                   .groupby('REGIONC')
                   [['HDD65']]
                   .agg(w_avg,  'HDD65', 'Rep_Weight')
                  )
    sum_diff = sum_diff + (HDD09_repw - HDD09_wm)**2

HDD09_est_var = 1/(R*(1-eps)**2) * sum_diff
HDD09_est_SE = HDD09_est_var.agg(np.sqrt)

level=0.95
z = norm.ppf(1 - (1 - level) / 2)
HDD09_lwr, HDD09_upr = HDD09_wm - z * HDD09_est_SE, HDD09_wm + z * HDD09_est_SE
# HDD09_lwr, HDD09_upr, HDD09_wm

# +
# ========================
# for 2009 CDD

# point estimates (using the weights) 
CDD09_wm = (recs09_mini
               .groupby('REGIONC')
               [['CDD65']]
               .agg(w_avg,  'CDD65', 'NWEIGHT')
              )

sum_diff = CDD09_wm.copy()
sum_diff['CDD65'] = 0
R = 244
eps = 0.5

# 95% confidece intervals (using standard errors estiamted with the 
# repliacte weights)
for r in range(1,R+1):
    recs09_mini['Rep_Weight'] = repw09_mini[['brr_weight_' + str(r)]]
    CDD09_repw = (recs09_mini
                   .groupby('REGIONC')
                   [['CDD65']]
                   .agg(w_avg,  'CDD65', 'Rep_Weight')
                  )
    sum_diff = sum_diff + (CDD09_repw - CDD09_wm)**2

CDD09_est_var = 1/(R*(1-eps)**2) * sum_diff
CDD09_est_SE = CDD09_est_var.agg(np.sqrt)

level=0.95
z = norm.ppf(1 - (1 - level) / 2)
CDD09_lwr, CDD09_upr = CDD09_wm - z * CDD09_est_SE, CDD09_wm + z * CDD09_est_SE
# CDD09_lwr, CDD09_upr, CDD09_wm

# +
# ========================
# for 2015 HDD

# point estimates (using the weights) 
HDD15_wm = (recs15_mini
               .groupby('REGIONC')
               [['HDD65']]
               .agg(w_avg,  'HDD65', 'NWEIGHT')
              )

sum_diff = HDD15_wm.copy()
sum_diff['HDD65'] = 0
R = 96
eps = 0.5

# 95% confidece intervals (using standard errors estiamted with the repliacte weights)
for r in range(1,R+1):
    recs15_mini['Rep_Weight'] = recs15_df[['BRRWT' + str(r)]]
    HDD15_repw = (recs15_mini
                   .groupby('REGIONC')
                   [['HDD65']]
                   .agg(w_avg,  'HDD65', 'Rep_Weight')
                  )
    sum_diff = sum_diff + (HDD15_repw - HDD15_wm)**2

HDD15_est_var = 1/(R*(1-eps)**2) * sum_diff
HDD15_est_SE = HDD15_est_var.agg(np.sqrt)

level=0.95
z = norm.ppf(1 - (1 - level) / 2)
HDD15_lwr, HDD15_upr = HDD15_wm - z * HDD15_est_SE, HDD15_wm + z * HDD15_est_SE
# HDD15_lwr, HDD15_upr, HDD15_wm

# +
# ========================
# for 2015 CDD

# point estimates (using the weights) 
CDD15_wm = (recs15_mini
               .groupby('REGIONC')
               [['CDD65']]
               .agg(w_avg,  'CDD65', 'NWEIGHT')
              )

sum_diff = CDD15_wm.copy()
sum_diff['CDD65'] = 0
R = 96
eps = 0.5

# 95% confidece intervals (using standard errors estiamted with the repliacte weights)
for r in range(1,R+1):
    recs15_mini['Rep_Weight'] = recs15_df[['BRRWT' + str(r)]]
    CDD15_repw = (recs15_mini
                   .groupby('REGIONC')
                   [['CDD65']]
                   .agg(w_avg,  'CDD65', 'Rep_Weight')
                  )
    sum_diff = sum_diff + (CDD15_repw - CDD15_wm)**2

CDD15_est_var = 1/(R*(1-eps)**2) * sum_diff
CDD15_est_SE = CDD15_est_var.agg(np.sqrt)

level=0.95
z = norm.ppf(1 - (1 - level) / 2)
CDD15_lwr, CDD15_upr = CDD15_wm - z * CDD15_est_SE, CDD15_wm + z * CDD15_est_SE
# CDD15_lwr, CDD15_upr, CDD15_wm

# +
# HDD multiple index name
HDDWM_idxn = ['HDD_wm'] *4
HDD09_wm.index = [HDDWM_idxn, HDD09_wm.index]
HDD15_wm.index = [HDDWM_idxn, HDD15_wm.index]

HDDLWR_idxn = ['HDD_lwr'] *4
HDD09_lwr.index = [HDDLWR_idxn, HDD09_lwr.index]
HDD15_lwr.index = [HDDLWR_idxn, HDD15_lwr.index]

HDDUPR_idxn = ['HDD_upr'] *4
HDD09_upr.index = [HDDUPR_idxn, HDD09_upr.index]
HDD15_upr.index = [HDDUPR_idxn, HDD15_upr.index]

# CDD multiple index name
CDDWM_idxn = ['CDD_wm'] *4
CDD09_wm.index = [CDDWM_idxn, CDD09_wm.index]
CDD15_wm.index = [CDDWM_idxn, CDD15_wm.index]

CDDLWR_idxn = ['CDD_lwr'] *4
CDD09_lwr.index = [CDDLWR_idxn, CDD09_lwr.index]
CDD15_lwr.index = [CDDLWR_idxn, CDD15_lwr.index]

CDDUPR_idxn = ['CDD_upr'] *4
CDD09_upr.index = [CDDUPR_idxn, CDD09_upr.index]
CDD15_upr.index = [CDDUPR_idxn, CDD15_upr.index]

# +
# rename columns
HDD09_wm = HDD09_wm.rename(columns={"HDD65": "09"})
HDD09_lwr = HDD09_lwr.rename(columns={"HDD65": "09"})
HDD09_upr = HDD09_upr.rename(columns={"HDD65": "09"})

HDD15_wm = HDD15_wm.rename(columns={"HDD65": "15"})
HDD15_lwr = HDD15_lwr.rename(columns={"HDD65": "15"})
HDD15_upr = HDD15_upr.rename(columns={"HDD65": "15"})

CDD09_wm = CDD09_wm.rename(columns={"CDD65": "09"})
CDD09_lwr = CDD09_lwr.rename(columns={"CDD65": "09"})
CDD09_upr = CDD09_upr.rename(columns={"CDD65": "09"})

CDD15_wm = CDD15_wm.rename(columns={"CDD65": "15"})
CDD15_lwr = CDD15_lwr.rename(columns={"CDD65": "15"})
CDD15_upr = CDD15_upr.rename(columns={"CDD65": "15"})

# +
# construct HDD 09
frames = [HDD09_wm, HDD09_lwr, HDD09_upr]
HDD_09 = pd.concat(frames)
HDD_09.index.names = ['HDD', 'REGIONC'] # rename the index

# construct HDD 15
frames = [HDD15_wm, HDD15_lwr, HDD15_upr]
HDD_15 = pd.concat(frames)
HDD_15.index.names = ['HDD', 'REGIONC']

# merge 09 15 HDD
HDD_result = pd.merge(HDD_09, HDD_15, on=['HDD','REGIONC'], how='left')
HDD_result

# +
# construct CDD 09
frames = [CDD09_wm, CDD09_lwr, CDD09_upr]
CDD_09 = pd.concat(frames)
CDD_09.index.names = ['CDD', 'REGIONC'] # rename the index
CDD_09

# construct CDD 15
frames = [CDD15_wm, CDD15_lwr, CDD15_upr]
CDD_15 = pd.concat(frames)
CDD_15.index.names = ['CDD', 'REGIONC']

# merge 09 15 CDD
CDD_result = pd.merge(CDD_09, CDD_15, on=['CDD','REGIONC'], how='left')
CDD_result

# +
# Combine HDD CDD
# Add Multi_idx to HDD
HDD_result_c = HDD_result.copy()

HDD_idxn = [tuple(['HDD'])] * 12
old_idxn = list(HDD_result.index)
new_idxn = np.concatenate((HDD_idxn, old_idxn), axis=1)
new_idxn = [tuple(i) for i in new_idxn]

index = pd.MultiIndex.from_tuples(new_idxn, names=['HDD/CDD', 'Point_Est/CI', \
    'REGIONC'])

HDD_result_c.index = index

# Add Multi_idx to CDD
CDD_result_c = CDD_result.copy()

CDD_idxn = [tuple(['CDD'])] * 12
old_idxn = list(CDD_result.index)
new_idxn = np.concatenate((CDD_idxn, old_idxn), axis=1)
new_idxn = [tuple(i) for i in new_idxn]

index = pd.MultiIndex.from_tuples(new_idxn, names=['CDD/CDD', 'Point_Est/CI', \
    'REGIONC'])

CDD_result_c.index = index
# -

frames = [HDD_result_c, CDD_result_c]
Final_Result_Frame = pd.concat(frames)
Final_Result_Frame

# ### part b)
# Using the estimates and standard errors from part a, estimate **the change** 
# in heating and cooling degree days between 2009 and 2015 for each Census 
# region. In constructing interval estimates, use the facts that the estimators 
# for each year are independent and that,

# point estimates (using the weights) 
HDD09_wm = (recs09_mini
               .groupby('REGIONC')
               [['HDD65']]
               .agg(w_avg,  'HDD65', 'NWEIGHT')
              )
# point estimates (using the weights) 
CDD09_wm = (recs09_mini
               .groupby('REGIONC')
               [['CDD65']]
               .agg(w_avg,  'CDD65', 'NWEIGHT')
              )
# point estimates (using the weights) 
HDD15_wm = (recs15_mini
               .groupby('REGIONC')
               [['HDD65']]
               .agg(w_avg,  'HDD65', 'NWEIGHT')
              )
# point estimates (using the weights) 
CDD15_wm = (recs15_mini
               .groupby('REGIONC')
               [['CDD65']]
               .agg(w_avg,  'CDD65', 'NWEIGHT')
              )

# +
# HDD change Point Estimate
HDD_diff_m = HDD15_wm - HDD09_wm

# variance
HDD_diff_v = HDD09_est_var + HDD15_est_var
HDD_diff_SE = HDD_diff_v.agg(np.sqrt)

# CI of HDD
level=0.95
z = norm.ppf(1 - (1 - level) / 2)
HDD_diff_lwr, HDD_diff_upr = HDD_diff_m - z * HDD_diff_SE, HDD_diff_m + z * HDD_diff_SE
# HDD_diff_lwr, HDD_diff_upr, HDD_diff_m

# +
# CDD change Point Estimate
CDD_diff_m = CDD15_wm - CDD09_wm

# variance
CDD_diff_v = CDD09_est_var + CDD15_est_var
CDD_diff_SE = CDD_diff_v.agg(np.sqrt)

# CI of CDD
level=0.95
z = norm.ppf(1 - (1 - level) / 2)
CDD_diff_lwr, CDD_diff_upr = CDD_diff_m - z * CDD_diff_SE, CDD_diff_m + z * CDD_diff_SE
# CDD_diff_lwr, CDD_diff_upr

# +
HDD_diff_lwr = HDD_diff_lwr.rename(columns={"HDD65": "Diff_lwr"})
HDD_diff_upr = HDD_diff_upr.rename(columns={"HDD65": "Diff_upr"})
HDD_diff_m = HDD_diff_m.rename(columns={"HDD65": "Diff_mean"})

HDD_diff_result = pd.merge(HDD_diff_m, HDD_diff_lwr, on=['REGIONC'], how='left')
HDD_diff_result = pd.merge(HDD_diff_result, HDD_diff_upr, on=['REGIONC'], how='left')

# HDD multiple index name
HDD_idxn = ['HDD'] *4
HDD_diff_result.index = [HDD_idxn, HDD_diff_result.index]
HDD_diff_result

# +
CDD_diff_lwr = CDD_diff_lwr.rename(columns={"CDD65": "Diff_lwr"})
CDD_diff_upr = CDD_diff_upr.rename(columns={"CDD65": "Diff_upr"})
CDD_diff_m = CDD_diff_m.rename(columns={"CDD65": "Diff_mean"})

CDD_diff_result = pd.merge(CDD_diff_m, CDD_diff_lwr, on=['REGIONC'], how='left')
CDD_diff_result = pd.merge(CDD_diff_result, CDD_diff_upr, on=['REGIONC'], how='left')

# CDD multiple index name
CDD_idxn = ['CDD'] *4
CDD_diff_result.index = [CDD_idxn, CDD_diff_result.index]
CDD_diff_result
# -

frames = [HDD_diff_result, CDD_diff_result]
Final_Diff_Frame = pd.concat(frames)
Final_Diff_Frame

# ## Question 3 - [20 points]
# Use pandas and/or matplotlib to create visualizations for the results reported as tables in parts a and b of question 2. As with the tables, your figures should be “polished” and professional in appearance, with well-chosen axis and tick labels, English rather than code_speak, etc. Use an adjacent markdown cell to write a caption for each figure.

# +
# for HDD of RECS_2009
HDD09_wm_Q3 = HDD09_wm.rename(columns={"HDD65": "wm"})
HDD09_SE_Q3 = HDD09_est_SE.rename(columns={"HDD65": "SE"})
HDD09_plot_df = pd.merge(HDD09_wm_Q3, HDD09_SE_Q3, on=['REGIONC'], how='left').reset_index()
HDD09_plot_df = HDD09_plot_df.rename(columns={"REGIONC": "REGIONC_HDD"})
HDD09_plot_df

# for CDD of RECS_2009
CDD09_wm_Q3 = CDD09_wm.rename(columns={"CDD65": "wm"})
CDD09_SE_Q3 = CDD09_est_SE.rename(columns={"CDD65": "SE"})
CDD09_plot_df = pd.merge(CDD09_wm_Q3, CDD09_SE_Q3, on=['REGIONC'], how='left').reset_index()
CDD09_plot_df = CDD09_plot_df.rename(columns={"REGIONC": "REGIONC_CDD"})
CDD09_plot_df

# for HDD of RECS_2015
HDD15_wm_Q3 = HDD15_wm.rename(columns={"HDD65": "wm"})
HDD15_SE_Q3 = HDD15_est_SE.rename(columns={"HDD65": "SE"})
HDD15_plot_df = pd.merge(HDD15_wm_Q3, HDD15_SE_Q3, on=['REGIONC'], how='left').reset_index()
HDD15_plot_df = HDD15_plot_df.rename(columns={"REGIONC": "REGIONC_HDD"})
HDD15_plot_df

# for CDD of RECS_2015
CDD15_wm_Q3 = CDD15_wm.rename(columns={"CDD65": "wm"})
CDD15_SE_Q3 = CDD15_est_SE.rename(columns={"CDD65": "SE"})
CDD15_plot_df = pd.merge(CDD15_wm_Q3, CDD15_SE_Q3, on=['REGIONC'], how='left').reset_index()
CDD15_plot_df = CDD15_plot_df.rename(columns={"REGIONC": "REGIONC_CDD"})
CDD15_plot_df

## figure 1
fig1, ax1 = plt.subplots(nrows=2, ncols=1, figsize=(15,10))
fig1.tight_layout()
# 2009
_ = ax1[0].scatter(
    data=HDD09_plot_df,
    x='wm',
    y='REGIONC_HDD',
    marker='s',
    color='RED'
    )
_ = ax1[0].errorbar(
    x=HDD09_plot_df['wm'], 
    y=HDD09_plot_df['REGIONC_HDD'],
    xerr=HDD09_plot_df['SE'] * 1.96,
    fmt='None',
    ecolor='red',
    capsize=5
    )

_ = ax1[0].scatter(
    data=CDD09_plot_df,
    x='wm',
    y='REGIONC_CDD',
    marker='s',
    color='blue'
    )
_ = ax1[0].errorbar(
    x=CDD09_plot_df['wm'], 
    y=CDD09_plot_df['REGIONC_CDD'],
    xerr=CDD09_plot_df['SE'] * 1.96,
    fmt='None',
    ecolor='blue',
    capsize=5
    )

# 2015
_ = ax1[1].scatter(
    data=HDD15_plot_df,
    x='wm',
    y='REGIONC_HDD',
    marker='s',
    color='RED'
    )
_ = ax1[1].errorbar(
    x=HDD15_plot_df['wm'], 
    y=HDD15_plot_df['REGIONC_HDD'],
    xerr=HDD15_plot_df['SE'] * 1.96,
    fmt='None',
    ecolor='red',
    capsize=5
    )

_ = ax1[1].scatter(
    data=CDD15_plot_df,
    x='wm',
    y='REGIONC_CDD',
    marker='s',
    color='blue'
    )
_ = ax1[1].errorbar(
    x=CDD15_plot_df['wm'], 
    y=CDD15_plot_df['REGIONC_CDD'],
    xerr=CDD15_plot_df['SE'] * 1.96,
    fmt='None',
    ecolor='blue',
    capsize=5
    )

_ = ax1[0].set_title('Mean and 95% CI for HDD and CDD of RECS_2009 and RECS_2015')
_ = ax1[0].set_ylabel('REGIONC')
_ = ax1[0].set_xlabel('Heating/Cooling degree days in 2009, base temperature 65F (unit: degree days)')
_ = ax1[0].legend(loc='upper right') 

_ = ax1[1].set_ylabel('REGIONC')
_ = ax1[1].set_xlabel('Heating/Cooling degree days in 2015, base temperature 65F (unit: degree days)')
_ = ax1[1].legend(loc='upper right')
# -

# The above plot is the **Mean and 95% CI for HDD and CDD of RECS_2009 and RECS_2015**.The upper one shows the estimation of datas from 2009 while the lower one shows that of 2015. As well as, the **Heating Degree Days** and the **Cooling Degree Days** are seperately assigned with **red** and **blue** color.

# +
# ====================
# Estimate the change in heating and cooling degree days between 2009 and 2015 for each Census region. 
# -

HDD_diff_SE = HDD_diff_SE.rename(columns={"HDD65": "HDD_diff_SE"})
HDD_diff_plot = pd.merge(HDD_diff_m, HDD_diff_SE, on=['REGIONC'], how='left').reset_index()
HDD_diff_plot = HDD_diff_plot.rename(columns={"REGIONC": "REGIONC_HDD"})
HDD_diff_plot

CDD_diff_SE = CDD_diff_SE.rename(columns={"CDD65": "CDD_diff_SE"})
CDD_diff_plot = pd.merge(CDD_diff_m, CDD_diff_SE, on=['REGIONC'], how='left').reset_index()
CDD_diff_plot = CDD_diff_plot.rename(columns={"REGIONC": "REGIONC_CDD"})
CDD_diff_plot

# +
## figure 1
fig2, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(14,5))
fig2.tight_layout()

_ = plt.scatter(
    data=HDD_diff_plot,
    x='Diff_mean',
    y='REGIONC_HDD',
    marker='s',
    color='RED'
    )
_ = plt.errorbar(
    x=HDD_diff_plot['Diff_mean'], 
    y=HDD_diff_plot['REGIONC_HDD'],
    xerr=HDD_diff_plot['HDD_diff_SE'] * 1.96,
    fmt='None',
    ecolor='red',
    capsize=5
    )

_ = plt.scatter(
    data=CDD_diff_plot,
    x='Diff_mean',
    y='REGIONC_CDD',
    marker='s',
    color='blue'
    )
_ = plt.errorbar(
    x=CDD_diff_plot['Diff_mean'], 
    y=CDD_diff_plot['REGIONC_CDD'],
    xerr=CDD_diff_plot['CDD_diff_SE'] * 1.96,
    fmt='None',
    ecolor='blue',
    capsize=5
    )
_ = ax2.set_title('Point estimate and CI of the change in heating and cooling degree days between 2009 and 2015')
_ = ax2.set_ylabel('REGIONC')
_ = ax2.set_xlabel('The change in heating and cooling degree days between 2009 and 2015 (unit: degree days)')
_ = ax2.legend(loc='lower right') 

# -

# The above plot is the **Point estimate and CI of the change in heating and cooling degree days between 2009 and 2015 for each Census region.**. The point estimate is given by the squares in plot and the error bars indicating the CI of change. The same as the former plot, the **Heating Degree Days** and the **Cooling Degree Days** are seperately assigned with **red** and **blue** color.


