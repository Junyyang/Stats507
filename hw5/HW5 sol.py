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

# +
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

# OLS GLM
import statsmodels.api as sm
import statsmodels.formula.api as smf
from collections import defaultdict
from scipy.stats import chi2_contingency, ttest_ind
from scipy.stats import norm, beta

# Resampling
from os.path import exists
from scipy.stats import t, bootstrap

# B_Spline
from patsy import dmatrices, dmatrix, demo_data
# -

# ## Question 0 - R-Squared Warmup [20 points]
#
# In this question you will fit a model to the **ToothGrowth data**
# used in the notes on Resampling and Statsmodels-OLS. 
# - Read the data
# - log transform tooth length,
# - fit a model with independent variables for supplement type, 
# **dose (as categorical)**, and their interaction. 
#
# Demonstrate how to compute the R-Squared and 
# Adjusted R-Squared values and compare your 
# computations to the attributes (or properties) 
# already present in the result object.

# tooth growth data
file = 'tooth_growth.feather'
if exists(file):
    tg_data = pd.read_feather(file)
else: 
    tooth_growth = sm.datasets.get_rdataset('ToothGrowth')
    #print(tooth_growth.__doc__)
    tg_data = tooth_growth.data
    tg_data.to_feather(file)
# tg_data

# +
tg_data['log_len'] = tg_data[['len']].transform(np.log)
tg_data['dose_cat'] = pd.Categorical(tg_data['dose'])

tg_data['OJ'] = pd.get_dummies(tg_data['supp'])['OJ']
# -

# Fit the model with supplement type, dose (as categorical), and their 
# interaction.
mod1 = sm.OLS.from_formula('log_len ~ OJ*dose_cat', data=tg_data)
res1 = mod1.fit()
res1.summary2()

# - The R-square can be computed by the division of the sum of squares due to 
# regression $SS_{regression}$ and total sum of squares $SS_{total}$,
# $$R^2 = \frac{SS_{regression}}{SS_{total}}$$
# where $SS_{regression} = \sum{(y_{predict} - y_{mean})^2}$
# and $SS_{total} = \sum{(y_{observe} - y_{mean})^2}$
#
# - The adjusted R-square could be derived by modifing R-square
# $Adusted\_R^2 = 1- \frac{(1-R^2) \cdot (n-1)}{n-k-1}$, with n is 
# the number of samples and k is the number of variables

# +
# Demonstrate how to compute the R-Squared and Adjusted R-Squared values 
# and compare your computations to the presented in the result object.

# Presented R-Squared and Adjusted R-Squared values 
print('Presented R-squared value is', res1.rsquared)
print('Presented Adjusted R-squared value is', res1.rsquared_adj)

# How to compute R-Squared and Adjusted R-Squared values 
y_hat, r = res1.predict(), res1.resid
X = mod1.exog

y = y_hat + r # y_observation
y_bar = np.sum(y)/len(y)          # or sum(y)/len(y)
SSReg = np.sum(np.square(np.subtract(y_hat,y_bar)))
SST = np.sum(np.square(np.subtract(y,y_bar)))
Rsquared = SSReg/SST
print('The calculated R-squared is', Rsquared)

adj_rsquared = 1 - (1-Rsquared)*(len(y_hat) - 1) / (len(y_hat) - X.shape[1] - 1)
print('The calculated adj_rsquared is', adj_rsquared)
# -

# ## Question 1 - NHANES Dentition [50 points]
#
# In this question you will use the NHANES dentition and demographics data 
# from problem sets 2 and 4.
#
# ### Prob.a [30 points] 
# - Pick a single tooth (OHXxxTC) and model the probability that a permanent 
# tooth is present (look up the corresponding statuses) as a function of 
# **age** using logistic regression.
# - For simplicity, assume the data are iid and 
# ignore the survey weights and design.
# - Use a B-Spline basis to allow the probability to vary smoothly with age. 
# - Perform model selection using **AIC** (or another method) to **choose the 
# location of knots** and **the order of the basis** (or just use degree=3 
# (aka order) and focus on knots).
#
# Control for other demographics included in the data as warranted. 
# - You may also select these by minimizing AIC 
# or you may choose to include some demographics regardless of whether they 
# improve model fit. 
# - Describe your model building decisions and/or selection process and the 
# series of models fit.
#
# Update October 27: When placing knots, be careful not to place knots at 
# ages below (or equal to) the minimum age at which the tooth you are modeling 
# is present in the data. Doing so will lead to an issue known as perfect 
# separation and make your model non-identifiable. To make the assignment 
# easier you may (but are not required to) limit the analyses to those 
# age 12 and older and use no knots below age 14.
#
#

# +
# Construction of Demo and Ohx refers to HW2
demo_file = './demo_comb_df.pkl'
demo_df = pd.read_pickle(demo_file)

ohx_file = './oral_comb_df.pkl'
ohx_df = pd.read_pickle(ohx_file)

seed = 2021 * 11 * 3
# -

df = demo_df[['id','age']]
# Select a signle tooth "OHX02TC"
df = pd.merge(df, ohx_df[['id','tc_02']], on='id', how='left')

# +
# limit the analyses to those age 12 and older and use no knots below age 14.
df = df.query('age >= 12')

# Dependent Variable: 
# a permanent tooth is present (look up the corresponding statuses)
# Choose the upper right 2nd molar
permanent_tooth_present = 'Permanent tooth present'
df['tc02_Perm_Pre'] = (df['tc_02']
                      .apply(lambda x: x == permanent_tooth_present)
                      .replace({np.nan: False})
                     )

# Turn True and False to 1/0
df['tc02_Perm_Pre'] = df['tc02_Perm_Pre'].replace(
    {True: 1,
     False: 0
    })
# -

# model 0
mod0 = smf.logit('tc02_Perm_Pre~bs(age, df=5, degree=3)', data=df)
res0 = mod0.fit(disp=True)
res0.summary()

df['predict'] = mod0.predict(params = res0.params, exog=mod0.exog)
Plot_df = df[['age', 'predict']].sort_values(by=['age']).drop_duplicates()
x_var = np.array(Plot_df['age'])
y_var = np.array(Plot_df['predict'])
plt.plot(x_var, y_var, color='k')
plt.xlabel('Age')
plt.ylabel('Probability of permanent tooth tc_02 present')

aic_list = []
knot_min = 5
knot_max = 20
res_best = np.inf
for knot in range(knot_min,knot_max):
    mod = smf.logit('tc02_Perm_Pre~bs(age, df=(knot-1), degree=3)', data=df)
    res = mod.fit(disp=False)
    if res.aic < res_best:
        res_best = res.aic
        knot_best = knot

print('the best knot for GLM is ', knot_best)

# When the `knots=9`, the AIC is the best among `knots=5~20`. So that, 
# choose the best model as with `knots=8`.

# ### Prob.b [10 points] 
# Fit the best model you find in part a to all other teeth in the data and 
# create columns in your DataFrame for the fitted values.
#
# Update October 27: Leave the demographics alone, but if you are not 
# restricting to those 12 and older you may need to modify the locations 
# of the knots to make the models identifiable.
#
#

# +
# Select all other tooth
all_tooth_df = pd.merge(demo_df[['id','age']], ohx_df, on='id', how='left')
all_tooth_df = all_tooth_df.query('age >= 12')

permanent_tooth = 'Permanent tooth present'
for col in all_tooth_df.columns:
    if ('tc' in col) and ('ctc' not in col):
        all_tooth_df[col] = (all_tooth_df[col]
                              .apply(lambda x: x == permanent_tooth)
                              .replace({np.nan: False})
                             )
        
        # Turn True and False to 1/0
        all_tooth_df[col] = all_tooth_df[col].replace(
            {True: 1,
             False: 0
            })
        # print(col)
        mod1 = smf.logit(col+'~bs(age, df=knot_best-1, degree=3)', 
                         data=all_tooth_df)
        res1 = mod1.fit(disp=False)
        all_tooth_df[col+'pred'] = mod1.predict(params = res1.params)
# all_tooth_df
# -

all_tooth_df

# ### Prob.c [10 points] 
# Create a visualization showing how the predicted probability that a permanent 
# tooth is present varies with age for each tooth.
#
# clean up axes and present what is showing

# Set the position
position = (
    list(range(1,9))+
    list(reversed(range(9,17)))+
    list(range(17,25))+
    list(reversed(range(25,33)))
)
tooth_names = (
    '3rd Molar', '2nd Molar', '1st Molar',
    '2nd biscuspid', '1st biscuspid', 'cuspid',
    'lateral incisor', 'central incisor'
)
areas = ('upper right', 'upper left', 'lower left', 'lower right')

fig, ax = plt.subplots(nrows=8, ncols=4, sharex=True, sharey=True)
fig.set_size_inches(16,24)
for i in range(32):
    r = (position[i] -1)%8
    c = i //8
    
    pred_col = 'tc_' + str(i+1).zfill(2) + 'pred'
    Plot_df = (all_tooth_df[['age', pred_col]]
               .sort_values(by=['age'])
               .drop_duplicates()
              )
    
    x_var = np.array(Plot_df['age'])
    
    y_var = np.array(Plot_df[pred_col])
    ax[r, c].plot(x_var, y_var)
    
    if r == 0:
        ax[r,c].set_title(areas[c])
    if c == 0:
        ax[r,c].set_ylabel(tooth_names[r])

# ## Question 2 - Hosmer-Lemeshow Calibration Plot [30 points]
#
# In this question you will construct a plot often associated with the 
# Hosmer-Lemeshow goodness-of-fit test. The plot is often used to assess 
# the calibration of a generalized linear models across the range of predicted 
# values. Specifically, it is used to assess if the expected and observed 
# means are approximately equal across the range of the expected mean.
#
# Use the tooth you selected in question 1 part a for this question.

# - Split the data into deciles based on the fitted (aka predicted) 
# probabilities your model assigns to each subject’s tooth. The 10 groups 
# you create using deciles should be approximately equal in size.
#
# - Within each decile, compute the observed proportion of cases with a 
# permanent tooth present and the expected proportion found by averaging 
# the probabilities.

# +
df['predict_decile'] = np.multiply(np.round(df['predict'],1),10)
df['predict_decile'] = pd.to_numeric(df['predict_decile'] , downcast='integer')
observed_prop = (
    df
    .groupby('predict_decile')[['tc02_Perm_Pre']]
    .mean()
)

expected_prop = (
    df
    .groupby('predict_decile')[['predict']]
    .mean()
)
# -

observed_prop

expected_prop

# - Create a scatter plot comparing the observed and expected probabilities 
# within each decile and add a line through the origin with slope 1 as a guide. 
# Your model is considered well-calibrated if the points in this plot fall 
# approximately on this line.

x_var = np.array(observed_prop['tc02_Perm_Pre'])
y_var = np.array(expected_prop['predict'])
plt.scatter(x=x_var, y=y_var, color='blue')
plt.plot([0.0, 1.0], [0.0, 1.0], color='red')

# Calculate the T-test for the means of two independent samples of scores.
p = np.round(ttest_ind(x_var, y_var)[1],4)
p

# - Briefly comment on how-well calibrated your model is (or is not).
#
# The model is well-calibrated for the sattered points above approximately lie 
# around the line. The p-value for the observed probability and the predicted 
# probability is 0.9982 indicating the well-calibration.








