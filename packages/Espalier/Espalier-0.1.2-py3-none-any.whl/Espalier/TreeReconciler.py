"""
Created on Tue Apr 28 13:23:58 2020

TreeReconciler - reconciles topological differeces between pairs of trees

@author: david
"""

import msprime
import dendropy
import numpy as np
import math
import random
import RAxML
from Bio import AlignIO
from Bio import SeqIO

# For profiling only
import time

"Global variable cluster determines how system calls to os are made"
#cluster = True

raxml_path = 'raxmlHPC-PTHREADS-AVX' # for BRC iMac
#raxml_path = 'raxmlHPC-PTHREADS-SSE3' # for cluster
#raxml_path = 'raxml' # for MacBook
                
def get_root_node(tree):
    for nd in tree.preorder_node_iter():
        root = nd
        break
    return root

def get_root_edge(tree):
    for ed in tree.preorder_edge_iter():
        root = ed
        break
    return root

def deep_root_pair(ref,alt):
    
    "Deep root a pair of trees preserving taxon namespace by writing and reading in new newick trees"
    
    ref_deep_rooted = add_deep_root(ref)
    alt_deep_rooted = add_deep_root(alt)
    
    "Write out and read in newick trees to update taxa namespaces"
    temp_ref_file = 'temp_ref.tre'
    temp_alt_file = 'temp_alt.tre'
    ref_deep_rooted.write(path=temp_ref_file,schema='newick',suppress_annotations=True)
    alt_deep_rooted.write(path=temp_alt_file,schema='newick',suppress_annotations=True)
    taxa = dendropy.TaxonNamespace()
    ref_deep_rooted = dendropy.Tree.get(file=open(temp_ref_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
    alt_deep_rooted = dendropy.Tree.get(file=open(temp_alt_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)

    return ref_deep_rooted, alt_deep_rooted

def add_deep_root(tree,reroot=True):
    
    "Add deep root above current root by adding dummy node at new root"
    new_tree = dendropy.Tree(taxon_namespace=tree.taxon_namespace)
    dummy = new_tree.seed_node.new_child() # dummy node above new root
    dummy.edge.length = 1
    curr_root = get_root_node(tree)
    new_tree.seed_node.add_child(curr_root)
    
    if reroot:
        new_root = get_root_node(new_tree)
        new_tree.reroot_at_node(new_root, update_bipartitions=False)    
    
    "Add taxon label for dummy node"
    new_tree.taxon_namespace.add_taxon(dendropy.Taxon("dummy"))
    dummy.taxon = new_tree.taxon_namespace.get_taxon("dummy")
    
    return new_tree

def add_deep_root_with_ages(tree,reroot=True):

    "Get age of curr root in tree"
    curr_root = get_root_node(tree)
    tree.calc_node_ages(ultrametricity_precision=False)
    curr_root_age = curr_root.age
    
    "Add deep root above current root by adding dummy node at new root"
    new_tree = dendropy.Tree(taxon_namespace=tree.taxon_namespace)
    dummy = new_tree.seed_node.new_child() # dummy node above new root
    dummy.edge.length = curr_root_age
    
    new_tree.seed_node.add_child(curr_root)
    curr_root.edge.length = 0.0
    
    if reroot:
        new_root = get_root_node(new_tree)
        new_tree.reroot_at_node(new_root, update_bipartitions=False)    
    
    "Add taxon label for dummy node"
    new_tree.taxon_namespace.add_taxon(dendropy.Taxon("dummy"))
    dummy.taxon = new_tree.taxon_namespace.get_taxon("dummy")
    
    return new_tree

def remove_deep_root(tree):
    
    tree.prune_taxa_with_labels(["dummy"])
    
    return tree

def plot_maf(maf):
        
    print("-" * 25)
    print("Maximum agreement forest:")
    print("-" * 25)
    for tr in maf:
        print()
        if len(tr.nodes()) > 1:
            tr.print_plot()
        else:
            print('---' + tr.nodes()[0].taxon.label)
    
def get_leaf_indexes(tree):
    
    "Create a dict that maps taxa to bipartition indexes"
    tree.encode_bipartitions()
    leaf_bipart_index_dict = {}
    for edge in tree.leaf_edge_iter():  
        taxon = edge.head_node.taxon.label # use label instead of taxon objects so compatible with deep cloning
        bitstring = edge.bipartition.leafset_as_bitstring() # don't actually need bitstring since these are always in order
        leaf_bipart_index_dict[taxon] =  bitstring.index('1')
    #for key, value in leaf_bipart_index_dict.items(): print(key, value)
    
    return leaf_bipart_index_dict

def get_bipart_indexes(tree):
    
    "Create a dict that maps taxa to bipartition indexes"
    tree.encode_bipartitions()
    bipart_index_leaf_dict = {}
    for edge in tree.leaf_edge_iter():  
        taxon = edge.head_node.taxon.label # use label instead of taxon objects so compatible with deep cloning
        bitstring = edge.bipartition.leafset_as_bitstring() # don't actually need bitstring since these are always in order
        bipart_index_leaf_dict[bitstring.index('1')] = taxon  
    #for key, value in leaf_bipart_index_dict.items(): print(key, value)
    
    return bipart_index_leaf_dict

def get_bitstring_dict(tree):
    
    "Create a dict that maps taxa to bipartition indexes"
    tree.encode_bipartitions()
    bitstring_edge_dict = {}
    for edge in tree.postorder_edge_iter():  
        bitstring = edge.bipartition.leafset_as_bitstring() # don't actually need bitstring since these are always in order
        bitstring_edge_dict[bitstring] = edge  
    return bitstring_edge_dict


def test_discordance(ref,alt):
    ref.encode_bipartitions() # need to encode bipartitions before can access them    
    alt.encode_bipartitions()
    ref_bipartition_dict = ref.split_bitmask_edge_map #dictionary mapping split bitmasks (integers) to their corresponding edges through the Tree.split_bitmask_edge_map attribute
    trees_discordant = update_concordance(alt,ref_bipartition_dict)
    return trees_discordant

def update_concordance(alt,ref_bipartition_dict):
    
    "Mark each edge and its child node as concordant/discordant"
    trees_discordant = False
    for edge in alt.postorder_edge_iter():
        bitmask = edge.leafset_bitmask
        ref_edge = ref_bipartition_dict.get(bitmask,None)
        if ref_edge: # if edge bipartition exists in reference 
            #print('Bipartition is concordant')
            edge.concordant = True
            edge.head_node.concordant = True
        else:
            #print('Bipartition is discordant')
            edge.concordant = False
            edge.head_node.concordant = False
            trees_discordant = True
            
    return trees_discordant

"""
    Think we can remove this -- never used
"""
def update_concordance_test_cut(alt,ref_bitstring_dict):
    
    "Mark each edge and its child node as concordant/discordant"
    trees_discordant = False
    for edge in alt.postorder_edge_iter():
        #bitmask = edge.leafset_bitmask
        bitstring = edge.temp_bitstring
        ref_edge = ref_bitstring_dict.get(bitstring,None)
        if ref_edge: # if edge bipartition exists in reference 
            #print('Bipartition is concordant')
            edge.concordant = True
            edge.head_node.concordant = True
        else:
            #print('Bipartition is discordant')
            edge.concordant = False
            edge.head_node.concordant = False
            trees_discordant = True
            
    return trees_discordant

def count_discordant_edges(alt,ref_bipartition_dict):
    
    "Count discordant edges in between trees"
    count = 0
    for edge in alt.postorder_edge_iter():
        bitmask = edge.leafset_bitmask
        ref_edge = ref_bipartition_dict.get(bitmask,None)
        if not ref_edge: # if edge bipartition exists in reference 
            count += 1
            
    return count

def count_discordant_edges_test_cut(alt,ref_bitstring_dict):
    
    "Count discordant edges in between trees"
    count = 0
    for edge in alt.postorder_edge_iter():
        bitstring = edge.temp_bitstring
        ref_edge = ref_bitstring_dict.get(bitstring,None)
        if not ref_edge: # if edge bipartition exists in reference 
            count += 1
            
    return count


def get_spr_dist(ref,alt):
    
    if ref.taxon_namespace is not alt.taxon_namespace:
        alt.taxon_namespace = ref.taxon_namespace
        alt.reindex_subcomponent_taxa()
    maf = get_maf_4cut(ref,alt)
    spr_dist = len(maf) - 1
    
    return spr_dist

def get_maf_4cut_noclone(ref,alt,deep_root=False,plot=False):
    
    """
        This algorithm tries to find the MAF by identifying one of four possible edges to cut
        If a given edge in ALT is discordant with subtrees A,C
        We find sibling of A in REF and call this B
        And find sibling of C in REF and call this D
        Note: B or D may not exist in ALT
        Then cut edge A,B,C or D that minimizes discordance in the pruned trees
    """
    
    "Deep copy original trees so we don't lose them - do we need to do this?"
    #ref = ref_in.clone(depth=2)
    #alt = alt_in.clone(depth=2)
    
    "Deep root trees by adding dummy node as outgroup"
    if deep_root:
        ref,alt = deep_root_pair(ref,alt)
    
    ref.encode_bipartitions() # need to encode bipartitions before can access them    
    alt.encode_bipartitions()
    
    ref_bipartition_dict = ref.split_bitmask_edge_map #dictionary mapping split bitmasks (integers) to their corresponding edges through the Tree.split_bitmask_edge_map attribute
    #for key, value in ref_bipartition_dict.items(): print(key, value)
    
    trees_discordant = update_concordance(alt,ref_bipartition_dict)
        
    "The MAF algorithm"
    forest = dendropy.TreeList() # subtrees in MAF. Made this a TreeList instead of list to preserve taxon_namespace across all sub trees in MAF
    counter = 0
    while trees_discordant:
                    
        "Find first discordant edge"
        for edge in alt.postorder_edge_iter():
            if not edge.concordant: break
        parent = edge.head_node #first discordant sibling pair (edge) in t1
        edge_cut_list = parent.child_edges()
        
        "Get sibling of A and C in REF"
        ref_bipartition_dict = ref.split_bitmask_edge_map
        alt_bipartition_dict = alt.split_bitmask_edge_map
        edge_A = edge_cut_list[0]
        edge_C = edge_cut_list[1]
        
        "Get sibling edge B"
        ref_edge_A = ref_bipartition_dict.get(edge_A.split_bitmask,None)
        parent_edge_A = ref_edge_A.tail_node
        child_edges = parent_edge_A.child_edges()
        if child_edges[0] is ref_edge_A:
            sibling_edge = child_edges[1]
        else:
            sibling_edge = child_edges[0]
        alt_edge_B = alt_bipartition_dict.get(sibling_edge.split_bitmask,None)
        if alt_edge_B:
            edge_cut_list.append(alt_edge_B)
        
        "Get sibling edge D"
        ref_edge_C = ref_bipartition_dict.get(edge_C.split_bitmask,None)
        parent_edge_C = ref_edge_C.tail_node
        child_edges = parent_edge_C.child_edges()
        if child_edges[0] is ref_edge_C:
            sibling_edge = child_edges[1]
        else:
            sibling_edge = child_edges[0]
        alt_edge_D = alt_bipartition_dict.get(sibling_edge.split_bitmask,None)
        if alt_edge_D:
            edge_cut_list.append(alt_edge_D)
        
        "Cut each edge in edge_cut_list"
        "Compare resulting alt and ref trees for discordance"
        D = [] # array to hold discordance metric
        #alt_cut_trees = []
        #ref_cut_trees = []
        #components = []
        for edge in edge_cut_list:
            
            """
                Here we don't actually clone ref or alt and make cuts
                Rather we test the effect a cut would have on tree concordance
                By temporarilly updating the bitstring of each bipartition as if we had made the cut
                Bitstrings are updated by subtracting the bitstring of the cut edge bipartition from the bitstring of all other nodes
                Such that the bitstring reflects the split bipartition that would exist without the cut edge/subtree
            """
            
            bitmask = edge.split_bitmask
            alt_cut_edge = alt_bipartition_dict.get(bitmask,None)
            ref_cut_edge = ref_bipartition_dict.get(bitmask,None)

            "Extract subtree from alt and place in subtree forest"
            #parent_nd = alt_cut_edge.tail_node
            #child_nd = alt_cut_edge.head_node
            #component = alt_cut.extract_tree_with_taxa(taxa=set([lf.taxon for lf in child_nd.leaf_iter()]))
            #components.append(component)
            
            """
                Reversible remove does not work here since we need to update bipartitions -- which will cause reinsert nodes to fail
            """
            #alt_cut_connection_list = parent_nd.reversible_remove_child(child_nd, suppress_unifurcations=False)
            #alt.update_bipartitions()
            #parent_nd.reinsert_nodes(alt_cut_connection_list)
        
            "Prune subtree from alt_cut"
            #alt_cut_child = alt_cut_edge.head_node
            #alt.prune_subtree(alt_cut_child, update_bipartitions=True, suppress_unifurcations=True)
            
            "Add bitstrings for cut"
            cut_bitstring = alt_cut_edge.split_as_bitstring()
            cut_bit_array = np.array(list(map(int,list(cut_bitstring))))
            cut_leaf_pos = [pos for pos, char in enumerate(cut_bitstring) if char == '1']
            cut_leaf_pos.sort(reverse=True)
            alt_bitstring_dict = {}
            for edge in alt.postorder_edge_iter():
                
                "Deleting cut leaf taxa from bitstring"
                temp_bitstring = edge.split_as_bitstring()
                #temp_bitstring = ''.join([temp_bitstring[i] for i in xrange(len(temp_bitsring)) if i not in leaf_pos])
                
                "Or byte array deletion"
                ba = bytearray(temp_bitstring,'utf-8')
                for pos in cut_leaf_pos: del ba[pos]
                temp_bitstring =  ba.decode("utf-8")
                
                "Converting to np array, subtracting then re-joining"
                #edge_bit_array = np.array(list(map(int,list(edge.split_as_bitstring()))))
                #temp_bit_array = edge_bit_array - cut_bit_array
                #temp_bit_array[temp_bit_array < 0] = 0
                ##temp_bitstring = "".join(map(str, temp_bit_array)) # profiling shows this is surprisingly slow!
                #temp_bitstring = np.array2string(temp_bit_array,separator='')[1:-1]
                
                edge.temp_bitstring = temp_bitstring
                alt_bitstring_dict.update({temp_bitstring:edge.split_as_bitstring()})
        
        
            "Find and prune corresponding edge in ref_cut tree"
            #ref_cut_child = ref_cut_edge.head_node
            #ref.prune_subtree(ref_cut_child, update_bipartitions=True, suppress_unifurcations=True)
            
            cut_bitstring = ref_cut_edge.split_as_bitstring()
            cut_bit_array = np.array(list(map(int,list(cut_bitstring))))
            cut_leaf_pos = [pos for pos, char in enumerate(cut_bitstring) if char == 1]
            cut_leaf_pos.sort(reverse=True)
            ref_bitstring_dict = {}
            for edge in ref.postorder_edge_iter():
                
                "Deleting cut leaf taxa from bitstring"
                temp_bitstring = edge.split_as_bitstring()
                #temp_bitstring = ''.join([temp_bitstring[i] for i in xrange(len(temp_bitsring)) if i not in leaf_pos])
                
                "Or byte array deletion"
                ba = bytearray(temp_bitstring,'utf-8')
                for pos in cut_leaf_pos: del ba[pos]
                temp_bitstring =  ba.decode("utf-8")
                
                #edge_bit_array = np.array(list(map(int,list(edge.split_as_bitstring()))))
                #temp_bit_array = edge_bit_array - cut_bit_array
                #temp_bit_array[temp_bit_array < 0] = 0
                #temp_bitstring = "".join(map(str, temp_bit_array))
                ##temp_bitstring = np.array2string(temp_bit_array,separator='')[1:-1]
                
                edge.temp_bitstring = temp_bitstring
                ref_bitstring_dict.update({temp_bitstring:edge.split_as_bitstring()})
            
            "Update concordance"
            #ref_cut_bipartition_dict = ref.split_bitmask_edge_map
            #trees_discordant = update_concordance_test_cut(alt, ref_bitstring_dict)
            D.append(count_discordant_edges_test_cut(alt, ref_bitstring_dict))
            #alt_cut_trees.append(alt_cut)
            #ref_cut_trees.append(ref_cut)
            
        #print("D: " + str(D))
        
        "Decide which cut minimizes D"
        cut = D.index(min(D))
     
        "Actually make cut"
        edge = edge_cut_list[cut]
        bitmask = edge.split_bitmask
        alt_cut_edge = alt_bipartition_dict.get(bitmask,None)
        ref_cut_edge = ref_bipartition_dict.get(bitmask,None)
        
        "Extract subtree from alt and place in subtree forest"
        alt_cut_child = alt_cut_edge.head_node
        component = alt.extract_tree_with_taxa(taxa=set([lf.taxon for lf in alt_cut_child.leaf_iter()]))

        "Prune subtree from alt/ref"
        alt.prune_subtree(alt_cut_child, update_bipartitions=True, suppress_unifurcations=True)
        ref_cut_child = ref_cut_edge.head_node
        ref.prune_subtree(ref_cut_child, update_bipartitions=True, suppress_unifurcations=True)
        
        "Add component to forest"
        #cut_tree = components[cut]
        forest.append(component)
        
        counter += 1
        if plot:
            print("-" * 20)
            print("MAF iteration: " + str(counter))
            print("Reference tree:")
            ref.print_plot()
            print()
            print("Alternate tree:")
            alt.print_plot()
            print()
            print("Cut tree:")
            if len(component.nodes()) > 1:
                component.print_plot()
            else:
                print('---' + component.nodes()[0].taxon.label)
            print()
            print("-" * 20)
            
        "Make sure trees_discordant is updated"
        ref_bipartition_dict = ref.split_bitmask_edge_map 
        trees_discordant = update_concordance(alt,ref_bipartition_dict)
    
    "Remove dummy node at deep root"
    if deep_root:
        alt = remove_deep_root(alt)
    
    forest.append(alt) # append what's left of alt (should at least be a rooted tree with two edges)
    return forest

def get_maf_4cut(ref_in,alt_in,deep_root=False,plot=False):
    
    """
        This algorithm tries to find the MAF by identifying one of four possible edges to cut
        If a given edge in ALT is discordant with subtrees A,C
        We find sibling of A in REF and call this B
        And find sibling of C in REF and call this D
        Note: B or D may not exist in ALT
        Then cut edge A,B,C or D that minimizes discordance in the pruned trees
        
        NOTE: Order of ref and alt input args can be exchanged but MAF substrees are extracted from alt by default
    """
    
    "Deep copy original trees so we don't lose them - do we need to do this?"
    ref = ref_in.clone(depth=2)
    alt = alt_in.clone(depth=2)
    
    "Deep root trees by adding dummy node as outgroup"
    if deep_root:
        ref,alt = deep_root_pair(ref,alt)
    
    ref.encode_bipartitions() # need to encode bipartitions before can access them    
    alt.encode_bipartitions()
    
    ref_bipartition_dict = ref.split_bitmask_edge_map #dictionary mapping split bitmasks (integers) to their corresponding edges through the Tree.split_bitmask_edge_map attribute
    #for key, value in ref_bipartition_dict.items(): print(key, value)
    
    trees_discordant = update_concordance(alt,ref_bipartition_dict)
        
    "The MAF algorithm"
    forest = dendropy.TreeList() # subtrees in MAF. Made this a TreeList instead of list to preserve taxon_namespace across all sub trees in MAF
    counter = 0
    while trees_discordant:
                    
        "Find first discordant edge"
        for edge in alt.postorder_edge_iter():
            if not edge.concordant: break
        parent = edge.head_node #first discordant sibling pair (edge) in t1
        edge_cut_list = parent.child_edges()
        
        "Get sibling of A and C in REF"
        ref_bipartition_dict = ref.split_bitmask_edge_map
        alt_bipartition_dict = alt.split_bitmask_edge_map
        edge_A = edge_cut_list[0]
        edge_C = edge_cut_list[1]
        
        "Get sibling edge B"
        ref_edge_A = ref_bipartition_dict.get(edge_A.split_bitmask,None)
        parent_edge_A = ref_edge_A.tail_node
        child_edges = parent_edge_A.child_edges()
        if child_edges[0] is ref_edge_A:
            sibling_edge = child_edges[1]
        else:
            sibling_edge = child_edges[0]
        alt_edge_B = alt_bipartition_dict.get(sibling_edge.split_bitmask,None)
        if alt_edge_B:
            edge_cut_list.append(alt_edge_B)
        
        "Get sibling edge D"
        ref_edge_C = ref_bipartition_dict.get(edge_C.split_bitmask,None)
        parent_edge_C = ref_edge_C.tail_node
        child_edges = parent_edge_C.child_edges()
        if child_edges[0] is ref_edge_C:
            sibling_edge = child_edges[1]
        else:
            sibling_edge = child_edges[0]
        alt_edge_D = alt_bipartition_dict.get(sibling_edge.split_bitmask,None)
        if alt_edge_D:
            edge_cut_list.append(alt_edge_D)
        
        "Cut each edge in edge_cut_list"
        "Compare resulting alt and ref trees for discordance"
        D = [] # array to hold discordance metric
        alt_cut_trees = []
        ref_cut_trees = []
        components = []
        for edge in edge_cut_list:
            
            alt_cut = alt.clone(depth=2) #Deep copy tree
            ref_cut = ref.clone(depth=2) #Deep copy tree
            
            alt_cut_bipartition_dict = alt_cut.split_bitmask_edge_map
            ref_cut_bipartition_dict = ref_cut.split_bitmask_edge_map
            bitmask = edge.split_bitmask
            alt_cut_edge = alt_cut_bipartition_dict.get(bitmask,None)
            ref_cut_edge = ref_cut_bipartition_dict.get(bitmask,None)
            
            "Make sure we're getting the correct edges"
            #edge_taxa = set([lf.taxon.label for lf in edge.head_node.leaf_iter()])
            #alt_cut_edge_taxa = set([lf.taxon.label for lf in alt_cut_edge.head_node.leaf_iter()])
            #ref_cut_edge_taxa = set([lf.taxon.label for lf in ref_cut_edge.head_node.leaf_iter()])

            "Extract subtree from alt and place in subtree forest"
            child_nd = alt_cut_edge.head_node
            component = alt_cut.extract_tree_with_taxa(taxa=set([lf.taxon for lf in child_nd.leaf_iter()]))
            components.append(component)
        
            "Prune subtree from alt_cut"
            alt_cut.prune_subtree(child_nd, update_bipartitions=True, suppress_unifurcations=True)
        
            "Find and prune corresponding edge in ref_cut tree"
            ref_cut_child = ref_cut_edge.head_node
            ref_cut.prune_subtree(ref_cut_child, update_bipartitions=True, suppress_unifurcations=True)
            
            "Update concordance"
            ref_cut_bipartition_dict = ref_cut.split_bitmask_edge_map
            trees_discordant = update_concordance(alt_cut,ref_cut_bipartition_dict)
            D.append(count_discordant_edges(alt_cut,ref_cut_bipartition_dict))
            alt_cut_trees.append(alt_cut)
            ref_cut_trees.append(ref_cut)
        
        "Decide which cut minimizes D"
        cut = D.index(min(D))
        "Set alt and ref for next iter"
        alt = alt_cut_trees[cut]
        ref = ref_cut_trees[cut]
        "Add component to forest"
        cut_tree = components[cut]
        forest.append(components[cut])
        
        counter += 1
        if plot:
            print("-" * 20)
            print("MAF iteration: " + str(counter))
            print("Reference tree:")
            ref.print_plot()
            print()
            print("Alternate tree:")
            alt.print_plot()
            print()
            print("Cut tree:")
            if len(cut_tree.nodes()) > 1:
                cut_tree.print_plot()
            else:
                print('---' + cut_tree.nodes()[0].taxon.label)
            print()
            print("-" * 20)
            
        "Make sure trees_discordant is updated"
        ref_bipartition_dict = ref.split_bitmask_edge_map 
        trees_discordant = update_concordance(alt,ref_bipartition_dict)
    
    "Remove dummy node at deep root"
    if deep_root:
        alt = remove_deep_root(alt)
    
    forest.append(alt) # append what's left of alt (should at least be a rooted tree with two edges)
    return forest

"""
    Made a safe copy while testing new version: can delete once new version is tested
"""
def find_attachment_edge_copy(rec_tree,alt_tree,subtree_taxa,rectree_taxa):
    
    "Get bipart_index_leaf_dict - maps bipartition indexes (keys) to taxon lables (values)"
    bipart_index_leaf_dict = get_bipart_indexes(alt_tree)
    #for key, value in bipart_index_leaf_dict.items(): print(key, value)
    
    "Find edge where subtree attaches in alt tree" 
    "Note: this will be the parent of the first edge that includes all subtree_taxa in its leaf set"
    "BUT this edge may not exist in rec_tree yet if none of the taxa descending from attachment edge have been added to rec_tree yet"
    for edge in alt_tree.postorder_edge_iter():
        edge_leafset_bitstring = edge.bipartition.leafset_as_bitstring()
        edge_taxa = set([bipart_index_leaf_dict[pos] for pos, char in enumerate(edge_leafset_bitstring) if char == '1'])
        if subtree_taxa.issubset(edge_taxa): # subtree_taxa are subset of all edge_taxa
            break
    attachment_edge_leafset = edge.tail_node.leafset_as_bitstring()
    attachment_edge_taxa_set = set([bipart_index_leaf_dict[pos] for pos, char in enumerate(attachment_edge_leafset) if char == '1'])
    
    """
        BIG PROBLEM: There may be no equivalent edge to attach to if none of the taxa in attachment_edge_taxa_set have been added yet
        Possible solution: if taxa_set_intersect is null set move to parent of attachment edge until union is not null set
    """
    
    "Find edge equivalent to the attachment edge in rec_tree"
    "Note: this edge will have all taxa in attachment_edge_taxa_set that are also taxa the rec_tree"
    taxa_set_intersection = attachment_edge_taxa_set & rectree_taxa
    while not taxa_set_intersection: # while intersect is null set
        edge = edge.tail_node.edge # get parent edge
        attachment_edge_leafset = edge.tail_node.leafset_as_bitstring()
        attachment_edge_taxa_set = set([bipart_index_leaf_dict[pos] for pos, char in enumerate(attachment_edge_leafset) if char == '1'])
        taxa_set_intersection = attachment_edge_taxa_set & rectree_taxa
    for edge in rec_tree.postorder_edge_iter():
        edge_taxa = set([lf.taxon.label for lf in edge.head_node.leaf_iter()])
        if not taxa_set_intersection.difference(edge_taxa): 
            "If there is no difference:"
            break
    attachment_edge = edge # edge subtree will be attached to in rec_tree
    #print([lf.taxon.label for lf in attachment_edge.head_node.leaf_iter()])
    return attachment_edge

def find_attachment_edge(rec_tree,alt_tree,subtree_taxa,rectree_taxa):
    
    """
        Find edge where subtree attaches in alt tree
        Attachment edge will be the parent of the first edge that includes all subtree_taxa in its leaf set"
    """
    for edge in alt_tree.postorder_edge_iter():
        edge_taxa = set([lf.taxon.label for lf in edge.head_node.leaf_iter()])
        if subtree_taxa.issubset(edge_taxa): # subtree_taxa are subset of all edge_taxa
            break
    
    """
        Find edge equivalent to the attachment edge in rec_tree
        Equivalent edge will have all taxa in attachment_edge_taxa_set that are also taxa the rec_tree
        NOTE: There may be no equivalent edge to attach to if none of the taxa in attachment_edge_taxa_set have been added to rec_tree yet
        So if taxa_set_intersect is null set move to parent of attachment edge until union is not null set
    """
    if not edge.tail_node:
        print("Error finding attachment edge: edge has no parent/tail")
    attachment_edge_taxa_set = set([lf.taxon.label for lf in edge.tail_node.leaf_iter()])
    taxa_set_intersection = attachment_edge_taxa_set & rectree_taxa
    while not taxa_set_intersection: # while intersect is null set
        edge = edge.tail_node.edge # get parent edge
        attachment_edge_taxa_set = set([lf.taxon.label for lf in edge.tail_node.leaf_iter()])
        taxa_set_intersection = attachment_edge_taxa_set & rectree_taxa
    for edge in rec_tree.postorder_edge_iter():
        edge_taxa = set([lf.taxon.label for lf in edge.head_node.leaf_iter()])
        if not taxa_set_intersection.difference(edge_taxa): 
            break # if there is no difference
    attachment_edge = edge # edge subtree will be attached to in rec_tree
    #print([lf.taxon.label for lf in attachment_edge.head_node.leaf_iter()])
    return attachment_edge

def attach_subtree(rec_tree,sub_tree,attachment_tree,attachment_edge,midpoint=False):
    
    verbose = False
    
    min_length = 0.0
    
    "Create a new 'graft' node to attach sub_tree and sister of sub_tree"
    attachment_parent_node = attachment_edge.tail_node
    attachment_sister_node = attachment_edge.head_node
    deep_rooted = False
    if not attachment_parent_node:
        """"
            Grafting above root of rec tree such that graft node will be new root
            This can happen if cut one of the root's child edges
            This should be working now but not very well tested!!
        """
        
        if verbose:
            print("Deep rooting tree")
        
        rec_tree = add_deep_root(rec_tree) # reroot == True by default now
        deep_rooted = True
        attachment_parent_node = attachment_edge.tail_node
        attachment_sister_node = attachment_edge.head_node
    
    """
        Get temporal constraints on graft node height:
        Graft node must be below attrachment parent node
        But above the root node of the grafted sub_tree and sister_subtree
    """
    rec_tree.calc_node_ages(ultrametricity_precision=False)
    attachment_parent_height = attachment_parent_node.age
    max_height =  attachment_parent_height
    sister_subtree_height = attachment_sister_node.age
    sub_tree.calc_node_ages(ultrametricity_precision=False)
    subtree_root = get_root_node(sub_tree)
    subtree_height = subtree_root.age
    min_height = max(sister_subtree_height,subtree_height)
    
    if verbose:
        if attachment_parent_height < sister_subtree_height:
            print("WARNING: Parent height is below sister subtree height")
        if attachment_parent_height < subtree_height:
            print("WARNING: Parent height is below subtree height")
    
    #if attachment_parent_height < min_height:
        
        """
            I think this can happen if we attach a subtree (pruned from ref) to a position in alt
        """
        #label_fn = lambda nd: nd.taxon.label if nd.is_leaf() else str(f"{nd.age:0.2f}")
        #rec_tree.print_plot(show_internal_node_labels=True,node_label_compose_fn=label_fn)
        #sub_tree.print_plot(show_internal_node_labels=True,node_label_compose_fn=label_fn)
        #attachment_tree.calc_node_ages(ultrametricity_precision=False)
        #attachment_tree.print_plot(show_internal_node_labels=True,node_label_compose_fn=label_fn)
        #print("WARNING: Parent height is below sister or subtree height")

    "Add new graft node to attach sub_tree to"
    attachment_edge_length = attachment_sister_node.edge_length
    graft_node = attachment_parent_node.new_child()

    "Extract sister subtree descending from attachment edge and prune it from rec_tree"
    
    "New way - does not remove dummy 'new_child' node we've grafted above"
    #sister_subtree = rec_tree.extract_tree_with_taxa(taxa=set([lf.taxon for lf in attachment_sister_node.leaf_iter()]))
    #print()
    
    "Old way to extract"
    for node in rec_tree.preorder_node_iter():
        node.remove = False
    for node in attachment_sister_node.preorder_iter():
        node.remove = True
    node_filter_fn = lambda nd: nd.remove
    sister_subtree = rec_tree.extract_tree(node_filter_fn=node_filter_fn)
    rec_tree.prune_subtree(attachment_sister_node, update_bipartitions=False, suppress_unifurcations=True)

    "Get and set length of graft edge"
    if midpoint:
        graft_node.edge.length = attachment_edge_length / 2.0
    else:
        subtree_taxon = sub_tree.leaf_nodes()[0].taxon.label # get one leaf in subtree
        sister_subtree_taxon = sister_subtree.leaf_nodes()[0].taxon.label # get one leaf in sister subtree
        attachment_tree.calc_node_ages(ultrametricity_precision=False) # moved above
        mrca = attachment_tree.mrca(taxon_labels=[subtree_taxon,sister_subtree_taxon]) #Should this be tree specific (rec/alt?)
        graft_node_age = mrca.age
        "Check constraints on graft node height/age"
        if graft_node_age < min_height or graft_node_age > max_height:
            graft_node_age = min_height + (max_height - min_height)/2.0 # center between max and min
        graft_node.edge.length = attachment_parent_height - graft_node_age #mrca.edge_length

    "Reattach sister subtree to graft node"
    sister_subtree_root = get_root_node(sister_subtree)
    if midpoint:
        sister_subtree_root.edge.length = attachment_edge_length / 2.0
    else:
        
        """
            sister_subtree_root.age resets to old root age when we deep root
        """
        
        "Edge length is difference between mrca age and height of sister_subtree"
        sister_subtree_root_length = graft_node_age - sister_subtree_height #sister_subtree_root.age
        if sister_subtree_root_length >= 0.0:
            sister_subtree_root.edge.length = sister_subtree_root_length #attachment_edge_length - mrca.edge_length
        else:
            if verbose:
                print('WARNING: Sister subtree edge length is less than zero!!')
            sister_subtree_root.edge.length = min_length #attachment_edge_length - mrca.edge_length
    graft_node.add_child(sister_subtree_root)
    
    "Attach sub_tree to graft node"
    subtree_root = get_root_node(sub_tree)
    if midpoint:
        subtree_root.edge.length = attachment_edge_length / 2.0
    else:
        
        "Edge length is difference between mrca age and height of subtree"
        subtree_root_length = graft_node_age - subtree_height #subtree_root.age
        if subtree_root_length >= 0.0:
            subtree_root.edge.length = subtree_root_length #attachment_edge_length - mrca.edge_length
        else:
            if verbose:
                print('WARNING: Subtree edge length is less than zero!!')
            subtree_root.edge.length = min_length #attachment_edge_length - mrca.edge_length
    graft_node.add_child(subtree_root)
    
    if deep_rooted:
        
        rec_tree = remove_deep_root(rec_tree)
        
        """
            Don't think we need to reroot now that we reroot when we add deep root above"
        """
        
        "We need to reroot but following approach not working?"
        #mrca = rec_tree.mrca(taxon_labels=[lf.taxon.label for lf in rec_tree.leaf_node_iter()])
        #rec_tree.reroot_at_edge(attachment_edge, update_bipartitions=False) # get_root_edge(rec_tree)
        
        "Rerooting on midpoint since ML trees are rooted on midpoint anyways"
        #rec_tree.reroot_at_midpoint()
        #rec_tree.print_plot()
        #print()
        
    for edge in rec_tree.postorder_edge_iter():
        if edge.length:
            if edge.length < 0.0:
                edge.length = min_length
                if verbose:
                    print("Negative branch length in reconciled tree")
            
    if not rec_tree.is_rooted:
        print("Reconciled tree has lost rooting")   

    return rec_tree

"""
    Reconcile node heights/ages in rec tree based on heights in alt and ref
"""
def reconcile_heights(rec_tree,ref,alt,seq_file=None,prior_ratio = 1.0):
    
    "Get dictionary of sequence ids : seq records"
    if seq_file:
        from Bio import SeqIO
        my_records = list(SeqIO.parse(seq_file, "fasta"))
        seq_dict = {record.id:record for record in my_records}
    
    "Calc node ages"
    rec_tree.calc_node_ages(ultrametricity_precision=False)
    ref.calc_node_ages(ultrametricity_precision=False)
    alt.calc_node_ages(ultrametricity_precision=False)
    
    "Encode bipartitions and bipart dicts"
    rec_tree.encode_bipartitions()  # need to encode bipartitions before can access them
    ref.encode_bipartitions()    
    alt.encode_bipartitions()
    
    ref_bipartition_dict = ref.split_bitmask_edge_map
    alt_bipartition_dict = alt.split_bitmask_edge_map
    
    for node in rec_tree.postorder_internal_node_iter():
        
        "Get equivalent edge in ref and alt"
        edge = node.edge
        ref_edge = ref_bipartition_dict.get(edge.split_bitmask,None)
        alt_edge = alt_bipartition_dict.get(edge.split_bitmask,None)
        
        "Get child node heights"
        child_heights = [nd.age for nd in node.child_node_iter()]
        
        "Set new height to current height"
        new_height = node.age
        
        if ref_edge and alt_edge:
            
            "Edge is in both alt and ref"
            #print("Edge is present in alt and ref")
            
            ref_height = ref_edge.head_node.age
            alt_height = alt_edge.head_node.age
            
            if ref_height == alt_height:
                continue # continue to next node since heights agree
            
            "Check constraints set by children height"
            min_height = max(child_heights)
            if ref_height > min_height and alt_height > min_height:
                
                "Need to choose among node height in ref and alt"
                
                """
                    If extracting a subtree to compute likelihood
                    Would work except RAxML won't accept trees with only two taxa
                """
                #subtree = rec_tree.extract_tree_with_taxa(taxa=set([lf.taxon for lf in node.leaf_iter()]))
                #ref_subtree = subtree.clone(depth=2)
                #parent = get_root_node(ref_subtree)
                
                "Set child edge lengths based on heights in ref"
                ref_clone = rec_tree.clone(depth=2)
                ref_clone.encode_bipartitions()
                ref_clone_bipartition_dict = ref_clone.split_bitmask_edge_map
                ref_clone_edge = ref_clone_bipartition_dict.get(edge.split_bitmask,None)
                parent = ref_clone_edge.head_node
                for idx,child in enumerate(parent.child_node_iter()):
                    child.edge.length = ref_height - child_heights[idx] #child.age
                    
                "Set child edge lengths based on heights in alt"
                alt_clone = rec_tree.clone(depth=2)
                alt_clone.encode_bipartitions()
                alt_clone_bipartition_dict = alt_clone.split_bitmask_edge_map
                alt_clone_edge = alt_clone_bipartition_dict.get(edge.split_bitmask,None)
                parent = alt_clone_edge.head_node
                for idx,child in enumerate(parent.child_node_iter()):
                    child.edge.length = alt_height - child_heights[idx] #child.age
                    
                "Just for debugging"
                #age_label_fn = lambda nd: nd.taxon.label if nd.is_leaf() else str(f"{nd.age:0.2f}")
                #ref_clone.calc_node_ages(ultrametricity_precision=False)
                #ref_clone.print_plot(plot_metric='age',show_internal_node_labels=True,node_label_compose_fn=age_label_fn)
                #alt_clone.calc_node_ages(ultrametricity_precision=False)
                #alt_clone.print_plot(plot_metric='age',show_internal_node_labels=True,node_label_compose_fn=age_label_fn)
                
                ref_tree_file = 'temp_ref.tre'
                ref_clone.write(path=ref_tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
            
                alt_tree_file = 'temp_alt.tre'
                alt_clone.write(path=alt_tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
            
                "Get fasta seq file for taxa currently in rec_tree"
                #temp_seq_file = 'temp_seqs.fasta'
                #temp_records = [seq_dict[nd.taxon.label] for nd in subtree.leaf_node_iter()]
                #SeqIO.write(temp_records, temp_seq_file, "fasta")
                temp_seq_file = seq_file
            
                alt_logL = RAxML.get_tree_likelihood(alt_tree_file,temp_seq_file)
                ref_logL = RAxML.get_tree_likelihood(ref_tree_file,temp_seq_file)
            
                like_ratio = math.exp(alt_logL - ref_logL)
                ratio = like_ratio * prior_ratio
            
                "New way: randomly choose based on like ratio and prior"
                if ratio > random.random():
                    new_height = alt_height
                else:
                    new_height = ref_height 
                
            elif ref_height > min_height:
                
                new_height = ref_height 
                
            elif alt_height > min_height:
                
                new_height = alt_height 
                
            else:
                print("WARNING: Neither ref or alt node height is valid")
            
        elif ref_edge:
            #print("Edge is only present in ref")
            new_height = ref_edge.head_node.age
        elif alt_edge:
            #print("Edge is only present in alt") 
            new_height = alt_edge.head_node.age
        else:
            print("Special case: edge is NOT in alt or ref")        
        
        "Set child edge lengths and recompute heights(?)"
        for idx,child in enumerate(node.child_node_iter()):
            child.edge.length = new_height - child_heights[idx] #child.age
        rec_tree.calc_node_ages(ultrametricity_precision=False)
        
    return rec_tree

"""
    Reconcile node heights for concordant nodes across tree path using the "lock and chain" method
    All concordant nodes in neighboring local trees will be assigned same height
    Added (optional) min branch length threshold so no branches have zero length
"""
def reconcile_linked_heights(tree_path, min_branch_length = 0.01, verbose=False):
    
    path_length = len(tree_path)
    
    bipartition_maps = []
    for tree in tree_path:
        tree.calc_node_ages(ultrametricity_precision=False)
        tree.encode_bipartitions() # need to encode bipartitions before we can access them
        bipartition_maps.append(tree.split_bitmask_edge_map) # create dict the maps edges to edge (split) bitmasks
    
    """
        Set state of all nodes state as unlocked
        Once locked a nodes age cannot be reset
        This prevents from repeatedly updating the same nodes age
    """
    for tree_idx, tree in enumerate(tree_path):
        for node in tree.postorder_internal_node_iter():
            node.locked = False
    
    for tree_idx, tree in enumerate(tree_path):
        
        if verbose:
            print("Starting reconciliation on tree # " + str(tree_idx))
        
        for node in tree.postorder_internal_node_iter():
            
            if not node.locked:
            
                "Find equivalent edges in adjacent trees until there is no such equivalent edge"
                edge = node.edge
                linked_trees = [tree] # list of linked trees with equivalent edge
                linked_heights = [node.age]
                linked_edges = [edge]
                min_constraint = max([nd.age for nd in node.child_node_iter()])
                linked_min_constraints = [min_constraint]
                for idx in range(tree_idx+1,path_length):
                    edge = bipartition_maps[idx].get(edge.split_bitmask,None)
                    if edge:
                        linked_trees.append(tree_path[idx]) #(idx)
                        linked_heights.append(edge.head_node.age)
                        linked_edges.append(edge)
                        min_constraint = max([nd.age for nd in edge.head_node.child_node_iter()])
                        linked_min_constraints.append(min_constraint)
                    else:
                        break
        
                """
                    Set new node height/age to median of linked hights
                    This is just a shortcut hack for now 
                    We should find the height that maximizes the likelihood of the sequence data across the linked blocks
                """
                new_height = np.median(linked_heights)
                min_constraint = max(linked_min_constraints) + min_branch_length # added so node has to be above closest child by min_branch_length
                if new_height < min_constraint:
                    new_height = min_constraint
                
                "Reset edge lengths in all linked trees"
                for edge_idx, edge in enumerate(linked_edges):
                    parent = edge.head_node
                    parent.locked = True
                    for child in parent.child_node_iter():
                        new_edge_length = new_height - child.age
                        if new_edge_length < 0:
                            print("WARNING: Child edge length negative!!")
                        child.edge.length = new_edge_length
                    
                    "Recompute node ages here to reflect to edge lengths"
                    linked_trees[edge_idx].calc_node_ages(ultrametricity_precision=False)

    return tree_path

"""
Reconcile a pair of trees (ref and alt) through their max agreement forest (maf)
"""
def reconcile_trees(ref,alt,maf,seq_file=None,prior_ratio = 1.0,midpoint=True, plot=False,deep_copy=True):
    
    "Get dictionary of sequence ids : seq records"
    if seq_file:
        from Bio import SeqIO
        my_records = list(SeqIO.parse(seq_file, "fasta"))
        seq_dict = {record.id:record for record in my_records}
    
    rec_tree = maf.pop() # seed rec_tree with last connected component in maf
    if deep_copy:
        rec_tree = rec_tree.clone(depth=2)
    
    for sub_tree in reversed(maf):
    
        "Get taxa set in subtree and rectree we are attaching"
        subtree_taxa = set([lf.taxon.label for lf in sub_tree.leaf_node_iter()])
        rectree_taxa = set([lf.taxon.label for lf in rec_tree.leaf_node_iter()])
            
        "Algorithm bifurcates here: find attachment edge (in rec_tree) for both alt and ref trees"
        attachment_edge_alt = find_attachment_edge(rec_tree,alt,subtree_taxa,rectree_taxa)
        rec_tree_clone = rec_tree.clone(depth=2) # I think cloning rec_tree here again is the problem b/c attachment_edge_ref no longer points to ojbect in cloned tree
        attachment_edge_ref = find_attachment_edge(rec_tree_clone,ref,subtree_taxa,rectree_taxa)
         
        """
        Attach sub_tree to rec_tree by adding a new "graft" node along attachment edge        
        """
        sub_tree_clone = sub_tree.clone(depth=2) #Should we also deep clone sub_tree?
        if deep_copy:
            sub_tree_2 = sub_tree.clone(depth=2)
        else:
            sub_tree_2 = sub_tree
        
        #print("Attaching subtree to ref position")
        rec_tree_ref = attach_subtree(rec_tree_clone,sub_tree_clone,ref,attachment_edge_ref,midpoint=midpoint)
        
        #print("Attaching subtree to alt position")
        rec_tree_alt = attach_subtree(rec_tree,sub_tree_2,alt,attachment_edge_alt,midpoint=midpoint) # rec_tree_ref.clone(depth=2)
        
        if plot:
            rec_tree_alt.print_plot()
            rec_tree_ref.print_plot()
            print()
            
        if rec_tree_alt.__len__() != rec_tree_ref.__len__():
            print("Rec trees of unequal size found!!")
        
        "Compare likelihood of sequence data under rec_tree_alt and rec_tree_ref"
        if seq_file:
            
            alt_tree_file = 'temp_alt.tre'
            rec_tree_alt.write(path=alt_tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
            
            "Get fasta seq file for taxa currently in rec_tree"
            temp_seq_file = 'temp_seqs.fasta'
            temp_records = [seq_dict[nd.taxon.label] for nd in rec_tree_alt.leaf_node_iter()]
            SeqIO.write(temp_records, temp_seq_file, "fasta")
            
            ref_tree_file = 'temp_ref.tre'
            rec_tree_ref.write(path=ref_tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
            
            alt_logL = RAxML.get_tree_likelihood(alt_tree_file,temp_seq_file)
            ref_logL = RAxML.get_tree_likelihood(ref_tree_file,temp_seq_file)
            
            like_ratio = math.exp(alt_logL - ref_logL)
            ratio = like_ratio * prior_ratio
            
            "New way: randomly choose based on like ratio and prior"
            if ratio > random.random():
                rec_tree = rec_tree_alt
            else:
                rec_tree = rec_tree_ref
            
        else:

            "Randomly decide whether rec_tree_alt or rec_tree_ref becomes new rec_tree"           
            ratio = random.random() * prior_ratio
            if ratio > random.random():
                print("Picked alt tree")
                rec_tree = rec_tree_alt 
            else:
                print("Picked ref tree")
                rec_tree = rec_tree_ref

                
    return rec_tree

"""
Reconcile local tree (alt) with global (ref) tree through their max agreement forest (maf)
Differs from reconcile_trees by allowing site likelihoods outside of local region to be discounted
"""
def reconcile_local_tree(ref,alt,maf,seq_file,start_pos,end_pos,prior_gamma=0.0,midpoint=True, plot=False,deep_copy=True):
    
    "Get dictionary of sequence ids : seq records"
    from Bio import SeqIO
    my_records = list(SeqIO.parse(seq_file, "fasta"))
    seq_dict = {record.id:record for record in my_records}
    total_length = len(seq_dict[next(iter(seq_dict))].seq)
    
    rec_tree = maf.pop() # seed rec_tree with last connected component in maf
    if deep_copy:
        rec_tree = rec_tree.clone(depth=2)
    
    for sub_tree in reversed(maf):
    
        "Get taxa set in subtree and rectree we are attaching"
        subtree_taxa = set([lf.taxon.label for lf in sub_tree.leaf_node_iter()])
        rectree_taxa = set([lf.taxon.label for lf in rec_tree.leaf_node_iter()])
            
        "Algorithm bifurcates here: find attachment edge (in rec_tree) for both alt and ref trees"
        attachment_edge_alt = find_attachment_edge(rec_tree,alt,subtree_taxa,rectree_taxa)
        rec_tree_clone = rec_tree.clone(depth=2) # I think cloning rec_tree here again is the problem b/c attachment_edge_ref no longer points to ojbect in cloned tree
        attachment_edge_ref = find_attachment_edge(rec_tree_clone,ref,subtree_taxa,rectree_taxa)
         
        """
        Attach sub_tree to rec_tree by adding a new "graft" node along attachment edge        
        """
        sub_tree_clone = sub_tree.clone(depth=2) #Should we also deep clone sub_tree?
        if deep_copy:
            sub_tree_2 = sub_tree.clone(depth=2)
        else:
            sub_tree_2 = sub_tree
        
        #print("Attaching subtree to ref position")
        rec_tree_ref = attach_subtree(rec_tree_clone,sub_tree_clone,ref,attachment_edge_ref,midpoint=midpoint)
        
        #print("Attaching subtree to alt position")
        rec_tree_alt = attach_subtree(rec_tree,sub_tree_2,alt,attachment_edge_alt,midpoint=midpoint) # rec_tree_ref.clone(depth=2)
        
        if plot:
            rec_tree_alt.print_plot()
            rec_tree_ref.print_plot()
            print()
            
        if rec_tree_alt.__len__() != rec_tree_ref.__len__():
            print("Rec trees of unequal size found!!")
        
        "Compare likelihood of sequence data under rec_tree_alt and rec_tree_ref"
        if rec_tree_alt.__len__() > 3: # min tree size for RAxML is 4
            
            alt_tree_file = 'temp_alt.tre'
            rec_tree_alt.write(path=alt_tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
            
            "Get fasta seq file for taxa currently in rec_tree"
            temp_seq_file = 'temp_seqs.fasta'
            temp_records = [seq_dict[nd.taxon.label] for nd in rec_tree_alt.leaf_node_iter()]
            SeqIO.write(temp_records, temp_seq_file, "fasta")
            
            ref_tree_file = 'temp_ref.tre'
            rec_tree_ref.write(path=ref_tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
            
            "Get site likelihoods (for all sites) given both alt and ref tree"
            alt_site_likes = RAxML.get_site_likelihoods(alt_tree_file,temp_seq_file,verbose=False)
            ref_site_likes = RAxML.get_site_likelihoods(ref_tree_file,temp_seq_file,verbose=False)
            
            alt_local_like = np.sum(alt_site_likes[start_pos:end_pos])  
            ref_local_like = np.sum(ref_site_likes[start_pos:end_pos])
            
            "For discounting like contribution from sites further away"
            left_dists = np.abs(np.arange(0,start_pos) - start_pos) # distances to left of start_pos
            right_dists = np.abs(np.arange(end_pos,total_length) - end_pos) # distances to left of start_pos

            left_alt_site_likes = alt_site_likes[:start_pos] * np.exp(-prior_gamma*left_dists)
            right_alt_site_likes = alt_site_likes[end_pos:] * np.exp(-prior_gamma*right_dists)
            left_ref_site_likes = ref_site_likes[:start_pos] * np.exp(-prior_gamma*left_dists)
            right_ref_site_likes = ref_site_likes[end_pos:] * np.exp(-prior_gamma*right_dists)
            
            alt_global_like = np.sum(left_alt_site_likes) + np.sum(right_alt_site_likes)  
            ref_global_like = np.sum(left_ref_site_likes) + np.sum(right_ref_site_likes) 
            
            "Without discounting"
            #alt_global_like = np.sum(alt_site_likes[:start_pos]) + np.sum(alt_site_likes[end_pos:])  
            #ref_global_like = np.sum(ref_site_likes[:start_pos]) + np.sum(alt_site_likes[end_pos:]) 
            
            like_ratio = math.exp(alt_local_like - ref_local_like)
            prior_ratio = math.exp(alt_global_like - ref_global_like)
            ratio = like_ratio * prior_ratio
            
            "New way: randomly choose based on like ratio and prior"
            if ratio > random.random():
                rec_tree = rec_tree_alt
            else:
                rec_tree = rec_tree_ref
            
        else:

            "Randomly decide whether rec_tree_alt or rec_tree_ref becomes new rec_tree"           
            ratio = random.random() # * prior_ratio
            if ratio > random.random():
                print("Picked alt tree")
                rec_tree = rec_tree_alt 
            else:
                print("Picked ref tree")
                rec_tree = rec_tree_ref

                
    return rec_tree

"""
Search for reconciled local trees using a branch and bound algorithm
"""
def bb_regraft(ref,alt,maf,seq_file,start_pos,end_pos,previous_trees,lower_bound_ratio=0.1,prior_gamma=0.0,midpoint=True, plot=False,deep_copy=True):
    
    class Node:
        def __init__(self, parent=None, tree=None, index=-1, like=0.0, source=None):
            self.parent = parent
            self.tree = tree
            self.index = index
            self.like = like
            self.source = source
    
    "Added recomb penalty so there would be a cost to regrafting to ALT position"
    recomb_penalty = 1.0 #0.001
    
    max_sample_size = 10 # max number of reconciled trees to sample
    
    "Get dictionary of sequence ids : seq records"
    "Could just pass seq_dict so we don't need to repeatedly import alignment"
    my_records = list(SeqIO.parse(seq_file, "fasta"))
    
    "Temp fix added for potyviruses where taxa have underscores in name incompatible with dendropy taxa names"
    #seq_dict = {record.id:record for record in my_records}
    seq_dict = {record.id.replace('_',' '):record for record in my_records}
    
    total_length = len(seq_dict[next(iter(seq_dict))].seq)
    
    "For discounting like contribution from sites further away"
    left_dists = np.abs(np.arange(0,start_pos) - start_pos) # distances to left of start_pos
    right_dists = np.abs(np.arange(end_pos,total_length) - end_pos) # distances to right of start_pos
    
    "Reverse order of maf subtrees so we start with largest connected component"
    maf = list(reversed(maf))
    
    verbose = False
    less_verbose = True
    if verbose or less_verbose:
        print("Starting regrafting")
        print("Subtrees in MAF: " + str(len(maf)))
    
    "Create root node"
    root_tree = maf[0].clone(depth=2)
    root = Node(parent = None, tree = root_tree, index = 0)
    
    queue = [] # queue of "open" nodes we still need to process
    queue.append(root)
    
    sampled_nodes = [] # sampled nodes represent regrafted (full) trees
    
    nodes_visited = 0
    ref_count = 0
    alt_count = 0
    
    while queue:
        
        parent = queue.pop()
        
        maf_index = parent.index+1
        
        nodes_visited += 1
        
        if verbose or less_verbose:
            if nodes_visited % 10 == 0:
                print("Processing next search node : " + str(nodes_visited))
        
        if maf_index == len(maf): # this is a full tree
        
            if parent.tree.__len__() != ref.__len__():
                print("Trees of unequal size found!!")
            parent.source = 'Reconciled'
            sampled_nodes.append(parent)
            
            if verbose:
                print("Reached tip node in search tree. Output tree #: " + str(len(sampled_nodes)))
        
        else: 
        
            "Node contains patial tree"
            sub_tree = maf[maf_index]
            rec_tree = parent.tree # should we clone rec_tree here?
            
            "Add children of parent"
            
            "Get taxa set in subtree and rectree we are attaching"
            subtree_taxa = set([lf.taxon.label for lf in sub_tree.leaf_node_iter()])
            rectree_taxa = set([lf.taxon.label for lf in rec_tree.leaf_node_iter()])
            
            "Algorithm bifurcates here: find attachment edge (in rec_tree) for both alt and ref trees"
            if verbose:
                print("Finding attachment edges")
            attachment_edge_alt = find_attachment_edge(rec_tree,alt,subtree_taxa,rectree_taxa)
            rec_tree_clone = rec_tree.clone(depth=2)
            attachment_edge_ref = find_attachment_edge(rec_tree_clone,ref,subtree_taxa,rectree_taxa)
            
            """
            Attach sub_tree to rec_tree by adding a new "graft" node along attachment edge        
            """
            if verbose:
                print("Attaching subtrees")
            sub_tree_clone = sub_tree.clone(depth=2) #Should we also deep clone sub_tree?
            if deep_copy:
                sub_tree_2 = sub_tree.clone(depth=2)
            else:
                sub_tree_2 = sub_tree
            rec_tree_ref = attach_subtree(rec_tree_clone,sub_tree_clone,ref,attachment_edge_ref,midpoint=midpoint)
            rec_tree_alt = attach_subtree(rec_tree,sub_tree_2,alt,attachment_edge_alt,midpoint=midpoint) # rec_tree_ref.clone(depth=2)
            
            if rec_tree_alt.__len__() > 3: # min tree size for RAxML is 4
                
            
                if verbose:
                    print("Computing site likelihoods")
            
                alt_tree_file = 'temp_alt.tre'
                rec_tree_alt.write(path=alt_tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
                
                "Get fasta seq file for taxa currently in rec_tree"
                temp_seq_file = 'temp_seqs.fasta'
                temp_records = [seq_dict[nd.taxon.label] for nd in rec_tree_alt.leaf_node_iter()]
                SeqIO.write(temp_records, temp_seq_file, "fasta")
                
                """
                    Check sub_alignment in temp_records for to make sure there are no sites with all undetermined values ('-')
                    Remove and record position of all sites with undetermined values
                    
                """
                # tic = time.perf_counter()
                # align = AlignIO.read(temp_seq_file, "fasta")
                # n_sites = align.get_alignment_length()
                # n_samples = len(align[:,0])
                # sites_removed = []
                # for i in reversed(range(n_sites)): # iterate through list in reverse order so site indexes don't change as we remove sites
                #     if align[:,i].count('-') == n_samples:
                #         sites_removed.append(i)
                #         align = align[:,:i] + align[:,i+1:] # take everything before and after site i
                # if sites_removed: # if sites have been removed
                #     AlignIO.write(align, temp_seq_file, "fasta")
                # toc = time.perf_counter()
                # elapsed = toc - tic
                # print(f"Elapsed time checking sub-alignment: {elapsed:0.4f} seconds")
                
                ref_tree_file = 'temp_ref.tre'
                rec_tree_ref.write(path=ref_tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
                
                "Get site likelihoods (for all sites) given both alt and ref tree"
                tic = time.perf_counter()
                #alt_site_likes = RAxML.get_site_likelihoods(alt_tree_file,temp_seq_file,verbose=False)
                #ref_site_likes = RAxML.get_site_likelihoods(ref_tree_file,temp_seq_file,verbose=False)
                alt_site_likes = RAxML.get_site_likelihoods_ng(alt_tree_file,temp_seq_file,verbose=False)
                ref_site_likes = RAxML.get_site_likelihoods_ng(ref_tree_file,temp_seq_file,verbose=False)
                toc = time.perf_counter()
                elapsed = toc - tic
                if verbose:
                    print(f"Elapsed time for site likelihoods: {elapsed:0.4f} seconds")
                
                "Add in dummy site likelihoods for sites removed"
                # for site_idx in reversed(sites_removed): # in original order so site indexes don't change
                #     alt_site_likes = np.insert(alt_site_likes,site_idx,0.0)
                #     ref_site_likes = np.insert(ref_site_likes,site_idx,0.0) 
                
                alt_local_like = np.sum(alt_site_likes[start_pos:end_pos])  
                ref_local_like = np.sum(ref_site_likes[start_pos:end_pos])
    
                left_alt_site_likes = alt_site_likes[:start_pos] * np.exp(-prior_gamma*left_dists)
                right_alt_site_likes = alt_site_likes[end_pos:] * np.exp(-prior_gamma*right_dists)
                left_ref_site_likes = ref_site_likes[:start_pos] * np.exp(-prior_gamma*left_dists)
                right_ref_site_likes = ref_site_likes[end_pos:] * np.exp(-prior_gamma*right_dists)
                
                alt_global_like = np.sum(left_alt_site_likes) + np.sum(right_alt_site_likes)  
                ref_global_like = np.sum(left_ref_site_likes) + np.sum(right_ref_site_likes) 
            
            else:
                
                alt_local_like = 0 
                ref_local_like = 0
                alt_global_like = 0 
                ref_global_like = 0
    
            alt_like = alt_local_like + alt_global_like + np.log(recomb_penalty)
            ref_like = ref_local_like + ref_global_like
            
            if verbose:
                print("Updating search tree")
                print("Alt / ref likelihood = " + f'{alt_like:.2f}' + ' / ' + f'{ref_like:.2f}')
            
            if ref_like > alt_like:
                child = Node(parent = parent, tree = rec_tree_ref, index = maf_index, like = ref_like)
                queue.append(child)
                ref_count += 1
                ratio = math.exp(alt_like - ref_like)
                if ratio > lower_bound_ratio:
                    child = Node(parent = parent, tree = rec_tree_alt, index = maf_index, like = alt_like)
                    queue.append(child)
                    alt_count += 1
                    if verbose:
                        print("Added lower like node to search tree. Like ratio = " + f'{ratio:.2f}')
            else:
                child = Node(parent = parent, tree = rec_tree_alt, index = maf_index, like = alt_like)
                queue.append(child)
                alt_count += 1
                ratio = math.exp(ref_like - alt_like)
                if ratio > lower_bound_ratio:
                    child = Node(parent = parent, tree = rec_tree_ref, index = maf_index, like = ref_like)
                    queue.append(child)
                    ref_count += 1
                    if verbose:
                        print("Added lower like node to search tree. Like ratio = " + f'{ratio:.2f}')
    
    "Add sampled trees from previous interval"
    new_sample_count = len(sampled_nodes)
    #previous_trees = dendropy.TreeList()
    #previous_trees.append(ref)
    for tr in previous_trees:
        tree_file = 'temp_ref.tre'
        tr.write(path=tree_file,schema='newick',suppress_annotations=True,suppress_rooting=True)
        site_likes = RAxML.get_site_likelihoods_ng(tree_file,seq_file,verbose=False)
        local_like = np.sum(site_likes[start_pos:end_pos])  
        left_site_likes = site_likes[:start_pos] * np.exp(-prior_gamma*left_dists)
        right_site_likes = site_likes[end_pos:] * np.exp(-prior_gamma*right_dists)
        global_like = np.sum(left_site_likes) + np.sum(right_site_likes)
        tr_like = local_like + global_like
        sampled_nodes.append(Node(parent = None, tree = tr, index = 'Previous', like = tr_like, source = 'Previous')) # index 'Previous' is assigned just to let us know this was a previously sampled tree
    
    "Sample trees with highest overall likelihood"
    if len(sampled_nodes) > max_sample_size:
        sampled_nodes.sort(key=lambda x: x.like)
        sampled_nodes = sampled_nodes[-max_sample_size:] # take last x nodes sorted in ascending order

    sampled_sources = [s.source for s in sampled_nodes]

    "Count how many sampled trees are from previous interval"
    previous_count =  0
    for n in sampled_nodes:
        if n.index == 'Previous':
            previous_count += 1
    
    sampled_trees = dendropy.TreeList()
    sampled_trees.taxon_namespace = ref.taxon_namespace
    for nd in sampled_nodes:
        #nd_tree.taxon_namespace = taxa
        #nd_tree.reconstruct_taxon_namespace() #reindex_subcomponent_taxa()
        if deep_copy:
            sampled_trees.append(nd.tree.clone(depth=2)) # clone tree before putting in tree_array
        else:
            sampled_trees.append(nd.tree)
        
    "Append ML tree"
    sampled_trees.append(alt) # append ML tree for segment
    sampled_sources.append('ML')           
    
    if verbose or less_verbose:
        print(f"Newly sampled trees : {new_sample_count}" + "; Previously sampled: " + f"{previous_count}")
        print("Alt / ref reattachments = " + f'{alt_count}' + ' / ' + f'{ref_count}')
        #print(f"Region length = {end_pos - start_pos}")
    
    return sampled_trees, sampled_sources


"Simulate a tree series in ms prime"

if  __name__ == '__main__':
    
    #tree_file = 'temp_ref.tre'
    #seq_file = 'temp_seqs.fasta'
    #site_likes = get_site_likelihoods(tree_file,seq_file,verbose=False)

    sim = False
    topo_changes = 0
    if sim:
        breaks = 0
        while breaks < 4:
            ts = msprime.simulate(sample_size=6, Ne=100, length=1e4, recombination_rate=1e-7, record_full_arg=True)
            breaks = len(ts.breakpoints(as_array=True))
        
        newicks = []
        prev_tree = None
        for tr_num, tree in enumerate(ts.trees()):
            print("-" * 20)
            print("tree {}: interval = {}".format(tree.index, tree.interval))
            print(tree.draw(format="unicode"))
            
            "Test for discordance "
            if tr_num > 0:
                taxa = dendropy.TaxonNamespace()
                ref = dendropy.Tree.get(data=prev_tree, schema="newick", rooting="default-rooted", taxon_namespace=taxa)
                alt = dendropy.Tree.get(data=tree.newick(), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
                if test_discordance(ref,alt):
                    topo_changes += 1    
            
            newicks.append(tree.newick()) # leaf nodes are labelled with their numerical ID + 1
            with open("maf_2TopoChanges_test2_tree" + str(tr_num) + ".tre", "w") as text_file:
                print(tree.newick(), file=text_file)
                
            prev_tree = tree.newick()
        
        print(ts.tables.nodes)
        print()
        print(ts.tables.edges)
        print()
        print("Recombination breakpoints: " + str(breaks))
        print()
        print("Topological changes in tree sequence: " + str(topo_changes))
    
    ref_file = "maf_2TopoChanges_test1_treeA.tre"
    alt_file = "maf_2TopoChanges_test1_treeB.tre"
    
    taxa = dendropy.TaxonNamespace()
    ref = dendropy.Tree.get(file=open(ref_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
    alt = dendropy.Tree.get(file=open(alt_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
    
    print("Reference tree:")
    ref.print_plot()
    print("Alternate tree:")
    alt.print_plot()
    
    "Get maximum agreement forest"
    maf = get_maf_4cut(ref,alt,plot=False)
    plot_maf(maf)
    
    rec_tree = reconcile_trees(ref,alt,maf,plot=False)
    
    rec_tree.write(
            path='maf_2TopoChanges_test1_reconciled.tre',
            schema='newick',
            suppress_annotations=True)