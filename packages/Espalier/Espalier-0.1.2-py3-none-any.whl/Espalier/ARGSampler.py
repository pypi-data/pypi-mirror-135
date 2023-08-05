"""
Created on Mon Jun  8 15:35:30 2020

@author: david
"""

import ARGSimulator
import TreeReconciler
import dendropy
from dendropy.calculate import treecompare
import numpy as np
from scipy.stats import poisson
from Bio import SeqIO
import Utils
import RAxML
import Dendro2TSConverter
from operator import attrgetter
from collections import namedtuple
import SCARLikelihood

"Global variable cluster determines how system calls to os are made"
cluster = True

class EMError(Exception):
    pass

def tree_in_set(test_tree,trees):
    
    "Test if test_tree is in trees list"
    for tr in trees:
        dist = treecompare.symmetric_difference(test_tree, tr) # # Unweighted Robinson-Foulds distance
        if dist == 0:
            return True

def get_like_array(seq_files,tree_array):
    
    "Compute likelihood for all trees in tree_array"
    like_array = []
    segments = len(seq_files)
    for loc in range(segments):
        tree_likes = []
        seq_file = seq_files[loc]
        for tr in tree_array[loc]:
            temp_tree_file = "temp_ref.tre"
            tr.write(path=temp_tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
            #logL = RAxML.get_tree_likelihood(temp_tree_file,seq_file)
            logL = RAxML.get_tree_likelihood_ng(temp_tree_file,seq_file) # if using raxml-ng
            tree_likes.append(logL)
        like_array.append(tree_likes)
    
    return like_array

"""
    Get consensus from a list of trees using DendroPy
    List can either be list of tree files or a DendroPy TreeList
    If root is set True, consensus tree will be rooted if not already rooted
"""
def get_consensus_tree(tree_list,root=True):
    
    if isinstance(tree_list, dendropy.TreeList):
        trees = tree_list
    else: 
        trees = dendropy.TreeList()
        for tree_file in tree_list: trees.read(path=tree_file,schema='newick',rooting="default-rooted")
    #consensus = trees.consensus(min_freq=0.95) # does not preserve branch lengths
    consensus = trees.maximum_product_of_split_support_tree()
    #print("\nTree {} maximizes the product of split support (log product = {}): {}".format(trees.index(mcct), mcct.log_product_of_split_support, mcct))
    if not consensus.is_rooted and root:
        consensus.reroot_at_midpoint()
    
    return consensus   

"""
    Compute transitions probs between all pairs of adjacent local trees in tree_array
    Recombination rate rho here is per site rate
    Can provide rSPR array so rSPRs are not recomputed each time trans probs are computed
"""
def get_recomb_trans_probs(tree_array,rho,seg_lengths,rSPR_array=None):
    
    "Get recombination transition probabilities between each pair of local trees"
    trans_probs = []
    trans_probs.append(None)
    segments = len(tree_array)
    for loc in range(1,segments):
        "Compute recomb transition probs between trees in previous loc and current loc"
        "Store them in matrix with rows corresponding to trees in T-1 and columns in T"
        trees = tree_array[loc]
        prev_trees = tree_array[loc-1]
        probs = np.zeros((len(prev_trees),len(trees)))
        for i, tree_i in enumerate(prev_trees):
            for j, tree_j in enumerate(trees):
                
                if rSPR_array:
                    rSPR = rSPR_array[loc][i][j]
                else:
                    rSPR = TreeReconciler.get_spr_dist(tree_i,tree_j)
                                
                "Modeling recombination events as a Poisson process"
                #seg_length = seg_lengths[loc-1]
                #tree_length = tree_i.length()
                #lambda_rec = rho * seg_length * tree_length # recombintation itensity over genomic segment/block
                #probs[i][j] = poisson.pmf(rSPR, lambda_rec)
                
                "Modeling as instantaneous events"
                seg_length = 1
                tree_length = tree_i.length()
                lambda_rec = rho * seg_length * tree_length # recombintation itensity over genomic segment/block
                probs[i][j] = lambda_rec**rSPR           
                
        trans_probs.append(probs)
    
    return trans_probs

"""
    Compute rooted subtree-prune-regraft distances between all pairs of adjacent local trees in tree_array
"""
def get_rSPR_array(tree_array):
    
    rSPR_array = []
    rSPR_array.append(None)
    segments = len(tree_array)
    for loc in range(1,segments):
        trees = tree_array[loc]
        prev_trees = tree_array[loc-1]
        rSPRs = np.zeros((len(prev_trees),len(trees)))
        for i, tree_i in enumerate(prev_trees):
            for j, tree_j in enumerate(trees):
                rSPRs[i][j] = TreeReconciler.get_spr_dist(tree_i,tree_j)
        rSPR_array.append(rSPRs)
    
    return rSPR_array


def norm_log_probs(log_probs):
    
    log_probs = log_probs - np.min(log_probs) # recenter so min log prob is at zero
    probs = np.exp(log_probs) # convert back to linear scale
    norm_probs = probs / np.sum(probs)
    return norm_probs

def forward_back(tree_array, trans_probs, like_array):
     
    segments = len(tree_array)
    tree_states = [len(trees) for trees in tree_array]
    max_states = max(tree_states)
    state_probs = np.zeros((segments,max_states))
    #path = np.zeros((segments,max_states)).astype(int)
    prior = [1.0]*tree_states[0]
    
    "Compute state probs for tree T0 based on priors"
    log_state_probs = []
    for st in range(tree_states[0]):
        log_state_probs.append(np.log(prior[st]) + like_array[0][st]) # always working on log scale
        #path[0][st] = 0
    
    "Normalize (log) probs"
    norm_probs = norm_log_probs(log_state_probs)
    for st in range(tree_states[0]):
        state_probs[0][st] = norm_probs[st]
    
    "Compute forward probs (i.e. conditional likelihood of segments seen so far for T1, T2... TN"
    for loc in range(1, segments):
        log_state_probs = []
        for st in range(tree_states[loc]):
            psum = 0 # sum over prev_states
            "Problem here b/c we can't sum probs if their already log transformed"
            "Solution: work with normalized probs since we only need full likelihoods for path chosen on backward pass"
            for prev_st in range(tree_states[loc-1]):
                psum += state_probs[loc-1][prev_st] * trans_probs[loc][prev_st][st] 
            log_state_probs.append(np.log(psum) + like_array[loc][st])
        
        "Normalize (log) probs"
        norm_probs = norm_log_probs(log_state_probs)
        for st in range(tree_states[loc]):
            state_probs[loc][st] = norm_probs[st]
    
    "Randomly sample state/tree for final loc proportional to probs" 
    final_probs = state_probs[-1][:tree_states[-1]]
    #norm_final_probs = norm_log_probs(final_probs) 
    chosen_st = np.random.choice(list(range(tree_states[-1])),1,p=final_probs)[0]
    opt = []
    opt.append(chosen_st)
 
    "Backtrack till the first observation"
    previous = chosen_st
    tree_path = []
    back_prob = like_array[-1][chosen_st] # these are on a log scale
    tree_path.append(tree_array[-1][chosen_st])
    for loc in range(segments - 2, -1, -1):
        weights = []
        for st in range(tree_states[loc]):
            "Check indexing here"
            weights.append(state_probs[loc][st] * trans_probs[loc+1][st][previous])
        W = weights / np.sum(weights)
        k = np.random.choice(list(range(tree_states[loc])),1,p=W)[0]
        tprob = trans_probs[loc+1][k][previous]
        previous = k
        "Need to compute backwards probs -- but these can be on a log scale"
        back_prob += like_array[loc][previous] + np.log(tprob)
        opt.append(previous)
        tree_path.append(tree_array[loc][previous])
    
    print ('The path of trees samples is ' + ' '.join(str(opt)) + ' with a max path likelihood of %s' % back_prob)
    
    return list(reversed(tree_path))

def viterbi(tree_array, trans_probs, like_array):
     
    segments = len(tree_array)
    tree_states = [len(trees) for trees in tree_array]
    max_states = max(tree_states)
    state_probs = np.zeros((segments,max_states))
    path = np.zeros((segments,max_states)).astype(int)
    prior = [1.0]*tree_states[0]
    
    "Compute state probs for tree T0 based on priors"
    for st in range(tree_states[0]):
        state_probs[0][st] = np.log(prior[st]) + like_array[0][st] # always working on log scale
        path[0][st] = 0
        
    "Compute forward probs (i.e. conditional likelihoods of segments seen so far for T1, T2... TN"
    for loc in range(1, segments):
        for st in range(tree_states[loc]):
            probs = []
            for prev_st in range(tree_states[loc-1]):
                probs.append(state_probs[loc-1][prev_st] + np.log(trans_probs[loc][prev_st][st]))
            path[loc][st] = np.argmax(probs) 
            state_probs[loc][st] = max(probs) + like_array[loc][st]
    
    "Select most likely state/tree for final loc" 
    final_probs = state_probs[-1][:tree_states[-1]]
    best_st = np.argmax(final_probs) 
    opt = []
    opt.append(best_st)
    max_prob = final_probs[best_st]
 
    "Backtrack till the first observation"
    previous = best_st
    tree_path = []
    #print(len(tree_array))
    tree_path.append(tree_array[-1][best_st])
    for loc in range(segments - 2, -1, -1):
        previous = path[loc+1][previous]
        opt.append(previous)
        tree_path.append(tree_array[loc][previous])
    
    "Reverse tree_path and opt"
    tree_path = list(reversed(tree_path))
    opt = list(reversed(opt))
    
    print ('The path of trees samples is ' + ' '.join(str(opt)) + ' with a max path likelihood of %s' % max_prob)
    
    return tree_path, opt
    
def sample_ARG(local_tree_files,seq_files,ref,rho=1.0,prior_tree_ratio=[1.0],midpoint=True,use_viterbi=True,plot=False,report=None):
    
    "Sample an ARG given starting local trees and a reference/consensus"
        
    "Smooth local tree sequencing by reconciling against reference"
    max_sample_size = 5
    tree_array = []
    taxa = ref.taxon_namespace
    
    "Get genome segment data"
    segments = len(local_tree_files)
    seg_lengths = []
    seg_starts = []
    seg_ends = []
    for loc in range(segments):
        seq_file = seq_files[loc] # path + "disentangler_test1_tree" + str(loc) + ".fasta"
        seg_length = len(list(SeqIO.parse(seq_file, "fasta"))[0])
        seg_start = int(np.sum(seg_lengths))
        seg_end = seg_start + seg_length # this is actually seg_end + 1 but this makes indexing sites easier
        seg_lengths.append(seg_length)
        seg_starts.append(seg_start)
        seg_ends.append(seg_end)
        
    "Get concatenated sequence"
    temp_concat_file = 'temp_concat_seqs.fasta'
    Utils.concate_aligns(seq_files,temp_concat_file)
    
    "Set up priors"
    if len(prior_tree_ratio) < segments:
        prior_tree_ratio = prior_tree_ratio * segments
    
    MAF_sizes = []
    num_trees_proposed = []
    num_trees_accepted = []
    for loc in range(segments):
        
        #print("-"*20)
        print("Segment = " + str(loc))
        #print("-"*20)
        
        "Get tree for this segment"
        alt_file = local_tree_files[loc] # local tree
        alt = dendropy.Tree.get(file=open(alt_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
        seq_file = seq_files[loc] # path + "disentangler_test1_tree" + str(loc) + ".fasta"

        if plot:
            print("Reference tree:")
            ref.print_plot()
            print("Alternate tree:")
            alt.print_plot()
        
        "Get maximum agreement forest"
        maf = TreeReconciler.get_maf_4cut(ref,alt,plot=False)
        if plot:
            TreeReconciler.plot_maf(maf)
        
        "Sample a reconciled tree - something goes wrong here when we sample more than one tree"
        sampled_trees = dendropy.TreeList()
        sampled_trees.taxon_namespace = taxa
        tree_sample_size = min(max_sample_size,2**(len(maf)-1)) # there are 2**(len(maf)-1) possible ways to reconcile tree and ref
        counter = 0
        p_tree_ratio = prior_tree_ratio[loc]
        while (len(sampled_trees) < tree_sample_size) and (counter < 2*max_sample_size):
            #print("Iteration = " + str(counter))
            
            "New way where prior depends on like of seq data outside of local segment"
            start_pos = seg_starts[loc]
            end_pos = seg_ends[loc]
            rec_tree = TreeReconciler.reconcile_local_tree(ref,alt,maf.clone(),temp_concat_file,start_pos,end_pos,prior_ratio=p_tree_ratio,midpoint=midpoint,plot=False)
            
            "Old way assuming a fixed prior based on segment sizes"
            #rec_tree = TreeReconciler.reconcile_trees(ref,alt,maf.clone(),seq_file=seq_file,prior_ratio=p_tree_ratio,midpoint=midpoint,plot=False)
            
            if rec_tree.__len__() != ref.__len__():
                print("Trees of unequal size found!!")
            rec_tree.taxon_namespace = taxa
            rec_tree.reconstruct_taxon_namespace() #reindex_subcomponent_taxa()
            
            """
                I guess this is where we would reconcile heights
            """
            
            if not tree_in_set(rec_tree, sampled_trees): # test if we've already sampled this tree
                sampled_trees.append(rec_tree)
            counter += 1
        
        tree_array.append(sampled_trees)
        
        "Stats for report"
        MAF_sizes.append(len(maf))
        num_trees_proposed.append(counter)
        num_trees_accepted.append(len(sampled_trees))
    
    "Get likelihood of all trees in tree_array"
    like_array = get_like_array(seq_files,tree_array)
    
    "Get recombination transition probs between trees based on SPR distances"
    trans_probs = get_recomb_trans_probs(tree_array,rho,seg_lengths)
    
    "Sample a path of local trees in ARG"
    if use_viterbi:
        tree_path = viterbi(tree_array, trans_probs, like_array)
    else:
        tree_path = forward_back(tree_array, trans_probs, like_array)
    
    """
        Write report to file, including:
            -Composition of trees (alt vs. ref)
            -Path chosen with dSPR distances between chosen trees 
    """
    if report:
        txt=open(report,"w")
        txt.write("Total number of genomic segments: " + str(segments) + "\n")
        for loc in range(segments):
            txt.write("-"*20 + "\n")    
            txt.write("Segment = " + str(loc) + "\n")
            txt.write("-"*20 + "\n")
            txt.write("Segment length = " + str(seg_lengths[loc]) + "\n")
            txt.write("Subtrees in MAF = " + str(MAF_sizes[loc]) + "\n") 
            txt.write("Prior alt/ref tree ratio = " + str(f"{prior_tree_ratio[loc]:0.2f}") + "\n")
            txt.write("Reconciled trees proposed = " + str(num_trees_proposed[loc]) + "\n")
            txt.write("Reconciled trees accepted = " + str(num_trees_accepted[loc]) + "\n")
            txt.write("\n")
        txt.close()
    
    return tree_path

def sample_ARG_DSLP(local_tree_files,seq_files,ref,rho=1.0,prior_gamma=0.0,midpoint=True,use_viterbi=True,plot=False,report=None):
    
    "Sample an ARG given starting local trees and a reference/consensus"
        
    "Smooth local tree sequencing by reconciling against reference"
    max_sample_size = 5
    tree_array = []
    taxa = ref.taxon_namespace
    
    "Get genome segment data"
    segments = len(local_tree_files)
    seg_lengths = []
    seg_starts = []
    seg_ends = []
    for loc in range(segments):
        seq_file = seq_files[loc] # path + "disentangler_test1_tree" + str(loc) + ".fasta"
        seg_length = len(list(SeqIO.parse(seq_file, "fasta"))[0])
        seg_start = int(np.sum(seg_lengths))
        seg_end = seg_start + seg_length # this is actually seg_end + 1 but this makes indexing sites easier
        seg_lengths.append(seg_length)
        seg_starts.append(seg_start)
        seg_ends.append(seg_end)
        
    "Get concatenated sequence"
    temp_concat_file = 'temp_concat_seqs.fasta'
    Utils.concate_aligns(seq_files,temp_concat_file)
    
    MAF_sizes = []
    num_trees_proposed = []
    num_trees_accepted = []
    for loc in range(segments):
        
        #print("-"*20)
        print("Segment = " + str(loc))
        #print("-"*20)
        
        "Get tree for this segment"
        alt_file = local_tree_files[loc] # local tree
        alt = dendropy.Tree.get(file=open(alt_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
        seq_file = seq_files[loc] # path + "disentangler_test1_tree" + str(loc) + ".fasta"

        if plot:
            print("Reference tree:")
            ref.print_plot()
            print("Alternate tree:")
            alt.print_plot()
        
        "Get maximum agreement forest"
        maf = TreeReconciler.get_maf_4cut(ref,alt,plot=False)
        if plot:
            TreeReconciler.plot_maf(maf)
        
        "Sample a reconciled tree - something goes wrong here when we sample more than one tree"
        sampled_trees = dendropy.TreeList()
        sampled_trees.taxon_namespace = taxa
        tree_sample_size = min(max_sample_size,2**(len(maf)-1)) # there are 2**(len(maf)-1) possible ways to reconcile tree and ref
        counter = 0
        while (len(sampled_trees) < tree_sample_size) and (counter < 2*max_sample_size):
            #print("Iteration = " + str(counter))
            
            "New way where prior depends on like of seq data outside of local segment"
            start_pos = seg_starts[loc]
            end_pos = seg_ends[loc]
            rec_tree = TreeReconciler.reconcile_local_tree(ref,alt,maf.clone(),temp_concat_file,start_pos,end_pos,prior_gamma=prior_gamma,midpoint=midpoint,plot=False)
            
            if rec_tree.__len__() != ref.__len__():
                print("Trees of unequal size found!!")
            rec_tree.taxon_namespace = taxa
            rec_tree.reconstruct_taxon_namespace() #reindex_subcomponent_taxa()
            
            """
                I guess this is where we would reconcile heights
            """
            
            if not tree_in_set(rec_tree, sampled_trees): # test if we've already sampled this tree
                sampled_trees.append(rec_tree)
            counter += 1
        
        tree_array.append(sampled_trees)
        
        "Stats for report"
        MAF_sizes.append(len(maf))
        num_trees_proposed.append(counter)
        num_trees_accepted.append(len(sampled_trees))
    
    "Get likelihood of all trees in tree_array"
    like_array = get_like_array(seq_files,tree_array)
    
    "Get recombination transition probs between trees based on SPR distances"
    trans_probs = get_recomb_trans_probs(tree_array,rho,seg_lengths)
    
    "Sample a path of local trees in ARG"
    if use_viterbi:
        tree_path = viterbi(tree_array, trans_probs, like_array)
    else:
        tree_path = forward_back(tree_array, trans_probs, like_array)
    
    """
        Write report to file, including:
            -Composition of trees (alt vs. ref)
            -Path chosen with dSPR distances between chosen trees 
    """
    if report:
        txt=open(report,"w")
        txt.write("Total number of genomic segments: " + str(segments) + "\n")
        for loc in range(segments):
            txt.write("-"*20 + "\n")    
            txt.write("Segment = " + str(loc) + "\n")
            txt.write("-"*20 + "\n")
            txt.write("Segment length = " + str(seg_lengths[loc]) + "\n")
            txt.write("Subtrees in MAF = " + str(MAF_sizes[loc]) + "\n") 
            #txt.write("Prior alt/ref tree ratio = " + str(f"{prior_tree_ratio[loc]:0.2f}") + "\n")
            txt.write("Reconciled trees proposed = " + str(num_trees_proposed[loc]) + "\n")
            txt.write("Reconciled trees accepted = " + str(num_trees_accepted[loc]) + "\n")
            txt.write("\n")
        txt.close()
    
    return tree_path

def sample_ARG_bb(local_tree_files,seq_files,ref,rho=1.0,lower_bound_ratio=0.1,prior_gamma=0.0,midpoint=True,use_viterbi=True,plot=False,report=None):
    
    "Sample an ARG given starting local trees and a reference/consensus"
        
    "Smooth local tree sequencing by reconciling against reference"
    #max_sample_size = 5
    tree_array = []
    taxa = ref.taxon_namespace
    
    "Get genome segment data"
    segments = len(local_tree_files)
    seg_lengths = []
    seg_starts = []
    seg_ends = []
    for loc in range(segments):
        seq_file = seq_files[loc] # path + "disentangler_test1_tree" + str(loc) + ".fasta"
        seg_length = len(list(SeqIO.parse(seq_file, "fasta"))[0])
        seg_start = int(np.sum(seg_lengths))
        seg_end = seg_start + seg_length # this is actually seg_end + 1 but this makes indexing sites easier
        seg_lengths.append(seg_length)
        seg_starts.append(seg_start)
        seg_ends.append(seg_end)
        
    "Get concatenated sequence"
    temp_concat_file = 'temp_concat_seqs.fasta'
    Utils.concate_aligns(seq_files,temp_concat_file)
    
    MAF_sizes = []
    #num_trees_proposed = []
    num_trees_accepted = []
    for loc in range(segments):
        
        #print("-"*20)
        print("Segment = " + str(loc))
        #print("-"*20)
        
        "Get tree for this segment"
        alt_file = local_tree_files[loc] # local tree
        alt = dendropy.Tree.get(file=open(alt_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
        seq_file = seq_files[loc] # path + "disentangler_test1_tree" + str(loc) + ".fasta"

        if plot:
            print("Reference tree:")
            ref.print_plot()
            print("Alternate tree:")
            alt.print_plot()
        
        "Get maximum agreement forest"
        maf = TreeReconciler.get_maf_4cut(ref,alt,plot=False)
        #maf = TreeReconciler.get_maf_4cut(alt,ref,plot=False) # switch ref/alt order so subtrees in MAF are pruned from ref
        if plot:
            TreeReconciler.plot_maf(maf)
        
        "Use branch and bound algorithm to search for reconciled trees"
        start_pos = seg_starts[loc]
        end_pos = seg_ends[loc]
        sampled_trees = TreeReconciler.bb_regraft(ref,alt,maf.clone(),temp_concat_file,start_pos,end_pos,lower_bound_ratio=lower_bound_ratio,prior_gamma=prior_gamma,midpoint=midpoint,plot=False)
        
        tree_array.append(sampled_trees)
        
        "Stats for report"
        MAF_sizes.append(len(maf))
        #num_trees_proposed.append(counter)
        num_trees_accepted.append(len(sampled_trees))
    
    "Get likelihood of all trees in tree_array"
    like_array = get_like_array(seq_files,tree_array)
    
    "Get recombination transition probs between trees based on SPR distances"
    trans_probs = get_recomb_trans_probs(tree_array,rho,seg_lengths)
    
    "Sample a path of local trees in ARG"
    if use_viterbi:
        tree_path = viterbi(tree_array, trans_probs, like_array)
    else:
        tree_path = forward_back(tree_array, trans_probs, like_array)
    
    """
        Write report to file, including:
            -Composition of trees (alt vs. ref)
            -Path chosen with dSPR distances between chosen trees 
    """
    if report:
        txt=open(report,"w")
        txt.write("Total number of genomic segments: " + str(segments) + "\n")
        for loc in range(segments):
            txt.write("-"*20 + "\n")    
            txt.write("Segment = " + str(loc) + "\n")
            txt.write("-"*20 + "\n")
            txt.write("Segment length = " + str(seg_lengths[loc]) + "\n")
            txt.write("Subtrees in MAF = " + str(MAF_sizes[loc]) + "\n") 
            #txt.write("Prior alt/ref tree ratio = " + str(f"{prior_tree_ratio[loc]:0.2f}") + "\n")
            #txt.write("Reconciled trees proposed = " + str(num_trees_proposed[loc]) + "\n")
            txt.write("Reconciled trees accepted = " + str(num_trees_accepted[loc]) + "\n")
            txt.write("\n")
        txt.close()
    
    return tree_path

"""
    Sample an ARG using a locally adaptive consensus tree
"""
def sample_ARG_lac(local_tree_files,seq_files,global_ref,rho=1.0,lower_bound_ratio=0.1,prior_gamma=0.0,midpoint=True,use_viterbi=True,plot=False,true_trees=None,report=None):
    
    "Sample an ARG given starting local trees and a reference/consensus"
        
    "Smooth local tree sequencing by reconciling against reference"
    #max_sample_size = 5
    tree_array = []
    taxa = global_ref.taxon_namespace
    
    "Get genome segment data"
    segments = len(local_tree_files)
    seg_lengths = []
    seg_starts = []
    seg_ends = []
    for loc in range(segments):
        seq_file = seq_files[loc] # path + "disentangler_test1_tree" + str(loc) + ".fasta"
        seg_length = len(list(SeqIO.parse(seq_file, "fasta"))[0])
        seg_start = int(np.sum(seg_lengths))
        seg_end = seg_start + seg_length # this is actually seg_end + 1 but this makes indexing sites easier
        seg_lengths.append(seg_length)
        seg_starts.append(seg_start)
        seg_ends.append(seg_end)
        
    "Get concatenated sequence"
    temp_concat_file = 'temp_concat_seqs.fasta'
    Utils.concate_aligns(seq_files,temp_concat_file)
    
    MAF_sizes = []
    #num_trees_proposed = []
    num_trees_accepted = []
    
    previous_trees = dendropy.TreeList()
    sampled_trees = dendropy.TreeList()
    sources_array = []
    
    ref = global_ref
    
    for loc in range(segments):
        
        #print("-"*20)
        print("Segment = " + str(loc))
        #print("-"*20)
        
        "Get tree for this segment"
        alt_file = local_tree_files[loc] # local tree
        alt = dendropy.Tree.get(file=open(alt_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
        seq_file = seq_files[loc] # path + "disentangler_test1_tree" + str(loc) + ".fasta"

        "Get locally adapted consensus for previous segement"
        #if loc > 0:
        #   ref = get_consensus_tree(sampled_trees)
        #else:
        #   ref = global_ref
        
        if plot:
            print("Reference tree:")
            ref.print_plot()
            print("Alternate tree:")
            alt.print_plot()
        
        "Get maximum agreement forest"
        maf = TreeReconciler.get_maf_4cut(ref,alt,plot=False)
        #maf = TreeReconciler.get_maf_4cut(alt,ref,plot=False) # switch ref/alt order so subtrees in MAF are pruned from ref
        if plot:
            TreeReconciler.plot_maf(maf)
        
        "Use branch and bound algorithm to search for reconciled trees"
        start_pos = seg_starts[loc]
        end_pos = seg_ends[loc]
        sampled_trees, sampled_sources = TreeReconciler.bb_regraft(ref,alt,maf.clone(),temp_concat_file,start_pos,end_pos,previous_trees,lower_bound_ratio=lower_bound_ratio,prior_gamma=prior_gamma,midpoint=midpoint,plot=False)
        
        tree_array.append(sampled_trees)
        previous_trees = sampled_trees
        sources_array.append(sampled_sources)
        
        "Stats for report"
        MAF_sizes.append(len(maf))
        #num_trees_proposed.append(counter)
        num_trees_accepted.append(len(sampled_trees))
    
    
    "Append the ref to the sampled trees for each region"
    for loc in range(segments):
        tree_array[loc].append(ref) # add ref to set of sampled trees
        sources_array[loc].append('Consensus')
        if true_trees:
            true_tree_file = true_trees[loc] # local tree
            true_tree = dendropy.Tree.get(file=open(true_tree_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
            true_tree.suppress_unifurcations(update_bipartitions=False)
            tree_array[loc].append(true_tree) # add ref to set of sampled trees
            sources_array[loc].append('True')
        
    "Get likelihood of all trees in tree_array"
    like_array = get_like_array(seq_files,tree_array)
    
    "Get recombination transition probs between trees based on SPR distances"
    trans_probs = get_recomb_trans_probs(tree_array,rho,seg_lengths)
    
    "Sample a path of local trees in ARG"
    if use_viterbi:
        tree_path, opt = viterbi(tree_array, trans_probs, like_array)
    else:
        tree_path = forward_back(tree_array, trans_probs, like_array)
        
    "Get source of trees in tree_path"
    tree_source_path = [sources_array[loc][opt[loc]] for loc in range(segments)]
    print("Tree source path: " + ' '.join(tree_source_path))
        
    """
        Write report to file, including:
            -Composition of trees (alt vs. ref)
            -Path chosen with dSPR distances between chosen trees 
    """
    if report:
        txt=open(report,"w")
        txt.write("Total number of genomic segments: " + str(segments) + "\n")
        for loc in range(segments):
            txt.write("-"*20 + "\n")    
            txt.write("Segment = " + str(loc) + "\n")
            txt.write("-"*20 + "\n")
            txt.write("Segment length = " + str(seg_lengths[loc]) + "\n")
            txt.write("Subtrees in MAF = " + str(MAF_sizes[loc]) + "\n") 
            #txt.write("Prior alt/ref tree ratio = " + str(f"{prior_tree_ratio[loc]:0.2f}") + "\n")
            #txt.write("Reconciled trees proposed = " + str(num_trees_proposed[loc]) + "\n")
            txt.write("Reconciled trees accepted = " + str(num_trees_accepted[loc]) + "\n")
            txt.write("\n")
        txt.close()
    
    return tree_path, tree_source_path

"""
    Only used by add_recombination_events()
    Move to TreeReconciler?
"""
def add_rec_node(tree,attachment_edge,recomb_time,midpoint=False):
    
    "Create a new 'graft' node to attach sub_tree and sister of sub_tree"
    attachment_parent_node = attachment_edge.tail_node
    attachment_child_node = attachment_edge.head_node
    deep_rooted = False
    if not attachment_parent_node:
        
        print('Grafting recombinant node above root')
        
        "Grafting above root of rec tree such that graft node will be new root"
        "This can happen if cut one of the root's child edges"
        "This should be working now but not very well tested!!"
        tree = TreeReconciler.add_deep_root(tree) # reroot == True by default now
        deep_rooted = True 
        attachment_parent_node = attachment_edge.tail_node
        attachment_child_node = attachment_edge.head_node
        
    else:
        
        attachment_edge_length = attachment_child_node.edge_length
        graft_node = attachment_parent_node.new_child() # this will represent the recombination node
    
        "Extract child subtree descending from attachment edge and prune it from tree"
        for node in tree.preorder_node_iter():
            node.remove = False
        for node in attachment_child_node.preorder_iter():
            node.remove = True
        node_filter_fn = lambda nd: nd.remove
        
        """
            Temp for debugging
        """
        #tree_label_fn = lambda nd: str(nd.remove) # if nd.is_leaf() else str(f"{nd.age:0.2f}")
        #tree.print_plot(show_internal_node_labels=True,node_label_compose_fn=tree_label_fn)
        
        child_subtree = tree.extract_tree(node_filter_fn=node_filter_fn)
        tree.prune_subtree(attachment_child_node, update_bipartitions=False, suppress_unifurcations=False) # supress_unifurcations was True, which was why we were losing recombinant nodes we already added

        "Get and set length of graft edge"
        if midpoint: # attach to midpoint of attachment edge
            graft_node.edge.length = attachment_edge_length / 2.0
        else: # figure out length of edge from attachment height
            tree.calc_node_ages(ultrametricity_precision=False)
            "This sets the height of the recombination node/event below the parent node"
            graft_node_edge_length = attachment_parent_node.age - recomb_time
            if graft_node_edge_length >= 0.0:
                graft_node.edge.length = graft_node_edge_length
            else:
                print('WARNING: Graft edge length is less than zero!!')
                graft_node.edge.length = 0.0
    
        "Reattach child subtree to graft node"
        child_subtree_root = TreeReconciler.get_root_node(child_subtree)
        if midpoint:
            child_subtree_root.edge.length = attachment_edge_length / 2.0
        else:
            "Edge length is difference between graft node age and height/age of child_subtree"
            child_subtree.calc_node_ages(ultrametricity_precision=False)
            child_subtree_edge_length = recomb_time - child_subtree_root.age
            if child_subtree_edge_length >= 0.0:
                child_subtree_root.edge.length = child_subtree_edge_length
            else:
                print('WARNING: Child subtree edge length is less than zero!!')
                child_subtree_root.edge.length = 0.0
        graft_node.add_child(child_subtree_root)
        
        if deep_rooted:
             tree = TreeReconciler.remove_deep_root(tree)
    
    return tree

"""
    Find edge where subtree attaches in alt and then find equivalent edge in ref
    Only used by add_recombination_events()
    Move to TreeReconciler?
"""
def find_recombinant_edge(tree,subtree_taxa):
    
    "Find edge where subtree attaches in alt tree" 
    "Note: this will be the parent of the first edge that includes all subtree_taxa in its leaf set"
    for edge in tree.postorder_edge_iter():
        edge_taxa = set([lf.taxon.label for lf in edge.head_node.leaf_iter()])
        if subtree_taxa.issubset(edge_taxa): # subtree_taxa are subset of all edge_taxa
            "All subtree_taxa are in edge_taxa so subtree must attach here!"
            break
    
    attachment_edge = edge
    parent_node = edge.tail_node # parent of recombinant/attachment edge
    child_node = edge.head_node # child of recombinant edge
    child_nodes = parent_node.child_nodes()
    if len(child_nodes) < 2:
        print('WTF!') # I think this can only happen if we've already added a recombination node as a unifurcation
    if child_nodes[0] is child_node:
        sibling_node = child_nodes[1]
    else:
        sibling_node = child_nodes[0]
    
    "Find constraints on timing of recomb event"
    tree.calc_node_ages(ultrametricity_precision=False)
    parent_time = parent_node.age # max recombination time is height/age of parent node
    child_time = child_node.age
    sibling_time = sibling_node.age

    return attachment_edge, parent_time, child_time, sibling_time


"""
    Find necessary recombination events to reconcile two trees based on MAF
    This has corrected node height constraints
"""
def find_recombination_events(ref,alt,maf,ref_rec_nodes,alt_rec_nodes,plot=False):
    
    RecNode = namedtuple('RecNode', 'edge_bitmask recomb_time')
    
    maf.pop() # remove last/largest connected component
    for sub_tree in reversed(maf):
    
        "Get taxa set in subtree"
        subtree_taxa = set([lf.taxon.label for lf in sub_tree.leaf_node_iter()])
            
        "Find edge where subtree attaches in alt and then find equivalent edge in ref"
        attachment_edge_alt, parent_time_alt, child_time_alt, sibling_time_alt = find_recombinant_edge(alt,subtree_taxa)
        
        "Find edge where subtree attaches in ref and then find equivalent edge in alt"
        attachment_edge_ref, parent_time_ref, child_time_ref, sibling_time_ref  = find_recombinant_edge(ref,subtree_taxa)
        
        "Pick a recombination event time that satisfies time constraints in both alt and ref trees"
        max_recomb_time = min(parent_time_alt,parent_time_ref) # event must be below parent nodes in either tree
        
        min_recomb_times = [child_time_alt,child_time_ref]
        """
            I don't think sibling time constrains are necessary
            And may make rec time requirements overly stringent
            Can commment out following lines!!!
        """
        if sibling_time_alt < max_recomb_time:
            min_recomb_times.append(sibling_time_alt)
        if sibling_time_ref < max_recomb_time:
            min_recomb_times.append(sibling_time_ref)
        min_recomb_time = max(min_recomb_times)        
        
        assert max_recomb_time >= min_recomb_time
        recomb_time = np.random.uniform(low=min_recomb_time,high=max_recomb_time) # draw a uniform time between these constraints 
        
        """
            Add single node as a unification representing recombination to both alt and ref tree        
            We will now add rec_nodes last so bifurcations and edge_bitmasks
            We will use a named tuple so we can easilty sort these by times 
        """
        ref_rec_nodes.append(RecNode(edge_bitmask=attachment_edge_ref.split_bitmask, recomb_time=recomb_time))
        alt_rec_nodes.append(RecNode(edge_bitmask=attachment_edge_alt.split_bitmask, recomb_time=recomb_time))
        
        if plot:
            print("Reference tree:")
            ref.print_plot()
            print("Alternate tree:")
            alt.print_plot()
    
    return ref_rec_nodes,alt_rec_nodes

"""
    Add recombination nodes to tree in path
"""
def add_path_rec_nodes(tree_path,verbose=False):
    
    segments = len(tree_path)
    
    "Create list to hold rec_nodes for each tree in path"
    rec_nodes = [[] for x in range(segments)]

    "Add recombination events to each tree in path"
    for loc in range(segments-1):
        ref = tree_path[loc]
        alt = tree_path[loc+1]
        ref_rec_nodes = rec_nodes[loc]
        alt_rec_nodes = rec_nodes[loc+1]
        maf = TreeReconciler.get_maf_4cut(ref,alt,plot=False)
        if verbose:
            print("Adding " + str(len(maf)-1) + " recombination events between segments " + str(loc) + " and " + str(loc+1))
        ref_rec_nodes,alt_rec_nodes = find_recombination_events(ref,alt,maf,ref_rec_nodes,alt_rec_nodes,plot=False)
    
    total_recs_added = 0
    for tree_idx, tree in enumerate(tree_path):
        
        bipartition_dict = tree.split_bitmask_edge_map
        
        "Sort rec_nodes in descending order by time so we add older events first"
        tree_rec_nodes = rec_nodes[tree_idx]
        tree_rec_nodes = sorted(tree_rec_nodes, key=attrgetter('recomb_time'), reverse=True)
        total_recs_added += len(tree_rec_nodes)
        for rn in tree_rec_nodes:
            
            """
                Temp for debugging
            """
            #bitmask_label_fn = lambda nd: str(nd.edge.split_bitmask) # if nd.is_leaf() else str(f"{nd.age:0.2f}")
            #tree.print_plot(show_internal_node_labels=True,node_label_compose_fn=bitmask_label_fn)
            
            rec_edge = bipartition_dict.get(rn.edge_bitmask,None)
            tree = add_rec_node(tree,rec_edge,rn.recomb_time)
            
            """
                Re-encode bipartitions in case bipartitions were lost after adding rec_node
            """
            tree.encode_bipartitions(suppress_unifurcations=False)
            bipartition_dict = tree.split_bitmask_edge_map
            
    print("Added " + str(total_recs_added) + " recombination nodes to tree path")
            
    return tree_path

"""
    Run EM algorithm to estimate recombination rate
"""
def run_EM(local_tree_files,seq_files,global_ref,scar_params,lower_bound_ratio=0.1,prior_gamma=0.0,midpoint=True,use_viterbi=True,plot=False,true_trees=None,report=None):
    
    "Sample an ARG given starting local trees and a reference/consensus"
    
    rho = scar_params["rho"] # this is the recomb rate per site
    
    "Smooth local tree sequencing by reconciling against reference"
    #max_sample_size = 5
    tree_array = []
    taxa = global_ref.taxon_namespace
    
    "Get genome segment data"
    segments = len(local_tree_files)
    seg_lengths = []
    seg_starts = []
    seg_ends = []
    for loc in range(segments):
        seq_file = seq_files[loc] # path + "disentangler_test1_tree" + str(loc) + ".fasta"
        seg_length = len(list(SeqIO.parse(seq_file, "fasta"))[0])
        seg_start = int(np.sum(seg_lengths))
        seg_end = seg_start + seg_length # this is actually seg_end + 1 but this makes indexing sites easier
        seg_lengths.append(seg_length)
        seg_starts.append(seg_start)
        seg_ends.append(seg_end)
        if loc == segments-1:
            seg_ends[loc] = int(scar_params['genome_length']) # just to enforce total length which may be off slightly due to rounding
    tree_intervals = [(i,j) for i,j in zip(seg_starts,seg_ends)]
            
    "Get concatenated sequence"
    temp_concat_file = 'temp_concat_seqs.fasta'
    Utils.concate_aligns(seq_files,temp_concat_file)
    
    MAF_sizes = []
    #num_trees_proposed = []
    num_trees_accepted = []
    
    previous_trees = dendropy.TreeList()
    sampled_trees = dendropy.TreeList()
    sources_array = []
    
    ref = global_ref
    
    for loc in range(segments):
        
        #print("-"*20)
        print("Segment = " + str(loc))
        #print("-"*20)
        
        "Get tree for this segment"
        alt_file = local_tree_files[loc] # local tree
        alt = dendropy.Tree.get(file=open(alt_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
        seq_file = seq_files[loc] # path + "disentangler_test1_tree" + str(loc) + ".fasta"

        "Get locally adapted consensus for previous segement"
        #if loc > 0:
        #   ref = get_consensus_tree(sampled_trees)
        #else:
        #   ref = global_ref
        
        if plot:
            print("Reference tree:")
            ref.print_plot()
            print("Alternate tree:")
            alt.print_plot()
        
        "Get maximum agreement forest"
        maf = TreeReconciler.get_maf_4cut(ref,alt,plot=False)
        #maf = TreeReconciler.get_maf_4cut(alt,ref,plot=False) # switch ref/alt order so subtrees in MAF are pruned from ref
        if plot:
            TreeReconciler.plot_maf(maf)
        
        "Use branch and bound algorithm to search for reconciled trees"
        start_pos = seg_starts[loc]
        end_pos = seg_ends[loc]
        sampled_trees, sampled_sources = TreeReconciler.bb_regraft(ref,alt,maf.clone(),temp_concat_file,start_pos,end_pos,previous_trees,lower_bound_ratio=lower_bound_ratio,prior_gamma=prior_gamma,midpoint=midpoint,plot=False)
        
        tree_array.append(sampled_trees)
        previous_trees = sampled_trees
        sources_array.append(sampled_sources)
        
        "Stats for report"
        MAF_sizes.append(len(maf))
        #num_trees_proposed.append(counter)
        num_trees_accepted.append(len(sampled_trees))
    
    
    "Append the ref to the sampled trees for each region"
    for loc in range(segments):
        tree_array[loc].append(ref.clone(depth=2)) # add ref to set of sampled trees
        sources_array[loc].append('Consensus')
        if true_trees:
            true_tree_file = true_trees[loc] # local tree
            true_tree = dendropy.Tree.get(file=open(true_tree_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
            true_tree.suppress_unifurcations(update_bipartitions=False) # maybe this should be True?
            tree_array[loc].append(true_tree.clone(depth=2)) # add ref to set of sampled trees
            sources_array[loc].append('True')
    
 
    
    "Get likelihood of all trees in tree_array"
    like_array = get_like_array(seq_files,tree_array)
    
    "Get recombination transition probs between trees based on SPR distances"
    rSPR_array = get_rSPR_array(tree_array)
    
    "If using true path"
    # tree_path = []
    # tree_source_path = []
    # for loc in range(segments):
    #     true_tree_file = true_trees[loc] # local tree
    #     true_tree = dendropy.Tree.get(file=open(true_tree_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
    #     true_tree.suppress_unifurcations(update_bipartitions=True) # was False
    #     true_tree.encode_bipartitions(suppress_unifurcations=False)
    #     tree_path.append(true_tree) # add ref to set of sampled trees
    #     tree_source_path.append('True')
    
    
    """
        Run EM algorithm iteratively sampling tree paths and opitimizing recomb rate rho
    """
    iters = 10
    max_attempts = 5 # maximum number of tree_paths to sample before exiting
    rho_samples = []
    for i in range(iters):        
    
        print("-" * 20)
        print("EM step: " + str(i+1))
        print("-" * 20)
        
        step_completed = False
        failed_attempts = 0
    
        while not step_completed:
    
            try:
        
                """
                    Expectation step: sample new tree path and convert to tree sequence
                """
            
                "Sample a path of local trees in ARG based on trans probs"
                print("Expectation step: Sampling new tree path")
                trans_probs = get_recomb_trans_probs(tree_array,rho,seg_lengths,rSPR_array=rSPR_array)
                if use_viterbi:
                    tree_path, opt = viterbi(tree_array, trans_probs, like_array)
                else:
                    tree_path = forward_back(tree_array, trans_probs, like_array)
                
                "Get source of trees in tree_path"
                tree_source_path = [sources_array[loc][opt[loc]] for loc in range(segments)]
                print("Tree source path: " + ' '.join(tree_source_path))
            
                "Presumably this is where we would reconcile tree node heights"
                print("Reconciling linked heights")
                tree_path = TreeReconciler.reconcile_linked_heights(tree_path)
                
                """
                    Jitter coal times that occur at exact same time by
                    Adding a small displacement dt to the length of their children
                """
                displace_dt = 0.0001
                for tree in tree_path:
                    tree.calc_node_ages(ultrametricity_precision=False)
                    coal_times = tree.internal_node_ages(ultrametricity_precision=False)
                    if len(set(coal_times)) < len(coal_times): # some most not be unique
                        existing_times = [] 
                        for node in tree.postorder_internal_node_iter():
                            while node.age in existing_times:
                                #print("Jittering coal time")
                                #print("Previous node age: " + str(node.age))
                                for child in node.child_node_iter():
                                    child.edge.length = child.edge.length + displace_dt
                                tree.calc_node_ages(ultrametricity_precision=False)
                                #print("Updated node age: " + str(node.age))
                                #print()
                            existing_times.append(node.age)
                
                "Add rec nodes to trees in path"
                print("Adding recombination events to trees in path")
                tree_path = add_path_rec_nodes(tree_path)
                
                # age_label_fn = lambda nd: nd.taxon.label if nd.is_leaf() else str(f"{nd.age:0.2f}")
                # for loc, tree in enumerate(tree_path):
                #     print("-" * 20)
                #     print("Tree #" + str(loc))
                #     print("-" * 20)
                #     tree.print_plot(show_internal_node_labels=True,node_label_compose_fn=age_label_fn)
            
                "Convert trees with recombination nodes to tskit TreeSequence"
                tree_intervals = [(i,j) for i,j in zip(seg_starts,seg_ends)]
                ts = Dendro2TSConverter.convert(tree_path,tree_intervals)
            
                # for tree in ts.trees():
                #     print("-" * 20)
                #     print("tree {}: interval = {}".format(tree.index, tree.interval))
                #     print(tree.draw(format="unicode"))
                # print()
            
                """
                    Maximization step: run optimization to find new rho
                    Note that the rho we infer here is per genome
                """ 
                print("Maximization step: Optimizing recombination rate")
                rho_MLE = SCARLikelihood.opt_MLE(ts,scar_params) # can also specficy bounds
                rho_samples.append(rho_MLE)
                print("Rho estimate: " + str(rho_MLE))
                print()
                            
            except Exception as e: 
                
                print(e)
                failed_attempts += 1
                #pass
            
            else:
                
                step_completed = True
                
            finally:
                                
                if failed_attempts == max_attempts:
                    raise EMError("Too many failed attempts to sample valid tree path")
                    
                    
        
    "Write tree in path to newick files"
    #write_tree_path = True
    #if write_tree_path:
    #    for loc, tree in enumerate(tree_path):
    #        tree_file = true_trees[loc].replace('tree','PathTree')
    #        tree.write(path=tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True) 
    #        new_tree = dendropy.Tree.get(file=open(tree_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
    #        tree_path[loc] = new_tree
    
    return ts, rho_MLE

    
if  __name__ == '__main__':
    
    path = "./sim_trees/"
    plot = False
    
    """
        Prevrious param values:
            recomb_rate = 0.005 (per genome)
            Ne = 100
            mu = 0.001
    """
    
    prior_gamma = 0.01
    lower_bound_ratio = 0.05
    
    mut_rate = 0.05 # high
    genome_length = 1e3
    recomb_rate = 1.0 # rate per genome
    rho = recomb_rate / genome_length
    Ne = 1.0/2 # divide by two to get haploid pop size

    "Simulate ARG in msprime"    
    sim = False
    if sim:
        
        ts = ARGSimulator.sim_ARG(sample_size=20,Ne=Ne,length=genome_length,recombination_rate=rho,min_breakpoints=2)
        breaks = ts.breakpoints(as_array=True)
        segments = len(breaks) - 1 # number of non-recombinant segments between breakpoints
        
        "Write local tree and seq files"
        tree_files = [path + "disentangler_test0_tree" + str(i) + ".tre" for i in range(segments)]
        seq_files = [path + "disentangler_test0_tree" + str(i) + ".fasta" for i in range(segments)]
        for tr_num, tree in enumerate(ts.trees()):
            with open(tree_files[tr_num], "w") as text_file:
                print(tree.newick(), file=text_file)
            seq_length = round(tree.interval[1] - tree.interval[0])
            ARGSimulator.sim_seqs(tree_files[tr_num],seq_files[tr_num],mut_rate=mut_rate,seq_length=seq_length)
    
    else:
        
        "Need to provide local tree and seq files"
        segments = 5
        tree_files = [path + "disentangler_test0_tree" + str(i) + ".tre" for i in range(segments)]
        seq_files = [path + "disentangler_test0_tree" + str(i) + ".fasta" for i in range(segments)]
    
    "Reconstruct local ML trees in RaXML"
    reconstruct = False
    tip_date_file = 'dates-lsd.txt'
    Utils.write_tip_dates(tree_files[0], tip_date_file)
    rate_file = 'rate.txt'
    Utils.write_rate_file(mut_rate, rate_file)
    ML_tree_files = [path + "disentangler_test0_MLTree" + str(i) + ".tre" for i in range(segments)]
    if reconstruct:
        for i in range(segments):
            #RAxML.get_raxml_tree(seq_files[i], ML_tree_files[i])
            RAxML.get_dated_raxml_tree(seq_files[i], ML_tree_files[i], tip_date_file, rate_file)
    
    "Get reference tree from consensus or user specified tree"
    consensus = True
    if consensus:
        ref = get_consensus_tree(ML_tree_files)
        #ref.write(path=path+"disentangler_test1_MLconsensus.tre",schema='newick',suppress_annotations=True,suppress_rooting=True)
    else:
        "Or give tree file to use as reference"
        ref_file = path + "disentangler_test0_MLTree0.tre" # could use MCC tree
        taxa = dendropy.TaxonNamespace()
        ref = dendropy.Tree.get(file=open(ref_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
   
    "Get prior tree ratios"
    prior_tree_ratio= [] # [0.1] * segments
    seg_lengths = []
    for loc in range(segments):
        seq_file = seq_files[loc] # path + "disentangler_test1_tree" + str(loc) + ".fasta"
        segment_length = len(list(SeqIO.parse(seq_file, "fasta"))[0])
        seg_lengths.append(segment_length)
    max_seg_length = max(seg_lengths)
    for loc in range(segments):
        prior_tree_ratio.append(seg_lengths[loc] / genome_length)
        #prior_tree_ratio.append(seg_lengths[loc] / max_seg_length)
    
    "Run the ARG sampler to get a tree path"
    out_report = 'arg-sampler-report.txt'
    #tree_path = sample_ARG(ML_tree_files,seq_files,ref,rho=rho,prior_tree_ratio=prior_tree_ratio,midpoint=False,use_viterbi=True,report=out_report)
    #tree_path = sample_ARG_DSLP(ML_tree_files,seq_files,ref,rho=rho,prior_gamma=prior_gamma,midpoint=False,use_viterbi=True,report=out_report)
    tree_path = sample_ARG_bb(ML_tree_files,seq_files,ref,rho=rho,lower_bound_ratio=lower_bound_ratio,prior_gamma=prior_gamma,midpoint=False,use_viterbi=True,report=out_report)
    
    plot = True
    import PlotTanglegrams
    "Plot original tanglegram"
    tanglegram_fig_name = 'tanglegram-original-trees.png' 
    if plot:
        PlotTanglegrams.plot(tree_files, tanglegram_fig_name)
    
    "Plot ML tree tanglegram"
    tanglegram_fig_name = 'tanglegram-ML-trees.png' 
    if plot:
        PlotTanglegrams.plot(ML_tree_files, tanglegram_fig_name)
    
    "Plot reconcilded tanglegram"
    tanglegram_fig_name = 'tanglegram-sampled-ARG.png'
    ARG_tree_files = [path + "disentangler_ARG_localTree" + str(i) + ".tre" for i in range(segments)]
    for idx,tr in enumerate(tree_path):
        tr.write(path=ARG_tree_files[idx],schema='newick',suppress_annotations=True,suppress_rooting=True) 
    if plot:
        PlotTanglegrams.plot(ARG_tree_files,tanglegram_fig_name)
    
    