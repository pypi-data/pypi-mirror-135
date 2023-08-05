"""
Created on Tues Feb 25 2020

Plot sequential tanglegrams to visualize recombination among CoVs using baltic

@author: david
"""

import numpy as np
import balticmod as bt
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
#import requests
from io import StringIO as sio
from io import BytesIO as csio
import re

def convert2nexus(in_tree,out_tree):
    
    myTree=bt.loadNewick(in_tree, absoluteTime=False)
    myTree.traverse_tree() ## required to set heights
    myTree.treeStats() ## report stats about tree
    names = []
    for idx,k in enumerate(myTree.Objects): ## iterate over a flat list of branches
        if k.branchType=='leaf':
            curr_name = k.numName
            names.append(curr_name)
    
    date_str = '' #'_2020.00'
    
    # Write taxa names
    nex=open(out_tree,"w")
    nex.write("#NEXUS\n")
    nex.write("Begin taxa;\n")
    nex.write("\tDimensions ntax=" + str(len(names)) + ";\n")	
    nex.write("\t\tTaxlabels\n")
    for n in names:
        nex.write("\t\t\t" + n + date_str + "\n")    
    nex.write("\t\t\t;\n")
    nex.write("End;\n")		
    
    # Write translation 	
    nex.write("Begin trees;\n")	
    nex.write("\tTranslate\n")	
    for idx,n in enumerate(names):
        nex.write("\t\t" + str(idx+1) + ' ' + n + date_str + "\n") # if taxa names are non-numerical strings
        #nex.write("\t\t" + n + ' ' + n + date_str + "\n") # if taxa names are numbers
    nex.write(";\n")
    
    # Write tree
    with open(in_tree, 'r') as file:
        tree_str = file.read().replace('\n', '')
    for idx,n in enumerate(names): # if taxa names are non-numerical strings 
        tree_str = re.sub(n, str(idx+1), tree_str)    
    nex.write("tree TREE1 = " + tree_str + "\n")
    nex.write("End;\n")

def add_tree_label(ax,tree,label_str,cumulative_displace):
    
    "Add tree label"
    curr_min_x = np.Inf
    curr_max_x = -np.Inf
    curr_min_y = np.Inf
    curr_max_y = -np.Inf
    for k in tree.Objects:
        if k.x > curr_max_x:
            curr_max_x = k.x
        if k.x < curr_min_x:
            curr_min_x = k.x
        if k.y > curr_max_y:
            curr_max_y = k.y
        if k.y < curr_min_y:
            curr_min_y = k.y
    x_text_pos = cumulative_displace + (curr_max_x - curr_min_x) / 2
    y_text_pos = curr_max_y + (curr_max_y - curr_min_y) * 0.05
    ax.text(x_text_pos,y_text_pos,label_str,horizontalalignment='center',fontsize=12)
        

def plot(tree_files,fig_name,tree_labels=None):

    "Params to vary to improve figure"
    displaceFrac = 0.5 #0.2 # sets displacement between neighboring trees based on fraction of max tree height
    branch_width = 2 # branch thinkness/width in plotted trees (default is 4)
    xax_border = 0.1 # was 0.2 -- should be relative to cumulative-displace
    yax_border = 2 # was 0.2 -- should be relative to ySpan of trees
    
    "Load trees into tree dict"
    trees={} ## dict
    segments = list(range(len(tree_files)))
    for idx,tr in enumerate(tree_files):
        output_tree = tr.replace('.tre','.nexus')
        convert2nexus(tr,output_tree)
        ll=bt.loadNexus(output_tree,absoluteTime=False)
        #ll.setAbsoluteTime(2020.0)
        trees[idx]=ll
    print('\nDone!')
    
    "Rescale tree heights so they are all equal"
    tree_heights = []
    for t,tr in enumerate(trees.keys()): ## iterate over trees
        cur_tree=trees[tr] ## fetch tree object
        tree_heights.append(cur_tree.treeHeight)
    max_height_cap = max(tree_heights)
    for t,tr in enumerate(trees.keys()): ## iterate over trees
        cur_tree=trees[tr] ## fetch tree object
        for k in cur_tree.Objects: ## iterate over a flat list of branches
            k.length = k.length * (max_height_cap/cur_tree.treeHeight)
        cur_tree.traverse_tree() ## required to set heights
        cur_tree.treeStats() ## report stats about tree
    
    "Compute displaceAmount on the same scale as the tree heights"
    displaceAmount= max_height_cap * displaceFrac # 50% of maximum tree height
    
    "Extract tip positions"
    tip_positions={x:{} for x in segments} ## remember the position of each tip in each tree
    for t,tr in enumerate(trees.keys()): ## iterate over trees
        cur_tree=trees[tr] ## fetch tree object
        for k in cur_tree.Objects:
            if k.branchType=='leaf':
                tip_positions[tr][k.name]=(k.height,k.y) ## remember (X, Y) position of tip
    
    cmap=mpl.cm.Spectral
    
    for X in range(10): ## 10 untangling iterations
        print('iteration %d'%(X+1))
        for t,tr in enumerate(segments): ## iterate over each tree
            print(tr)
            ptr=segments[t-1] ## previous tree
            ntr=segments[t] ## next tree
            seg=trees[ptr] ## fetch appropriate tree
            nex_seg=trees[ntr]
            for k in sorted(nex_seg.Objects,key=lambda q:q.height): ## iterate over branches from most recent to oldest
                if k.branchType=='node': ## can only sort nodes
                    leaves=[[seg.tipMap[tip] for tip in w.leaves if tip in seg.tipMap] if w.branchType=='node' else [w.name] for w in k.children] ## descendent tips in current order
                    
    #                 leaves=[[seg.tipMap[tip] for tip in w.leaves] if w.branchType=='node' else [w.name] for w in k.children] ## descendent tips in current order
                    
                    for c in range(len(leaves)):
    #                     leaves[c]=sorted(leaves[c],key=lambda x:tip_positions[ntr][x][1]) ## sort leaves according to their positions in the next tree
                        leaves[c]=sorted(leaves[c],key=lambda x:tip_positions[ntr][x][1] if x in tip_positions[ntr] else 0.0) ## sort leaves according to their positions in the next tree
                    
                    ys=[sorted([tip_positions[ntr][w][1] for w in cl if w in tip_positions[ntr]]) for cl in leaves] ## extract y positions of descendents
                    merge_ys=sum(ys,[]) ## flatten list of tip y coordinates
                    ypos=range(min(merge_ys),max(merge_ys)+1) ## get y positions of tips in current order
                    order={i:x for i,x in enumerate(leaves)} ## dict of tip order: tip name
                    
                    new_order=sorted(order.keys(),key=lambda x:-np.mean([(tip_positions[ptr][order[x][w]][1]-ypos[w]) for w in range(min([len(order[x]),len(ypos)])) if order[x][w] in tip_positions[ptr]])) ## get new order by sorting existing order based on y position differences
                    
    #                 new_order=sorted(order.keys(),key=lambda x:-np.mean([(tip_positions[ptr][order[x][w]][1]-ypos[w]) for w in range(len(order[x]))])) ## get new order by sorting existing order based on y position differences
                    
                    if new_order!=range(len(leaves)): ## if new order is not current order
                        k.children=[k.children[i] for i in new_order] ## assign new order of child branches
                        nex_seg.drawTree() ## update y positions
    
                        for w in nex_seg.Objects: ## iterate over objects in next tree
                            if w.branchType=='leaf':
                                tip_positions[ntr][w.name]=(w.height,w.y) ## remember new positions
                    
            if t==0: ## if first tree
                trees[segments[t]].drawTree() ## update positions
                lvs=sorted([w for w in trees[segments[t]].Objects if w.branchType=='leaf'],key=lambda x:x.y) ## get leaves in y position order
                
                norm=mpl.colors.Normalize(0,len(lvs))
                pos_colours={w.name:cmap(norm(w.y)) for w in lvs} ## assign colour
                
    
    "Plotting all trees"
    fig,ax = plt.subplots(figsize=(12,8),facecolor='w')
    
    #traitName='PB1' ## choose a trait to colour branches by
    cmap=mpl.cm.viridis # colormap 
    cumulative_displace=0 ## this tracks the "current" x position, so trees are plotted one after another
    
    tree_names=segments
    ref_tree = segments[0] # first tree
    
    for t,tr in enumerate(tree_names): ## iterate over trees
        cur_tree=trees[tr] ## fetch tree object
        
        x_attr=lambda k: k.height+cumulative_displace
        #x_attr=lambda k: (k.height*(max_height/cur_tree.treeHeight))+cumulative_displace
        
        b_func=lambda k: branch_width 
        s_func=lambda k: 30
        su_func=lambda k: 60
        ct_func=lambda k: cmap(tip_positions[ref_tree][k.name][1]/float(cur_tree.ySpan))
        cu_func=lambda k: 'k'
        z_func=lambda k: 100
        zu_func=lambda k: 99
        
        def colour_func(node):
            #if traitName in node.traits:
            #    return 'indianred' if node.traits[traitName]=='V' else 'steelblue'
            #else:
                return 'k'
            
        cn_func=colour_func
        
        cur_tree.plotTree(ax,x_attr=x_attr,branchWidth=b_func,colour_function=cn_func)
        cur_tree.plotPoints(ax,x_attr=x_attr,size_function=s_func,colour_function=ct_func,zorder_function=z_func)
        cur_tree.plotPoints(ax,x_attr=x_attr,size_function=su_func,colour_function=cu_func,zorder_function=zu_func)
        
        for k in cur_tree.Objects: ## iterate over branches
            if isinstance(k,bt.leaf): ## if leaf...
                y=k.y
                pos_in_first_tree=tip_positions[ref_tree][k.name][1] ## fetch y coordinate of same tip in the first tree
                frac_pos=pos_in_first_tree/float(cur_tree.ySpan) ## normalize coordinate to be within interval [0.0,1.0]
    
                if t!=len(tree_names)-1: ## as long as we're not at the last tree - connect tips with coloured lines
                    next_x,next_y=tip_positions[tree_names[t+1]][k.name] ## fetch coordinates of same tip in next tree
                    next_x+=cumulative_displace+cur_tree.treeHeight+displaceAmount ## adjust x coordinate by current displacement and future displacement
                    nextIncrement=cumulative_displace+cur_tree.treeHeight
                    ax.plot([x_attr(k),nextIncrement+0.05*displaceAmount,nextIncrement+0.95*displaceAmount,next_x],[y,y,next_y,next_y],lw=1,ls='-',color=cmap(frac_pos),zorder=0) ## connect current tip with same tip in the next tree
        
        if tree_labels:
            add_tree_label(ax,cur_tree,tree_labels[tr],cumulative_displace)
        
        cumulative_displace+=cur_tree.treeHeight+displaceAmount ## increment displacement by the height of the tree
    
    [ax.spines[loc].set_visible(False) for loc in ['top','right','left','bottom']]
    
    ax.tick_params(axis='x',size=0)
    ax.tick_params(axis='y',size=0)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    ax.set_ylim(-yax_border,cur_tree.ySpan+yax_border) ## set y limits
    ax.set_xlim(-xax_border,cumulative_displace+xax_border)
    
    plt.savefig(fig_name, dpi=300)

if  __name__ == '__main__':
    
    segments = 4
    
    path = "./sim_trees/"
    ML_tree_files = [path + "disentangler_test0_MLTree" + str(i) + ".tre" for i in range(segments)]
    tanglegram_fig_name = 'tanglegram-ML-trees.png' 
    
    tree_labels = ['Tree ' + str(s) for s in range(1,segments+1)]
    
    plot(ML_tree_files, tanglegram_fig_name,tree_labels=tree_labels)

