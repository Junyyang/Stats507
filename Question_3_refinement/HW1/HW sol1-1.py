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

# STATS 507
# Junyuan Yang
# HW1

# ## GSI Instructions
# ---
# - -10 for missing .py file
# - Q1: -3 for no both raw and formatted versions.
# - Q3: -6 for no interval for CP and Jeffery method.
# - Overall: -10 for no docstring

# ## Correction
# ---
# - .py file has been created and added
# - The raw markdown has been added
# - Adding docstring for each function
# - for no intervall of CP and Jeffery method: 
#    correct the beta.pdf to beta.ppf 
# ---

# ## Question 0
#
# This is *question 0* for [problem set 1](https://jbhender.github.io/Stats507/F21/ps/ps1.html) of [Stats 507](https://jbhender.github.io/Stats507/F21/)
#
# The next question is about the **Fibonacci sequence**, $F_n = F_{n-2} +F_{n-1}$. In part **a** we will define a Pythopn function `fib_rec()`.
#
# Below is a ...
#
# ### Level 3 Header
#
# Next, we can make a bulleted list:
# * Item 1
#     - detail 1
#     - detail 2
# * Item 2
#
# Finally, we can make an enumerated list:
# 1. Item 1
# 2. Item 2
# 3. Item 3

# ---
# The raw markdown is added by correcting
# ```
# This is *question 0* for [problem set 1](https://jbhender.github.io/Stats507/F21/ps/ps1.html) of [Stats 507](https://jbhender.github.io/Stats507/F21/)
#
# The next question is about the **Fibonacci sequence**, $F_n = F_{n-2} +F_{n-1}$. In part **a** we will define a Pythopn function `fib_rec()`.
#
# Below is a ...
#
# ### Level 3 Header
#
# Next, we can make a bulleted list:
# * Item 1
#     - detail 1
#     - detail 2
# * Item 2
#
# Finally, we can make an enumerated list:
# 1. Item 1
# 2. Item 2
# 3. Item 3
# ```
# ---

# +
import math
import numpy as np
import pandas as pd
from timeit import Timer
from collections import defaultdict

import scipy.stats as stats
from scipy.stats import norm, binom, beta


# -

# ---
# ## Question 1

# a. fib_rec()
def fib_rec(n, a = 0, b = 1):
    """
    Computing the Fibonacci number $F_n$, where $F_0 = a$ and $F_1 = b$.
    Using the recursive function
    
    Parameters input
    ------------
    n : int
        The aimming index for Fibonacci sequence $F_n$.
    a, b: int, optional
        The initiation of Fibonacci sequence $F_0 = a$ and $F_1 = b$
    
    Returns output
    ------------
    The n-th element of Fibonacci sequence $F_n$
    """
    if n >= 2:
        return fib_rec(n-2)+fib_rec(n-1)
    elif n == 0:
        return a #  F_0 = a
    elif n == 1:
        return b #  F_1 = b


print(fib_rec(7))
print(fib_rec(11))
print(fib_rec(13))


# b. fib_for()
def fib_for(n, a = 0, b = 1):
    """
    Computing the Fibonacci number $F_n$, where $F_0 = a$ and $F_1 = b$.
    Using the 'for' loop
    
    Parameters input
    ------------
    n : int
        The aimming index for Fibonacci sequence $F_n$.
    a, b: int, optional
        The initiation of Fibonacci sequence $F_0 = a$ and $F_1 = b$
    
    Returns output
    ------------
    The n-th element of Fibonacci sequence $F_n$
    """
    pre = a #  F_0 = a
    cur = b #  F_1 = b
    try:
        n >= 2     
        for i in range(n - 1):
            new = cur + pre # Fn−2+Fn−1
            pre = cur
            cur = new
        return new
    except:
        print("n should be greater than 1")


print(fib_for(7))
print(fib_for(11))
print(fib_for(13))


# c. fib_whl()
def fib_whl(n, a = 0, b = 1):
    """
    Computing the Fibonacci number $F_n$, where $F_0 = a$ and $F_1 = b$.
    Using the 'while' loop
    
    Parameters input
    ------------
    n : int
        The aimming index for Fibonacci sequence $F_n$.
    a, b: int, optional
        The initiation of Fibonacci sequence $F_0 = a$ and $F_1 = b$
    
    Returns output
    ------------
    The n-th element of Fibonacci sequence $F_n$
    """
    pre = a #  F_0 = a
    cur = b #  F_1 = b
    try:
        n >= 2     
        while(n>=2):
            new = cur + pre # Fn−2+Fn−1
            pre = cur
            cur = new
            n -= 1
        return new
    except:
        return None
#         print("n should be greater than 1")


print(fib_whl(7))
print(fib_whl(11))
print(fib_whl(13))


# d. fib_rnd()
def fib_rnd(n, a = 0, b = 1):
    """
    Computing the Fibonacci number $F_n$, where $F_0 = a$ and $F_1 = b$.
    Using the rounding method
    
    Parameters input
    ------------
    n : int
        The aimming index for Fibonacci sequence $F_n$.
    a, b: int, optional
        The initiation of Fibonacci sequence $F_0 = a$ and $F_1 = b$
    
    Returns output
    ------------
    The n-th element of Fibonacci sequence $F_n$
    """
    phi = (1+np.sqrt(5))/2
    try:
        n >= 0
        result = round( phi**n / np.sqrt(5) )
        return result
    except:
        print("n should be greater than 0")


print(fib_rnd(7))
print(fib_rnd(11))
print(fib_rnd(13))


# d. fib_flr()
def fib_flr(n, a = 0, b = 1):
    """
    Computing the Fibonacci number $F_n$, where $F_0 = a$ and $F_1 = b$.
    Using the truncation method
    
    Parameters input
    ------------
    n : int
        The aimming index for Fibonacci sequence $F_n$.
    a, b: int, optional
        The initiation of Fibonacci sequence $F_0 = a$ and $F_1 = b$
    
    Returns output
    ------------
    The n-th element of Fibonacci sequence $F_n$
    """
    phi = (1+np.sqrt(5))/2
    try:
        n >= 0
        result = math.floor(phi**n / np.sqrt(5) + 1/2)
        return result
    except:
        print("n should be greater than 0")


print(fib_flr(7))
print(fib_flr(11))
print(fib_flr(13))

# +
# f. time comsuming comparison
n = 30
a = 0
b = 1

# timing with ndarray input: -------------------------------------------------
a = np.asarray(a)
b = np.asarray(b)
n = np.asarray(n)
time_nda = defaultdict(list)

for f in [fib_rec, fib_for, fib_whl, fib_rnd, fib_flr]:
    
    tm_list = []

    t = Timer('f(n, a, b)', globals={'f': f, 'n': n, 'a': a, 'b': b})
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

# ---
# ## Question 2 - Pascal’s Triangle

def cal_PT_row(n):
    """
    Computing the n-th row of Pascal's Trianle
    
    Parameters input
    ------------
    n : int
        The aimming index for the row of Pascal's Trianle.
    
    Returns output
    ------------
    The array of the n-th row of Pascal's Trianle.
    """
    nk_array = np.asarray([1])
    for k in range(1,n+1):
        current = int( nk_array[k-1]*(n+1-k)/k )
        nk_array = np.concatenate( (nk_array, np.asarray([current])), axis=0)
    return nk_array


PT_row = cal_PT_row(5)
print(PT_row)


# +
def Num_to_Str(row):
    """
    Turn the array of row to string
    
    Parameters input
    ------------
    row : np.ndarray
        The aimming row for format transfer.
    
    Returns output
    ------------
    The string of the input row.
    """
    row_list = []
    for i in range(len(row)):
        row_list.append(str( row[i] ))
    row_string = '   '.join(row_list)
    return row_string

def print_PT(n):
    width = 5*n + 2
    
    for i in range(0, n+1):
        row = cal_PT_row(i)
        print(Num_to_Str(row).center(width))

print_PT(10)


# -

# ---
# ### Question 3 Statistics 101

# Pr3. a
def point_interv_est(data, level, ci_format):
    """
    Calculating the CI of given data and level of confidence.
    Output the result matching the specified format.
    
    Parameters input
    ------------
    data : np.ndarray
        The data to be estimated
    level: float
        The desired confidence level, converted to a percent in the output.
    ci_format: string
    
    Returns output
    ------------
    The point interval estimate of a given data and level in the certain format
    """
    dic = dict.fromkeys(['est', 'lwr', 'upr', 'level'])
    try:
        type(data) == np.ndarray
        
        if ci_format == None:
            return dic
        else:     
            z = stats.t.ppf(level, len(data)) # confidence level
            x_mean = np.mean(data)
            se = np.std(data)

            point_est = x_mean
            lwr, upr = x_mean - z * se , x_mean + z * se

            string = "{:.2f} [{:.2f}% CI: ({:.3f} , {:.3f})]"
            result = string.format(point_est, level, lwr, upr)

            return result
        
    except:
        print("data should be a numpy array")
        return 0


# +
# Pro3. b

# n trials
# x be the number of successes in thes trials

def point_interv_est2(data, level, method, ci_format='string'):
    """
    Calculating the CI of given data and level of confidence.
    Output the result matching the specified format.
    
    Parameters input
    ------------
    data : np.ndarray
        The data to be estimated
    level: float
        The desired confidence level, converted to a percent in the output.
    method: string
        The type of confidence interval and point estimate desired.
    ci_format: string, optional
    
    Returns output
    ------------
    The point interval estimate of a given data and level with a specified method.
    The output is organized in a certain format.
    """
    dic = dict.fromkeys(['est', 'lwr', 'upr', 'level'])
    try:
        type(data) == np.ndarray
        
        if ci_format == None:
            return dic
        else:     
            # z = stats.t.ppf(level, len(data)) #  Gaussian multiplier
            z = norm.ppf(1 - (1 - level) / 2)
            x_mean = np.mean(data)
            # se = np.std(data)
            n = len(data)
            se = np.sqrt(x_mean * (1 - x_mean) / n)
            string = "{:.2f} [{:.2f}% CI: ({:.3f} , {:.3f})]"
            x = len(data.nonzero()[0])  # number of nonzero elements
            # could be replace by sum for only 0/1 exists
            p_hat = x/n
            
            # ====================
            # Normal theory
            if method == 'Normal theory':
                point_est = x_mean
                lwr, upr = x_mean - z * se , x_mean + z * se

                result = string.format(point_est, level, lwr, upr)
                return result
            
            # ====================
            # Normal approximation
            if method == 'Normal approximation':
                p_hat = x/n
                if n*p_hat <12 or n*(1-p_hat) < 12:
                    print("warning that approximation could not be conventionally considered adequate")
                else:
                    point_est = p_hat
                    lwr = p_hat - z * np.sqrt(p_hat*(1-p_hat)/n) 
                    upr = p_hat + z * np.sqrt(p_hat*(1-p_hat)/n) 
            
                    result = string.format(point_est, level, lwr, upr)
                    return result
                
            # ====================
            # Clopper_Pearson interval
            elif method == 'Clopper_Pearson interval':
                # point_est = p_hat
                print('current method is Clopper_Pearson interval')
                s = np.sum(data)
                
                alpha = 1- level #1- confidence
                
                lwr = beta.ppf(alpha/2, s, n-s+1)
                upr = beta.ppf(1-alpha/2, s+1, n-s)
                
                result = string.format(x_mean, level, lwr, upr)
                return result
            
            # ====================
            # Jeffrey interval
            elif method == "Jeffrey interval":
                # point_est = p_hat
                alpha = 1- level #1- confidence
                s = np.sum(data)
                lwr = beta.ppf(alpha/2, s + 0.5, n - s + 0.5)
                upr = beta.ppf(1 - alpha/2, s + 0.5, n - s + 0.5)
                
                result = string.format(x_mean, level, lwr, upr)
                return result
            
            # ====================
            # Agresti_Coull interval 
            elif method == "Agresti_Coull interval":
                
                n_cur = n + z**2
                p_cur = (x + z**2 / 2)/n_cur
                
                n = n_cur
                p_hat = p_cur
                if n*p_hat <12 or n*(1-p_hat) < 12:
                    print("warning that approximation could not be conventionally considered adequate")
                else:
                    point_est = p_hat
                    lwr = p_hat - z * np.sqrt(p_hat*(1-p_hat)/n) 
                    upr = p_hat + z * np.sqrt(p_hat*(1-p_hat)/n) 
            
                    result = string.format(point_est, level, lwr, upr)
                    return result
        
    except:
        print("data should be a numpy array 22")


# -

array_one = np.ones(42)
array_zero = np.zeros(48)
data_array = np.concatenate( (array_one, array_zero), axis=0)

# +
df=pd.DataFrame(columns={"Methods":"","Point and Interval Estimates Results":""},index=[0])

for level in [0.9, 0.95, 0.99]:
    
    print("Confidence level is {:.2f}%".format(100*level) )
    df=pd.DataFrame(columns={"Methods":"","Point and Interval Estimates Results":""},index=[0])
    k = 0
    
    for method in ['Normal theory', 'Normal approximation', 'Clopper_Pearson interval',\
               "Jeffrey interval", "Agresti_Coull interval"]:
        result = point_interv_est2(data_array, level, method)
        df.loc[k]=[method,result]
        k += 1
    print(df)
    print("")
