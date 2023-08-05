"""
Created on Fri Aug  7 16:21:14 2020

Old defunct versions of the MAF algorithm (all flawed)

@author: david
"""

def get_discordant_subtrees(ref,alt):
    
    """
        Get all discordant subtrees - never finished implementing
        Do a pre-order node traversal starting from root
        Check if node is discordant (a discordant node had discordant parent edge)
        Check if parent node is also discordant
        If parent node is discordant:
            don't need to do anything
        If parent node is concordant:
            then this is a new discordant subtree
            extract subtree using extract_subtree
            
    """
    
    for node in alt.preorder_node_iter():
        if not node.concordant:
            
            "Root does not have a parent_node so we do not catch case of discordant root"
            
            if node.parent_node.concordant:
                "Then this is a new discordant subtree"
                #subtree = node.extract_subtree()
                sub_taxa = [leaf.taxon for leaf in node.leaf_iter()]
                subtree = alt.extract_tree_with_taxa(sub_taxa)
                subtree.print_plot()
                print()

def choose_edge_cut(parent,ref_bitstring_dict):
    
    """
        Look back in tree to see which child edge we should cut
        Remove one child edge, if subtree defined by grandparent is concordant then take this node
        Another problem with this approach is if grandparent leafset is incompatible b/c cut taxa are included in reference bipartition
    """
    child_nodes = parent.child_nodes()
    grandparent = parent.parent_node
    
    grandparent_bitstring = grandparent.bipartition.leafset_as_bitstring()
    grandparent_bitarray = list(map(int, grandparent_bitstring))
    child0_bitstring = child_nodes[0].bipartition.leafset_as_bitstring()
    child0_bitarray = list(map(int, child0_bitstring))
    child1_bitstring = child_nodes[1].bipartition.leafset_as_bitstring()
    child1_bitarray = list(map(int, child1_bitstring))
    
    test_bitarray_child0 = np.array(grandparent_bitarray) - np.array(child0_bitarray)
    test_bitstring_child0 = str("".join(map(str, test_bitarray_child0)))
    test_edge_child0 = ref_bitstring_dict.get(test_bitstring_child0,None)
    
    test_bitarray_child1 = np.array(grandparent_bitarray) - np.array(child1_bitarray)
    test_bitstring_child1 = str("".join(map(str, test_bitarray_child1)))
    test_edge_child1 = ref_bitstring_dict.get(test_bitstring_child1,None)
    
    if test_edge_child0 and test_edge_child1:
        "Removal of either child gives concordant grandparent node"
        if sum(child0_bitarray) < sum(child1_bitarray):
            child = 0
        else:
            child = 1  
    else:
        if test_edge_child0: # if edge bistring exists then remove this node
            child = 0
        else:
            child = 1
            
    return child

"Defunct - replaced by get_maf_4cut"
def get_max_agreement_forest(ref,alt,plot=False):
    
    """
        This algorithm tries to find true MAF by testing all possible edges to cut at each discordance level
        And then greedily making the cut that minimizes discordance in the pruned trees
        
        Should also find discordant edges in REF tree
    """
    
    ref.encode_bipartitions() # need to encode bipartitions before can access them    
    alt.encode_bipartitions()
    
    ref_bipartition_dict = ref.split_bitmask_edge_map #dictionary mapping split bitmasks (integers) to their corresponding edges through the Tree.split_bitmask_edge_map attribute
    #for key, value in ref_bipartition_dict.items(): print(key, value)
    
    trees_discordant = update_concordance(alt,ref_bipartition_dict)
        
    "The MAF algorithm"
    forest = [] # subtrees in MAF
    counter = 0
    while trees_discordant:
        
        "Find ALL discordant edges at this level"
        edge_list = []
        for edge in alt.postorder_edge_iter():
            if not edge.concordant:    
                "Test if edge has discordant descendents"
                node = edge.head_node
                dflag = False
                for nd in node.preorder_iter():
                    if nd is not node and not nd.edge.concordant:
                        dflag = True    
                        break
                if dflag:
                    break
                else:
                    edge_list.append(edge)
        
        "Get child edges to cut"
        edge_cut_list = []
        for edge in edge_list:
            parent = edge.head_node
            for ch_edge in parent.child_edge_iter():
                edge_cut_list.append(ch_edge)
        
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
            bitmask = edge.leafset_bitmask
            alt_cut_edge = alt_cut_bipartition_dict.get(bitmask,None)
            ref_cut_edge = ref_cut_bipartition_dict.get(bitmask,None)
            
            "Make sure we're getting the correct edges"
            #edge_taxa = set([lf.taxon.label for lf in edge.head_node.leaf_iter()])
            #alt_cut_edge_taxa = set([lf.taxon.label for lf in alt_cut_edge.head_node.leaf_iter()])
            #ref_cut_edge_taxa = set([lf.taxon.label for lf in ref_cut_edge.head_node.leaf_iter()])

            "Extract subtree from alt and place in subtree forest"
            child_nd = alt_cut_edge.head_node
            for node in alt_cut.preorder_node_iter():
                node.remove = False
            for node in child_nd.preorder_iter():
                node.remove = True
            node_filter_fn = lambda nd: nd.remove
            component = alt_cut.extract_tree(node_filter_fn=node_filter_fn)
            components.append(component)
            #print("Subtree size = ", len(component.nodes()))
        
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
     
    forest.append(alt) # append what's left of alt (should at least be a rooted tree with two edges)
    return forest

"Defunct - replaced by get_maf_4cut"              
def get_agreement_forest(ref,alt,plot=False):
    
    """
        This algorithm returns an agreement forest but this is not guarenteed to be maximum agreement forest
        b/c we randomly choose which edges to cut which may result in the AF containing unnecessary components
    """
    
    ref.encode_bipartitions() # need to encode bipartitions before can access them    
    alt.encode_bipartitions()
    
    #ref_bitstring_dict = ref.bipartition_edge_map #dictionary mapping leafset bitstrings instances to their corresponding edges
    ref_bitstring_dict = get_bitstring_dict(ref)
    #for key, value in ref_bitstring_dict.items(): print(key, value)
    ref_bipartition_dict = ref.split_bitmask_edge_map #dictionary mapping split bitmasks (integers) to their corresponding edges through the Tree.split_bitmask_edge_map attribute
    #for key, value in ref_bipartition_dict.items(): print(key, value)
    
    trees_discordant = update_concordance(alt,ref_bipartition_dict)
        
    "The MAF algorithm"
    forest = [] # subtrees in MAF
    while trees_discordant:
        
        "Find first discordant edge"
        for edge in alt.postorder_edge_iter():
            if not edge.concordant: break
            
        parent = edge.head_node #first discordant sibling pair (edge) in t1
        child_nodes = parent.child_nodes() # can also iter over child_nodes
        child_edges = parent.child_edges()
        
        "Can extract some additional info about this bipartition"
        #split = edge.bipartition.leafset_as_bitstring()
        
        "Choose which child edge to cut"
        child = choose_edge_cut(parent,ref_bitstring_dict)

        "Extract subtree from alt and place in subtree forest"
        child_nd = child_nodes[child]
        for node in alt.preorder_node_iter():
            node.remove = False
        for node in child_nd.preorder_iter():
            node.remove = True
        node_filter_fn = lambda nd: nd.remove
        component = alt.extract_tree(node_filter_fn=node_filter_fn)
        forest.append(component)
        #print("Subtree size = ", len(component.nodes()))
        
        "Prune subtree from alt"
        #parent.remove_child(child_nd, suppress_unifurcations=False)
        alt.prune_subtree(child_nd, update_bipartitions=True, suppress_unifurcations=True)
        if plot:
            alt.print_plot()
        
        "Find and prune corresponding edge in ref tree"
        bitmask = child_edges[child].leafset_bitmask
        ref_edge = ref_bipartition_dict.get(bitmask,None)
        ref_child = ref_edge.head_node
        ref.prune_subtree(ref_child, update_bipartitions=True, suppress_unifurcations=True)
        if plot:
            ref.print_plot()

        """
            What do we need to do before next iter
            Update bipartitions - did this above
            Update ref bitstring and bipartition dictionaries
            Update concordance
        """            
        #ref_bitstring_dict = ref.bipartition_edge_map #dictionary mapping leafset bitstrings instances to their corresponding edges
        ref_bitstring_dict = get_bitstring_dict(ref)
        ref_bipartition_dict = ref.split_bitmask_edge_map
        trees_discordant = update_concordance(alt,ref_bipartition_dict)
     
    forest.append(alt) # append what's left of alt (should at least be a rooted tree with two edges)
    return forest


