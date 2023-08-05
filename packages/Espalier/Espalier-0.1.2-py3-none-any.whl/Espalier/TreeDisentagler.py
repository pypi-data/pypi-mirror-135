#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 15:35:30 2020

@author: david
"""

import TreeReconciler
import msprime
import dendropy
import pyvolve
import subprocess
import sys
import os

def simulate_seqs(tree_file,seq_file,seq_length=1000):
    
    "User defined params"
    mut_rate = 0.001
    freqs = [0.25, 0.25, 0.25, 0.25]
    kappa = 2.75
    
    "Read in phylogeny along which Pyvolve should simulate"
    "Scale_tree sets absolute mutation rate"
    my_tree = pyvolve.read_tree(file = tree_file, scale_tree = mut_rate)
    #pyvolve.print_tree(my_tree) # Print the parsed phylogeny
    
    "Or just use an HKY model with kappa"
    nuc_model = pyvolve.Model( "nucleotide", {"kappa":kappa, "state_freqs":freqs})
    
    "Define a Partition object which evolves set # of positions according to my_model"
    my_partition = pyvolve.Partition(models = nuc_model, size = seq_length)
    
    "Define an Evolver instance to evolve a single partition"
    my_evolver = pyvolve.Evolver(partitions = my_partition, tree = my_tree) 
    
    "Evolve sequences with custom file names"
    #my_evolver(ratefile = "AMR_ratefile.txt", infofile = "AMR_infofile.txt", seqfile = "AMR-seqsim.fasta" )
    my_evolver(seqfile = seq_file)

def get_raxml_tree(seq_file,tree_file,root=True):
    
    "Run raxml to get ML tree"
    cmd = 'raxml -m GTRGAMMA -p 12345 -s ' + seq_file + ' -n test -T 2'
    try:
        output = subprocess.check_output(cmd, shell=True,stderr=subprocess.STDOUT)
        sys.stdout.write(output)
    except subprocess.CalledProcessError:
        print('Execution of "%s" failed!\n' % cmd)
        sys.exit(1)
    
    try:
        os.rename('RAxML_bestTree.test', tree_file)
    except OSError:
        pass
    
    if root:
        
        taxa = dendropy.TaxonNamespace()
        tree = dendropy.Tree.get(file=open(tree_file, 'r'), schema="newick", taxon_namespace=taxa)
        tree.reroot_at_midpoint()
        tree.write(path=tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
    
    try:
        os.remove('RAxML_info.test')
        os.remove('RAxML_log.test')
        os.remove('RAxML_parsimonyTree.test')
        os.remove('RAxML_result.test')
        os.remove('site_rates.txt')
        os.remove('site_rates_info.txt')
    except OSError:
        pass


if  __name__ == '__main__':

    sim = True
    min_breakpoints = 2
    
    "Simulate tree series"
    topo_changes = 0
    if sim:
        breaks = 0
        while breaks < min_breakpoints + 2:
            ts = msprime.simulate(sample_size=10, Ne=100, length=1e3, recombination_rate=5e-6, record_full_arg=True)
            breaks = len(ts.breakpoints(as_array=True))
        
        prev_tree = None
        for tr_num, tree in enumerate(ts.trees()):
            
            print("-" * 20)
            print("tree {}: interval = {}".format(tree.index, tree.interval))
            print(tree.draw(format="unicode"))
            
            "Test for discordance"
            if tr_num > 0:
                taxa = dendropy.TaxonNamespace()
                ref = dendropy.Tree.get(data=prev_tree, schema="newick", rooting="default-rooted", taxon_namespace=taxa)
                alt = dendropy.Tree.get(data=tree.newick(), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
                if TreeReconciler.test_discordance(ref,alt):
                    topo_changes += 1
            
            "Simulate sequence data for local tree"
            local_tree_file = 'disentangler_test1_tree' + str(tr_num) + ".tre"
            local_seq_file =  'disentangler_test1_tree' + str(tr_num) + ".fasta"
            with open(local_tree_file, "w") as text_file:
                print(tree.newick(), file=text_file)
            seq_length = round(tree.interval[1] - tree.interval[0])
            simulate_seqs(local_tree_file,local_seq_file,seq_length)
            
            "Reconstruct local ML tree"
            raxml_tree_file = 'disentangler_test1_MLTree' + str(tr_num) + ".tre"
            get_raxml_tree(local_seq_file, raxml_tree_file)
        
            prev_tree = tree.newick()
        
        print(ts.tables.nodes)
        print()
        print(ts.tables.edges)
        print()
        print("Recombination breakpoints: " + str(breaks))
        print()
        print("Topological changes in tree sequence: " + str(topo_changes))
    
    "Plot original tanglegram"
    import PlotTanglegrams
    fig_name = 'tanglegram.png'
    tree_file = "disentangler_test1_MLTree"
    if sim:
        segments = [str(i) for i in range(breaks-1)]   
    else:
        segments=['0','1','2']  
    PlotTanglegrams.plot(tree_file,segments,fig_name)
    
    "Sequentially disentangle trees"
    plot = False
    for loc in range(len(segments)):
        
        "This should be reconciled tree from previous segment if not at left-most tree"
        if loc > 0:
            ref_file = "disentangler_test1_reconciled" + str(loc-1) + ".tre" # previous tree
        else:
            "Reconcile with reference or self"
            ref_file = "disentangler_test1_MLTree0.tre" 
        alt_file = "disentangler_test1_MLTree" + str(loc) + ".tre" # local tree
        
        taxa = dendropy.TaxonNamespace()
        ref = dendropy.Tree.get(file=open(ref_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
        alt = dendropy.Tree.get(file=open(alt_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
        
        if plot:
            print("Reference tree:")
            ref.print_plot()
            print("Alternate tree:")
            alt.print_plot()
        
        "Deep copy trees"
        #ref_clone = ref.clone(depth=2)
        #alt_clone = alt.clone(depth=2)
        
        "Get maximum agreement forest"
        maf = TreeReconciler.get_maf_4cut(ref,alt,plot=False)
        if plot:
            TreeReconciler.plot_maf(maf)
        
        rec_tree = TreeReconciler.reconcile_trees(ref,alt,maf,plot=False)
        
        rec_file = "disentangler_test1_reconciled" + str(loc) + ".tre" 
        rec_tree.write(path=rec_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
        
    "Plot reconcilded tanglegram"
    fig_name = 'tanglegram-reconciled.png'
    tree_file = "disentangler_test1_reconciled"  
    PlotTanglegrams.plot(tree_file,segments,fig_name)
    
    
    "Topo changes between ML trees"
    "And topo changes in reconciled trees"
    # def count_topo_changes():
    true_changes = []  
    ML_changes = []
    reconciled_changes = []
    for loc in range(1,len(segments)):
        
        "Find true topo changes between local trees"
        ref_file = "disentangler_test1_tree" + str(loc-1) + ".tre" # local tree
        alt_file = "disentangler_test1_tree" + str(loc) + ".tre" # local tree
        taxa = dendropy.TaxonNamespace()
        ref = dendropy.Tree.get(file=open(ref_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
        alt = dendropy.Tree.get(file=open(alt_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
        true_changes.append(TreeReconciler.get_spr_dist(ref,alt))
        
        "Find topo changes between ML trees"
        ref_file = "disentangler_test1_MLTree" + str(loc-1) + ".tre" # local tree
        alt_file = "disentangler_test1_MLTree" + str(loc) + ".tre" # local tree
        ref = dendropy.Tree.get(file=open(ref_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
        alt = dendropy.Tree.get(file=open(alt_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
        ML_changes.append(TreeReconciler.get_spr_dist(ref,alt))
        
        "Find topo changes between reconciled trees"
        ref_file = "disentangler_test1_reconciled" + str(loc-1) + ".tre" # local tree
        alt_file = "disentangler_test1_reconciled" + str(loc) + ".tre" # local tree
        ref = dendropy.Tree.get(file=open(ref_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
        alt = dendropy.Tree.get(file=open(alt_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
        reconciled_changes.append(TreeReconciler.get_spr_dist(ref,alt))
        
    print("True topo changes: ")
    print(true_changes)
    print("ML topo changes: ")
    print(ML_changes)
    print("Reconciled topo changes: ")
    print(reconciled_changes)
    
    