"""
Created on Mon May 17 09:47:26 2021

Wrappers and utility functions for working with IQTree

@author: david
"""
import subprocess
import sys
import os
import dendropy

def get_iqtree_tree(seq_file,tree_file,root=True,verbose=False):
    
    "Run raxml to get ML tree"
    cmd = 'iqtree -s ' + seq_file + ' -m GTR -redo'
    try:
        output = subprocess.check_output(cmd, shell=True,stderr=subprocess.STDOUT)
        if verbose:
            sys.stdout.write(output)
    except subprocess.CalledProcessError:
        print('Execution of "%s" failed!\n' % cmd)
        sys.exit(1)

    "Rename tree"
    iq_tree_file = seq_file + '.treefile'
    try:
        os.rename(iq_tree_file, tree_file)
    except OSError:
        pass
    
    "Root tree in dendropy"
    if root:
        taxa = dendropy.TaxonNamespace()
        tree = dendropy.Tree.get(file=open(tree_file, 'r'), schema="newick", taxon_namespace=taxa)
        tree.reroot_at_midpoint()
        tree.write(path=tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
    
    "Clean up"
    try:
        os.remove(seq_file + '.bionj')
        os.remove(seq_file + '.ckp.gz')
        os.remove(seq_file + '.iqtree')
        os.remove(seq_file + '.log')
        os.remove(seq_file + '.mldist')
        os.remove('site_rates.txt')
        os.remove('site_rates_info.txt')
    except OSError:
        pass
    
def get_dated_iqtree_tree(seq_file,tree_file,tip_date_file,root=False,verbose=False):
    
    "Run raxml to get ML tree"
    cmd = 'iqtree -s ' + seq_file + ' --date ' + tip_date_file + ' --date-options "-w rate.txt"' + ' -m GTR -redo'
    try:
        output = subprocess.check_output(cmd, shell=True,stderr=subprocess.STDOUT)
        if verbose:
            sys.stdout.write(output)
    except subprocess.CalledProcessError:
        print('Execution of "%s" failed!\n' % cmd)
        sys.exit(1)

    "Rename tree"
    iq_tree_file = seq_file + '.timetree.nex'
    try:
        os.rename(iq_tree_file, tree_file)
    except OSError:
        pass
    
    "Root tree in dendropy: iqtree will automatically root dated tree"
    if root:
        taxa = dendropy.TaxonNamespace()
        tree = dendropy.Tree.get(file=open(tree_file, 'r'), schema="newick", taxon_namespace=taxa)
        tree.reroot_at_midpoint()
        tree.write(path=tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
    
    "Clean up"
    try:
        os.remove(seq_file + '.bionj')
        os.remove(seq_file + '.ckp.gz')
        os.remove(seq_file + '.iqtree')
        os.remove(seq_file + '.log')
        os.remove(seq_file + '.mldist')
        os.remove(seq_file + '.timetree.nwk')
        os.remove(seq_file + '.timetree.lsd')
        os.remove(seq_file + '.treefile')
        os.remove('site_rates.txt')
        os.remove('site_rates_info.txt')
    except OSError:
        pass