"""
Created on Wed Aug  5 11:59:34 2020

@author: david
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

normalize_RF = True
k = 20

file = "./arg-sampler-test_k20_mu0.1_prevTrees_gammaNatural/arg-sampler-test_k20_mu0.1_trueTrees_altRecRate_results.csv"
df = pd.read_csv(file) # index_col=0)

"Relabel"
df['Method'] = df['Method'].replace({'ARG Sampler':'Espalier'})

"Only take results for Espalier"
df = df[df['Method'] == 'Espalier']

sns.set(style="darkgrid")
#sns.color_palette("husl", 4)

fig, ax = plt.subplots(figsize=(5,4))
title = 'arg-sampler-test_k20_mu0.1_gammaNatural_trueTrees_altRecRate_informativeSites_vs_RFDists.png'
if normalize_RF:
    norm_factor = 2*(k-2) # sum of internal branches in both trees
    df['RF Dist'] = df['RF Dist'] / norm_factor
sns.regplot(x="Informative Sites", y="RF Dist", data=df,fit_reg=True)
ax.set_xlabel('Informative sites')
ax.set_ylabel('Normalized RF Distance')
fig.tight_layout()
fig.savefig(title, dpi=200)

fig, ax = plt.subplots(figsize=(5,4))
title = 'arg-sampler-test_k20_mu0.1_gammaNatural_trueTrees_altRecRate_proportionZeroBranches_vs_RFDists.png'
if normalize_RF:
    norm_factor = 2*(k-2) # sum of internal branches in both trees
    df['RF Dist'] = df['RF Dist'] / norm_factor
sns.regplot(x="Proportion Zero Branches", y="RF Dist", data=df,fit_reg=True)
ax.set_xlabel('Proportion Zero Branches')
ax.set_ylabel('Normalized RF Distance')
fig.tight_layout()
fig.savefig(title, dpi=200)


