"""
Created on Fri Jul 31 13:45:35 2020

Reconstruct ARG for potyviruses based on protein sub-alignments

@author: david
"""
import TreeReconciler
import ARGSampler
import ARGSimulator
import ARGweaver
import Utils
import dendropy
from dendropy.calculate import treecompare
import pandas as pd
import glob
import math
import os
import shutil
import argparse
import RAxML
import numpy as np

from Bio import SeqIO
    
"""
Control parameters in ARG sampler that need to be tuned:
    -rho recomb prob --> set this to true prob for now
    -prior ratio on alt/ref in reconciler --> now using locally adaptive prior
    -number of local trees to sample
"""

"Sim params"
rho = 0.00001 # rate per site
mut_rate = 1.0 # only used for dating ML trees

"prior"
# prior_gamma = 0.1 # set below
lower_bound_ratio = 0.5

"Set seq files"
features = ['P1','HC-Pro','P3','CI','VPg','NIa','NIb','CP']
segments = len(features)
poty_file_path = "./poty/"
seq_files = [poty_file_path+'potyviruses_P1_aligned_filtered.fasta',
             poty_file_path+'potyviruses_HC-Pro_aligned_filtered.fasta',
             poty_file_path+'potyviruses_P3_aligned_filtered.fasta',
             poty_file_path+'potyviruses_CI_aligned_filtered.fasta',
             poty_file_path+'potyviruses_VPg_aligned_filtered.fasta',
             poty_file_path+'potyviruses_NIa_aligned_filtered.fasta',
             poty_file_path+'potyviruses_NIb_aligned_filtered.fasta',
             poty_file_path+'potyviruses_CP_aligned_filtered.fasta']
        
"Reconstruct local ML trees in RaXML"
reconstruct = False
ML_tree_files = [f.replace('aligned_filtered.fasta','MLTree.tre') for f in seq_files]
tip_date_file = 'poty-dates-lsd.txt'
consensus_tree_file = poty_file_path+'potyviruses_consensus.tre'

"Write tip dates file"
#Utils.write_tip_dates(tree_files[0], tip_date_file)
seq_dict = SeqIO.to_dict(SeqIO.parse(seq_files[0], "fasta")) # one line alternative
taxa_labels = [k for k,v in seq_dict.items()]
tip_date_dict = {tx:0.0 for tx in taxa_labels}
txt=open(tip_date_file,"w")
txt.write(str(len(taxa_labels)) + '\n')
for k,v in tip_date_dict.items():
    txt.write(k + '\t' + str(v) + '\n')
txt.close()

"Write rates to file"
rate_file = 'rate.txt'
Utils.write_rate_file(mut_rate, rate_file)

if reconstruct:
    for i in range(segments):
        print("Segment: " + features[i])
        RAxML.get_dated_poty_tree(seq_files[i], ML_tree_files[i], tip_date_file, rate_file)
 
"Get reference"
ref = ARGSampler.get_consensus_tree(ML_tree_files)
ref.write(path=consensus_tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True) 


"""
    Use nearest tree as ref
"""
taxa = ref.taxon_namespace
tree_dists = np.zeros((segments,segments))
for seg_i in range(segments):   
    tree_i = dendropy.Tree.get(file=open(ML_tree_files[seg_i], 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
    for seg_j in range(segments):
        if seg_i != seg_j:
            tree_j = dendropy.Tree.get(file=open(ML_tree_files[seg_j], 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)    
            tree_dists[seg_i][seg_j] = treecompare.symmetric_difference(tree_i, tree_j)
best_tree = np.argmin(np.sum(tree_dists,axis=0))
ref = dendropy.Tree.get(file=open(ML_tree_files[best_tree], 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
#ref.suppress_unifurcations(update_bipartitions=False)

"""
    Compute total length of each tree
"""
#taxa = ref.taxon_namespace
tree_lengths = []
for tree_file in ML_tree_files:   
    tree = dendropy.Tree.get(file=open(tree_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
    tree_lengths.append(tree.length())
mean_tree_length = np.mean(tree_lengths)

prob_recomb_per_site = mean_tree_length * rho
prob_mut_per_site = mean_tree_length * mut_rate
prior_gamma = prob_recomb_per_site
    
"Run the ARG sampler to get a tree path"
out_report = poty_file_path + "arg-sampler-report.txt"
#tree_path = ARGSampler.sample_ARG_bb(ML_tree_files,seq_files,ref,rho=rho,lower_bound_ratio=lower_bound_ratio,prior_gamma=prior_gamma,midpoint=False,use_viterbi=True,report=out_report)
tree_path, tree_source_path = ARGSampler.sample_ARG_lac(ML_tree_files,seq_files,ref,rho=rho,lower_bound_ratio=lower_bound_ratio,prior_gamma=prior_gamma,midpoint=False,use_viterbi=True,true_trees=None,report=out_report)

"Plot ML tree tanglegram"
plot = True
import PlotTanglegrams
#tanglegram_fig_name = 'poty-tanglegram-ML-trees.png' 
#if plot:
#    PlotTanglegrams.plot(ML_tree_files, tanglegram_fig_name, tree_labels=features)
    
"Plot reconcilded tanglegram"
tanglegram_fig_name = 'poty-tanglegram-sampled-ARG.png'
ARG_tree_files = [f.replace('MLTree.tre','ARGLocal.tre') for f in ML_tree_files]
for idx,tr in enumerate(tree_path):
    tr.write(path=ARG_tree_files[idx],schema='newick',suppress_annotations=True,suppress_rooting=True) 
if plot:
    PlotTanglegrams.plot(ARG_tree_files,tanglegram_fig_name,tree_labels=features)


