"""
Created on Wed Aug  5 11:59:34 2020

@author: david
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import scipy.stats

def r2_score(x,y):
    
    x = x.values.reshape(-1,1) # reshape into 2D array
    y = y.values.reshape(-1,1) # reshape into 2D array
    
    "If using standard least squares regression"
    regressor = LinearRegression()  
    regressor.fit(x, y) # training the algorithm

    print(regressor)
    r2_score = regressor.score(x, y)
    
    return r2_score


normalize_RF = True
k = 20

path = "./EM-test_k20_mu0.1_L10000_varRho0.1-5.0/"
#file = "./arg-sampler-test_k20_mu0.1_prevTrees_gammaNatural/arg-sampler-test_k20_mu0.1_trueTrees_altRecRate_results.csv"
results_file = path + "EM-test_k20_mu0.1_bestTrueReference_results.csv"
df = pd.read_csv(results_file) # index_col=0)

sns.set(style="darkgrid")
#sns.color_palette("husl", 4)

"""
    Filter out cases where we inferred no recombination events
"""
zero_ests = df.index[df['Inferred Recomb Events'] == 0]
#df = df[df['Inferred Recomb Events'] > 0]
df = df[df['Rho Estimate'] < 6.0]

"""
    Compute error/bias in estimates
"""
df['Rate Estimate Error'] = df['Rho Estimate'] - df["True Rho"]
df['Rec Event Error'] = df['Inferred Recomb Events'] - df['True Recomb Events']


"""
    Regress estimates against true recomb rates
"""
fig, ax = plt.subplots(figsize=(5,4))
title = 'EM-test_k20_mu0.1_L10000_varRho0.1-5.0_true-vs-est_recRates.png'
sns.regplot(x="True Rho", y="Rho Estimate", data=df,fit_reg=False)
ax.set_xlabel('True rate $r$')
ax.set_ylabel('Estimated rate $r$')
xy_min = min(ax.get_xlim()[0],ax.get_ylim()[0])
xy_max = max(ax.get_xlim()[1],ax.get_ylim()[1])
ax.set_xlim([xy_min,xy_max])
ax.set_ylim([xy_min,xy_max])
x = np.linspace(xy_min, xy_max, 10)
ax.plot(x, x, '-k') # dashdot black
r = scipy.stats.pearsonr(df["True Rho"].values, df["Rho Estimate"].values)
r_str = '%.2f' % r[0]
ax.text(0, ax.get_ylim()[1]*0.9, r"$R = $" + r_str, fontsize=12)
bias_str = '%.2f' % df['Rate Estimate Error'].mean()
ax.text(0, ax.get_ylim()[1]*0.8, r"$Bias = $" + bias_str, fontsize=12)
fig.tight_layout()
fig.savefig(title, dpi=200)

"""
    Regress true vs. estimated number of rec events
"""
fig, ax = plt.subplots(figsize=(5,4))
title = 'EM-test_k20_mu0.1_L10000_varRho0.1-5.0_true-vs-est_recEvents.png'
sns.regplot(x='True Recomb Events', y='Inferred Recomb Events', data=df,fit_reg=False)
ax.set_xlabel('True rec events')
ax.set_ylabel('Estimated rec events')
xy_min = min(ax.get_xlim()[0],ax.get_ylim()[0])
xy_max = max(ax.get_xlim()[1],ax.get_ylim()[1])
ax.set_xlim([xy_min,xy_max])
ax.set_ylim([xy_min,xy_max])
x = np.linspace(xy_min, xy_max, 10)
ax.plot(x, x, '-k') # dashdot black
r = scipy.stats.pearsonr(df["True Recomb Events"].values, df["Inferred Recomb Events"].values)
r_str = '%.2f' % r[0]
ax.text(0, ax.get_ylim()[1]*0.9, r"$R = $" + r_str, fontsize=12)
bias_str = '%.2f' % df['Rec Event Error'].mean()
ax.text(0, ax.get_ylim()[1]*0.8, r"$Bias = $" + bias_str, fontsize=12)
fig.tight_layout()
fig.savefig(title, dpi=200)


"""
    Regress rate estimate error against rec event error
"""
fig, ax = plt.subplots(figsize=(5,4))
title = 'EM-test_k20_mu0.1_L10000_varRho0.1-5.0_rateError-vs-eventError_recRates.png'
sns.regplot(x="Rec Event Error", y="Rate Estimate Error", data=df,fit_reg=False)
ax.set_xlabel('Rec Event Error')
ax.set_ylabel('Rate Estimate Error')
r = scipy.stats.pearsonr(df["Rec Event Error"].values, df["Inferred Recomb Events"].values)
r_str = '%.2f' % r[0]
ax.text(ax.get_xlim()[0]*0.8, ax.get_ylim()[1]*0.9, r"$R = $" + r_str, fontsize=12)
fig.tight_layout()
fig.savefig(title, dpi=200)

"""
    If want to report R^2 instead
"""
#r2_str = '%.2f' % r2_score(df["True Rho"],df["Rho Estimate"])
#ax.text(0, ax.get_ylim()[1]*0.9, r"$R^2 = $" + r2_str, fontsize=12)


