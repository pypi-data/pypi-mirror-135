"""
Created on Wed Aug  5 11:59:34 2020

@author: david
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


"""
    Plot both 3/4-cut methods on same plot
"""
def plot(data,xvar,yvar,title):
    
    sns.set(style="darkgrid")
    fig, ax = plt.subplots(figsize=(4,4))
    
    "Plot correlation between moves and spr dist"
    sns.despine(bottom=True, left=True)

    # Show each observation with a scatterplot
    sns.stripplot(x=xvar, y=yvar, hue="Method", data=data, dodge=True, alpha=.25, zorder=1)

    # Show the conditional means
    #sns.pointplot(x=xvar, y=yvar, hue="Method", data=data, dodge=.532, join=False, palette="dark",markers="d", scale=.75, ci=None)
    ax.set_xlabel('True SPR moves')
    ax.set_ylabel('MAF components - 1') # MAF SPR distance
        
    fig.tight_layout()
    plt.show()
    fig.savefig(title, dpi=200)
    
"""
    Plot each method seperately
"""
def simple_plot(data,xvar,yvar,title,fig_title):
    
    sns.set(style="darkgrid")
    fig, ax = plt.subplots(figsize=(4,4))
    
    "Plot correlation between moves and spr dist"
    sns.despine(bottom=True, left=True)

    # Show each observation with a scatterplot
    sns.stripplot(x=xvar, y=yvar, data=data, dodge=False, alpha=.35, zorder=1)

    # Show the conditional means
    sns.pointplot(x=xvar, y=yvar, data=data, dodge=False, join=False, palette="dark",markers="d", scale=.75, ci=None)
    ax.set_xlabel('True SPR moves')
    ax.set_ylabel('MAF SPR distance') # MAF SPR distance
    ax.set_title(title)
        
    fig.tight_layout()
    plt.show()
    fig.savefig(fig_title, dpi=200)


"Plot results for sims with sample size = 10"   
file = "./results/test_MAF_randomSPRS_4cut_vs_3approx_max5_s10_results.csv"
df10 = pd.read_csv(file) # index_col=0)

"Plot true SPR moves vs MAF SPR dists"
title = 'test_MAF_randomSPRS_4cut_vs_3approx_max5_s10_results.png'
xvar = 'TrueSPRMoves'
yvar = 'SPRDist'
#plot(df10,xvar,yvar,title)

"Plot results with k = 10 for 4-cut algorithm"
df10_4cut = df10[df10['Method'] == "4Cut"]
fig_title = 'test_MAF_randomSPRS_4cut_max5_s10_results.png'
simple_plot(df10_4cut,xvar,yvar,'4-cut algorithm; 10 tips',fig_title)

"Plot results with k = 10 for 4-cut algorithm"
df10_3cut = df10[df10['Method'] == "3Approx"]
fig_title = 'test_MAF_randomSPRS_3cut_max5_s10_results.png'
simple_plot(df10_3cut,xvar,yvar,'3-cut algorithm; 10 tips',fig_title)

"Plot results for sims with sample size = 100"   
file = "./results/test_MAF_randomSPRS_4cut_vs_3approx_max5_s100_results.csv"
df100 = pd.read_csv(file) # index_col=0)

"Plot results with k = 100 for 4-cut algorithm"
df100_4cut = df100[df100['Method'] == "4Cut"]
fig_title = 'test_MAF_randomSPRS_4cut_max5_s100_results.png'
simple_plot(df100_4cut,xvar,yvar,'4-cut algorithm; 100 tips',fig_title)

"Plot results with k = 10 for 4-cut algorithm"
df100_3cut = df100[df100['Method'] == "3Approx"]
fig_title = 'test_MAF_randomSPRS_3cut_max5_s100_results.png'
simple_plot(df100_3cut,xvar,yvar,'3-cut algorithm; 100 tips',fig_title)

"Plot on same catplot -- doesn't look at nice as plotting each on seperate subplot"
# df = pd.concat([df10, df100])
# sns.set(style="darkgrid")
# fig, ax = plt.subplots(figsize=(4,4))
# title = 'test_MAF_randomSPRS_4cut_vs_3approx_max5_results.png'
# xvar = 'TrueSPRMoves'
# yvar = 'SPRDist'
# showfliers = False
# #g = sns.catplot(x=xvar, y=yvar,hue="Method", col="SampleSizes",data=df, kind="box", dodge=True, height=4, aspect=.7,showfliers = False)
# g = sns.catplot(x=xvar, y=yvar,hue="Method", col="SampleSizes",data=df, kind="strip", dodge=True, height=4, aspect=.7)
# fig.tight_layout()
# plt.show()
# fig.savefig(title, dpi=200)

print()