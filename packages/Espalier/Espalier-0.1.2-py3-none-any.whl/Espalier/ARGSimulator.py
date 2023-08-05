"""
Created on Thu Jul 30 07:19:56 2020

ARGSimulator simulates (local) phylogenetic trees within ARGs
Trees are simulated under a coalescent model in msprime
Sequences are simulated under a CTMC model in pyvolve

@author: david
"""

import TreeReconciler
import msprime
import dendropy
import pyvolve

def sim_ARG(sample_size=10,Ne=100,length=1e3,recombination_rate=5e-6,min_breakpoints=1,max_breakpoints=1000,plot=False):
    
    "Simulate local trees in ARG using msprime"
    
    topo_changes = 0
    breaks = 0
    while breaks < min_breakpoints or breaks > max_breakpoints: 
        ts = msprime.simulate(sample_size=sample_size, Ne=Ne, length=length, recombination_rate=recombination_rate, record_full_arg=True)
        breaks = len(ts.breakpoints(as_array=True)) - 2 # -2 because tskit counts ends as breakpoints
    
    prev_tree = None
    for tr_num, tree in enumerate(ts.trees()):
        
        if plot:
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

        prev_tree = tree.newick()
    
    if plot:
        print(ts.tables.nodes)
        print()
        print(ts.tables.edges)
        print()
        print("Recombination breakpoints: " + str(breaks))
        print()
        print("Topological changes in tree sequence: " + str(topo_changes))
    
    return ts

def sim_seqs(tree_file,seq_file,mut_rate=0.001,seq_length=1000):
    
    "User defined params"
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
    


