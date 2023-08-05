#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 16:41:04 2020

TreeRandomizer - randomizes topology of input tree by random subtree prune regraft moves

To do:
    -Enforce temporal constraints on attaching subtrees to "younger" edges

@author: david
"""
import dendropy
import msprime
import random

def get_root_edge(tree):
    for edge in tree.preorder_edge_iter():
        root = edge
        break
    return root

def get_root_node(tree):
    for nd in tree.preorder_node_iter():
        root = nd
        break
    return root

def random_SPR(tree,exclude_root_children=False,plot=False):
    
    tr = tree.clone(depth=2) #Deep copy tree
    tr.calc_node_ages(ultrametricity_precision=False)
    edge_list = tr.edges()
    
    "Pick random edge for subtree to prune"
    root_edge = get_root_edge(tr)
    
    "Check if child edge of root are terminal branches - exclude them if they are"
    root_child_edges = root_edge.head_node.child_edges()
    forbidden = [root_edge]
    if exclude_root_children:
        forbidden.append(root_child_edges[0])
        forbidden.append(root_child_edges[1])
    else:
        if root_child_edges[0].head_node.is_leaf():
            forbidden.append(root_child_edges[1])
        if root_child_edges[1].head_node.is_leaf():
            forbidden.append(root_child_edges[0])
    
    cut_edge = random.choice(edge_list)
    while cut_edge in forbidden:
        print("Cut edge is root")
        cut_edge = random.choice(edge_list)
    subtree_node = cut_edge.head_node
    parent = cut_edge.tail_node
    child_edges = parent.child_edges()
    if child_edges[0] is cut_edge:
        sister_edge = child_edges[1]
    else:
        sister_edge = child_edges[0]
    
    "Prune subtree"
    for node in tr.preorder_node_iter():
        node.remove = False
    for node in subtree_node.preorder_iter():
        node.remove = True
    node_filter_fn = lambda nd: nd.remove
    subtree = tr.extract_tree(node_filter_fn=node_filter_fn)
    tr.prune_subtree(subtree_node, update_bipartitions=False, suppress_unifurcations=True)
    if plot:
        if len(subtree.nodes()) > 1:
            subtree.print_plot()
        else:
            print('---' + subtree.nodes()[0].taxon.label)
        tr.print_plot()
    
    "Pick random edge to regraft subtree"
    edge_list = tr.edges()
    root_edge = get_root_edge(tr)
    graft_edge = random.choice(edge_list)
    forbidden = [root_edge,sister_edge] # Graft edge cannot be root or sister to cut edge
    while graft_edge in forbidden:
        print("Attachment edge is the same or sister to cut edge")
        graft_edge = random.choice(edge_list)

    
    "Regraft subtree"
    "Create a new 'graft' node to attach sub_tree and sister of sub_tree"
    attachment_parent_node = graft_edge.tail_node
    "This should not happen, but just in case:"
    if not attachment_parent_node:
        parent_leaf_set = set([lf.taxon.label for lf in graft_edge.head_node.leaf_iter()])
        print(parent_leaf_set)
    attachment_sister_node = graft_edge.head_node
    attachment_edge_length = attachment_sister_node.edge_length
    graft_node = attachment_parent_node.new_child()
    
    """
        Picking graft node age as midpoint of attachment_edge_length is dangerous
        Need to make sure graft node height is above grafted subtree and sister height!!!
    """ 
    attachment_parent_height = attachment_parent_node.age
    subtree_height = subtree_node.age
    sister_subtree_height = attachment_sister_node.age
    max_height = attachment_parent_height
    min_height = max(sister_subtree_height,subtree_height)
    
    "Prune sister subtree descending from attachment edge"
    tr.prune_subtree(attachment_sister_node, update_bipartitions=False, suppress_unifurcations=True)
    
    "Get and set length of graft edge - currently using midpoint but could also use something else?"
    #graft_node.edge.length = attachment_edge_length / 2.0 # old way
    graft_node_age = min_height + (max_height - min_height)/2.0
    graft_node.edge.length = attachment_parent_height - graft_node_age
    
    "Reattach sister subtree to graft node"
    #attachment_sister_node.edge.length = attachment_edge_length / 2.0 # old way
    attachment_sister_node.edge.length = graft_node_age - sister_subtree_height
    graft_node.add_child(attachment_sister_node)
    
    "Edge length is difference between graft node age and height of subtree"
    #subtree_node.edge.length = attachment_edge_length / 2.0 # old way
    subtree_node.edge.length = graft_node_age - subtree_height
    graft_node.add_child(subtree_node)
        
    if plot:
        print("New SPR tree")
        tr.print_plot()
    
    return tr

if  __name__ == '__main__':

    "Simulate tree without recombination"
    sim = True
    if sim:
        ts = msprime.simulate(sample_size=6, Ne=100, length=1e4, recombination_rate=0, record_full_arg=True)
        tree = ts.first()
        print("-" * 20)
        print(tree.draw(format="unicode"))
        with open("maf_randomSPRs_refTree_test1.tre", "w") as text_file:
            print(tree.newick(), file=text_file)
    
    ref_file = "maf_randomSPRs_refTree_test1.tre"
    #alt_file = "maf_2TopoChanges_test1_treeB.tre"
    
    taxa = dendropy.TaxonNamespace()
    ref = dendropy.Tree.get(file=open(ref_file, 'r'), schema="newick", rooting="default-rooted", taxon_namespace=taxa)
    
    """
    Perform random SPR moves on tree
    """
    moves = 2 # number of SPR moves
    alt = ref
    for i in range(moves):
        print("SPR move = ", str(i))
        alt = random_SPR(alt,plot=True)
    
    print("Reference tree:")
    ref.print_plot()
    
    print("Alternate tree:")
    alt.print_plot()
    #alt.write(path='maf_randomSPRs_altTree_test1.tre',schema='newick',suppress_annotations=True)
    
    
