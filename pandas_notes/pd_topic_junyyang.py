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

# ---
# Name: Junyuan Yang
#
# UM email: junyyang@umich.edu
#

# ---
# Extract the code from PS4 Q0
#
# ## Windows Rolling
#
# Return a rolling object allowing summary functions to be applied to windows of length n.
# By default, the result is set to the right edge of the window. This can be changed to the center of the window by setting center=True.
# Each points' weights could be determined by win_type shown in windows function, or evenly weighted as default.

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
