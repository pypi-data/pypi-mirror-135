"""
Created on Thu Jul 30 07:19:56 2020

ARGSimulator simulates (local) phylogenetic trees within ARGs
Trees are simulated under a coalescent model with recomb in msprime
Sequences are simulated under a CTMC model in pyvolve

Modified for Catherine Mo 2021-09 

@author: david
"""
from Bio import SeqIO
import msprime
import pyvolve

"""
    Simulate local trees in ARG using msprime
"""
def sim_ARG(sample_size=10,Ne=100,length=1e3,recombination_rate=5e-6,min_breakpoints=1,max_breakpoints=1000,plot=False):
    
    breaks = -1
    while breaks < min_breakpoints or breaks > max_breakpoints: 
        ts = msprime.simulate(sample_size=sample_size, Ne=Ne, length=length, recombination_rate=recombination_rate, record_full_arg=True)
        breaks = len(ts.breakpoints(as_array=True)) - 2 # -2 because tskit counts ends as breakpoints
    
    for tr_num, tree in enumerate(ts.trees()):
        
        if plot:
            print("-" * 20)
            print("tree {}: interval = {}".format(tree.index, tree.interval))
            print(tree.draw(format="unicode"))
    
    if plot:
        print("-" * 20)
        print(ts.tables.nodes)
        print()
        print(ts.tables.edges)
        print()
        print("Recombination breakpoints: " + str(breaks))
        print()
        print("-" * 20)
    
    return ts

def concate_aligns(seq_files,file_out):

    for idx, file in enumerate(seq_files):
        seq_dict = SeqIO.to_dict(SeqIO.parse(file, "fasta")) # one line alternative
        if idx == 0:
            concat_seqs = seq_dict
        else:
            for key in concat_seqs:
                concat_seqs[key] += seq_dict[key]            
    
    # Convert to list and write seq records to fasta file
    concat_records = [concat_seqs[key] for key in concat_seqs]
    SeqIO.write(concat_records, file_out, "fasta")

"""
    Simulate sequence evolution along tree in tree_file
    Assumes HKY model of molecular evolution
"""
def sim_seqs(tree_file,seq_file,mut_rate=0.001,seq_length=1000):
    
    "User defined params"
    freqs = [0.25, 0.25, 0.25, 0.25] # equil nuc freqs
    kappa = 2.75 # trans/transversion ratio
    
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
    
if  __name__ == '__main__':
    
    """
        Set pop gen params for simulations
    """
    sample_size = 20 # number of samples/tips
    Ne =  1.0 / 2 # effective pop size (divide by two for haploids b/c msprime assumes individuals are diploid)
    genome_length = 2 # numbers of sites in genome
    recomb_rate = 0.0 # recombination rate per genome
    rho = recomb_rate / genome_length # rate per site
    mut_rate = 0.01 # mutation rate per site per unit time
    
    min_breakpoints = 0 # conditions sims on minimum number of recombination events (i.e. breakpoints)
    sim_path = './'
    plot = True # plot simulated trees?
    
    """
        Simulate ARG/tree sequence (ts) using msprime
        Will be a single phylogeny if recombination rate = 0
    """
    ts = sim_ARG(sample_size=sample_size,Ne=Ne,length=genome_length,recombination_rate=rho,min_breakpoints=min_breakpoints,plot=plot)
    ts.dump(sim_path + 'msprime_tree_sequence')
    breaks = ts.breakpoints(as_array=True)
    segments = len(breaks) - 1 # number of non-recombinant segments between breakpoints
        
    """
        Simulate sequence evolution along each tree in ts
        Write local tree and seq files
    """
    tree_files = [sim_path + "sim_tree" + str(i) + ".tre" for i in range(segments)]
    seq_files = [sim_path + "sim_tree" + str(i) + ".fasta" for i in range(segments)]
    for tr_num, tree in enumerate(ts.trees()):
        seq_length = round(tree.interval[1] - tree.interval[0])
        with open(tree_files[tr_num], "w") as text_file:
            print(tree.newick(), file=text_file)
        sim_seqs(tree_files[tr_num],seq_files[tr_num],mut_rate=mut_rate,seq_length=seq_length)
    
    """
        Concatenate sequence files for local trees into one fasta file
    """
    concat_seq_file = sim_path + 'concat_seqs.fasta'
    concate_aligns(seq_files,concat_seq_file)

