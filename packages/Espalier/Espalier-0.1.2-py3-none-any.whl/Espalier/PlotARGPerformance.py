"""
Created on Wed Aug  5 11:59:34 2020

@author: david
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

normalize_RF = True
k = 20

#file = "arg-sampler-test_k10_mu0.01_branchAndBound_REFMAF_results.csv"
path = '/Volumes/GoogleDrive/My Drive/Espalier-Project/sim-results/'
file = path + "20210827-arg-sampler-test_k20_mu0.1_prevTrees_gammaNatural/arg-sampler-test_k20_mu0.1_bestTrueReference_results.csv"
df = pd.read_csv(file) # index_col=0)

"""
    Drop consensus results from df for SPR distances since these are always zero
"""
df.drop(df[df['Method'] == 'Consensus'].index, inplace=True)

"Relabel"
df['Method'] = df['Method'].replace({'ARG Sampler':'Espalier'})

sns.set(style="darkgrid")
#sns.color_palette("husl", 4)

"""
    Plot RF distances to true local trees
"""
fig, ax = plt.subplots(figsize=(5,4))
title = 'arg-sampler-test_k20_mu0.1_gammaNatural_bestTrueReference_RFDists.png'
if normalize_RF:
    norm_factor = 2*(k-2) # sum of internal branches in both trees
    df['RF Dist'] = df['RF Dist'] / norm_factor
sns.boxplot(x="Method", y="RF Dist", data=df, width=.4,fliersize=0,order=['Espalier','ARGWeaver','ML Tree'],palette="Set2")
ax.set_ylabel('Normalized RF Distance')
ax.set_ylim([ax.get_ylim()[0],1])
#sns.boxplot(x="Method", y="RF Dist", data=df,whis=[0, 100], width=.4,order=['ML Tree','ARGWeaver','ARG Sampler','Consensus']) # palette="vlag")
#sns.catplot(x="Method",y="RF Dist",kind="violin",inner="box",order=['ML Tree','ARGWeaver','ARG Sampler','Consensus'],cut=0, data=df)
#sns.stripplot(x="Method", y="RF Dist", data=df, size=2, color=".3", linewidth=0, order=['ML Tree','ARGWeaver','ARG Sampler','Consensus'])
fig.tight_layout()
fig.savefig(title, dpi=200)

"""
    Plot weighted RF distances to true local trees
"""
#fig, ax = plt.subplots(figsize=(5,4))
#title = 'arg-sampler-test_k20_mu0.01_gammaNatural_bestTrueReference_weightedRFDists.png'
#sns.boxplot(x="Method", y="Weighted RF Dist", data=df,fliersize=0, width=.4,order=['Espalier','ARGWeaver','ML Tree'],palette="Set2") # palette="vlag")
#fig.tight_layout()
#fig.savefig(title, dpi=200)

"""
    Plot RF distances to true local trees
"""
fig, ax = plt.subplots(figsize=(5,4))
title = 'arg-sampler-test_k20_mu0.1_gammaNatural_bestTrueReference_SPRDists_withLegend.png'
ax = sns.boxplot(x="True SPR Dist", y="SPR Dist", data=df, hue='Method', fliersize=0.2, width=.6,hue_order=['Espalier','ARGWeaver','ML Tree'],palette="Set2") # palette="vlag")
#ax = sns.stripplot(x="True SPR Dist", y="SPR Dist", data=df, hue='Method',hue_order=['Espalier','ARGWeaver','ML Tree'])
ax.legend(bbox_to_anchor=(1.01, 0.6),borderaxespad=0)
#ax.get_legend().remove()
ax.set_xlabel('True SPR Distance')
ax.set_ylabel('Reconstructed SPR Distance')
fig.tight_layout()
fig.savefig(title, dpi=200)

"""
    Compute conditional averages for SPR distances
"""
espalier_0_df = df[(df['Method'] == 'Espalier') & (df['True SPR Dist'] == 0)]
espalier_0_mean = espalier_0_df['SPR Dist'].mean()
print(espalier_0_mean)

argweaver_0_df = df[(df['Method'] == 'ARGWeaver') & (df['True SPR Dist'] == 0)]
argweaver_0_mean = argweaver_0_df['SPR Dist'].mean()
print(argweaver_0_mean)

espalier_1_df = df[(df['Method'] == 'Espalier') & (df['True SPR Dist'] == 1)]
espalier_1_mean = espalier_1_df['SPR Dist'].mean()
print(espalier_1_mean)

argweaver_1_df = df[(df['Method'] == 'ARGWeaver') & (df['True SPR Dist'] == 1)]
argweaver_1_mean = argweaver_1_df['SPR Dist'].mean()
print(argweaver_1_mean)




