"""
Created on Mon Feb 1st 10:03:34 2021

Clean version of struct coalescent w/ anc recombination (SCAR) likelihood function
Ancestral states can be given (known) or marginalized (uknown)

This version includes the sum links correction that tracks what ancestral material each lineage carries when computing recombination rates

ARG requirements for TreeSequence in ts are strictly enfored in this version
So multiple-mergers at coalescent events cannot be handeled

@author: david
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.linalg import expm
from scipy.optimize import minimize_scalar

global debug
debug = False
known_ancestral_states = False
dt_step = 0.1 # was 0.1

        
def get_line_links(line,children,rights,lefts):
    
    line_links = 0
    if len(children[children==line])==1:
        line_links = (rights[children==line] - lefts[children==line])[0] - 1
    elif len(children[children==line])>=2:
        line_links = max(rights[children==line]) - min(lefts[children==line]) - 1 
        
    return line_links

"""
    Compute the negative log likelihood of ARG
    Here we compute the negatve log likelihood because the scipy opt minimizes the func
    Note: ts, M, Ne, genome_length need to be passed through optimizer as a tuple
    
    If enfore_ARG_rules is True then TreeSequence must satisfy strict ARG rules:
        -Each coal node must have exactly two children
        -Each recomb node must have one child and two parents
"""
def compute_neg_log_like(rho,ts,M,Ne,genome_length,enfore_ARG_rules=False):

    states = [st.id for st in ts.populations()]
    pops = ts.num_populations
    if pops == 0: # we never assigned populations
        pops = 1
    samples = ts.num_samples
    
    "Get transition rate matrix"
    Q = M - np.diag(np.sum(M,axis=1)) # set diagonals to negative row sums
    
    populations = np.array(ts.tables.nodes.population,ndmin=1)
    
    children = np.array(ts.tables.edges.child,ndmin=1)
    parents = np.array(ts.tables.edges.parent,ndmin=1)
    lefts = np.array(ts.tables.edges.left,ndmin=1)
    rights = np.array(ts.tables.edges.right,ndmin=1)
    
    "Lineage arrays"
    active_lines = [] # active lines in ARG
    active_rec_links = [] # tracks ancestral material that can recomine on active_lines
    line_state_probs = [] # lineage state probabilities for active lines
    log_like = 0.0 # log likelihood of full tree
    
    "Iterate through each event/node in tree sequence working backwards through time"
    for idx, event in enumerate(ts.tables.nodes):
        
        "Get time of event and time of next event"
        event_time = event.time
        if (idx+1 < len(ts.tables.nodes)): # if not at final event
            next_time = ts.tables.nodes[idx+1].time
        else:
            next_time = event.time
        t_elapsed = next_time - event_time # time elapsed between events
        
        """
            Flags on ts.nodes:
                1 = samples
                0 = coalescent
                131072 = recombination event
                262144 = common ancestor in ARG (but no coalescence in local trees)
        """
        event_type = None
        if event.flags == 1:
            event_type = 'sample'
        if event.flags == 0:
            event_type = 'coalescent'
        if event.flags == 131072:
            event_type = 'recombination'
        if event.flags == 262144:
            event_type = 'hidden_coalescent'
        if event.flags == 524288:
            event_type = 'migration'
        
        "Initialize prob seeing events or no events"
        event_prob = 1.0
        prob_no_coal = 1.0
        prob_no_mig = 1.0
        prob_no_recomb = 1.0
        
        "Update active lineages based on event type: coalescent/sampling/migration events"
        if 'sample' == event_type:
            
            "Add sampled lineage"
            active_lines.append(idx)
            active_rec_links.append(get_line_links(idx,children,rights,lefts))
            state_probs = np.zeros(pops)
            if event.population == -1: # we never assigned populations
                state_probs[0] = 1.0 # set prob to 1.0 for sampled state
            else:
                state_probs[event.population] = 1.0 # set prob to 1.0 for sampled state
            line_state_probs.append(state_probs)            
        
        if 'coalescent' == event_type:
            
            "Get children of parent node at coalescent event"
            coal_children = children[parents == idx] # parent has id == idx in parent column of edges table
            
            "The same parent/child edge may occur more than once in the tree series if not in contiguous local trees"
            coal_children = np.unique(coal_children)
            
            """
                Find coal_children in active_lines
            """
            coal_children = [x for x in coal_children if x in active_lines]
            child_indexes = [active_lines.index(x) for x in coal_children]
            
            "Make sure coalescent events only occur among two lineages"
            if enfore_ARG_rules:
                if len(coal_children) != 2:
                    print("ERROR: Parent has more or less than two children at coalescent node")
                assert len(coal_children) == 2
            
            """
                New method for arbitrary number of children
            """
            coal_probs = np.ones(pops)
            for child_idx in child_indexes:
                coal_probs *= line_state_probs[child_idx]
            coal_probs = coal_probs / Ne
            lambda_sum = sum(coal_probs)
            event_prob = lambda_sum
            
            "Compute new parent state probs"
            if known_ancestral_states:
                parent_probs = np.zeros(pops)
                parent_probs[event.population] = 1.0
            else:
                parent_probs = coal_probs / lambda_sum # renormalize probs
                
            "Update lineage arrays - overwriting child1 with parent"
            active_lines[child_indexes[0]] = idx # name of parent
            active_rec_links[child_indexes[0]] = get_line_links(idx,children,rights,lefts)
            line_state_probs[child_indexes[0]] = parent_probs
            child_indexes.pop(0) # remove first index given to parent
            for child_idx in sorted(child_indexes, reverse=True): # remove in reverse order so indexes don't change
                del active_lines[child_idx]
                del active_rec_links[child_idx]
                del line_state_probs[child_idx]
            
                
            
            
            if len(coal_children) == 2:
            
                child1 = coal_children[0]
                child2 = coal_children[1]
                
                child1_idx = active_lines.index(child1)
                child2_idx = active_lines.index(child2)
                
                "Can we check if child1 or child2 coalesce deeper in the tree"
                #lines_to_keep = []
                #lines_to_keep_state_probs = []
                #deeper_coal_nodes = parents[children == child1_idx]
                #deeper_coal_nodes = [x for x in deeper_coal_nodes if ts.tables.nodes[x].time > event_time]
                #if len(deeper_coal_nodes) > 0:
                #    print('Removing coalescing lineage that will coalesce at deeper node')
                #    lines_to_keep.append(child1)
                #    lines_to_keep_state_probs.append(line_state_probs[child1_idx])
                #deeper_coal_nodes = parents[children == child2_idx]
                #deeper_coal_nodes = [x for x in deeper_coal_nodes if ts.tables.nodes[x].time > event_time]
                #if len(deeper_coal_nodes) > 0:
                #    print('Removing coalescing lineage that will coalesce at deeper node')
                #    lines_to_keep.append(child2)
                #    lines_to_keep_state_probs.append(line_state_probs[child2_idx])
                    
                if debug:
                    print(child1, child1_idx)
                    print(child2, child2_idx)
                    
                "Compute likelihood of coalescent event"
                p1 = line_state_probs[child1_idx]
                p2 = line_state_probs[child2_idx]
                coal_probs = (p1 * p2) / Ne # NOTE: this is element-wise vector multiplication/division
                lambda_sum = sum(coal_probs)
                event_prob = lambda_sum
                
                "Compute new parent state probs"
                if known_ancestral_states:
                    parent_probs = np.zeros(pops)
                    parent_probs[event.population] = 1.0
                else:
                    parent_probs = coal_probs / lambda_sum # renormalize probs
                
                "Update lineage arrays - overwriting child1 with parent"
                active_lines[child1_idx] = idx # name of parent
                active_rec_links[child1_idx] = get_line_links(idx,children,rights,lefts)
                line_state_probs[child1_idx] = parent_probs
                del active_lines[child2_idx]
                del active_rec_links[child2_idx]
                del line_state_probs[child2_idx]
                
                "Add back lines that will coalesce at a deeper time"
                #for idx_ln, ln in enumerate(lines_to_keep):
                #    active_lines.append(ln)
                #    active_rec_links.append(get_line_links(ln,children,rights,lefts))
                #    line_state_probs.append(lines_to_keep_state_probs[idx_ln])
                
            elif len(coal_children) == 1:
                
                child1 = coal_children[0]
                
                child1_idx = active_lines.index(child1)
                
                if debug:
                    print(child1, child1_idx)
                    
                "Compute likelihood of coalescent event"
                event_prob = 1.0
                
                "Compute new parent state probs"
                if known_ancestral_states:
                    parent_probs = np.zeros(pops)
                    parent_probs[event.population] = 1.0
                else:
                    parent_probs = line_state_probs[child1_idx] # same as child
                
                "Update lineage arrays - overwriting child1 with parent"
                active_lines[child1_idx] = idx # name of parent
                active_rec_links[child1_idx] = get_line_links(idx,children,rights,lefts)
                line_state_probs[child1_idx] = parent_probs
                
        
        if 'hidden_coalescent' == event_type:
            
            "Hidden coalescent in ARG not observed in local trees"
            "Need to update active_lines but nothing else"
            
            coal_children = children[parents == idx]
            coal_children = np.unique(coal_children)
            child1 = coal_children[0]
            child2 = coal_children[1]
            child1_idx = active_lines.index(child1)
            child2_idx = active_lines.index(child2)
            
            "Did not have this before for hidden coal events -- compute likelihood of coalescent event"
            p1 = line_state_probs[child1_idx]
            p2 = line_state_probs[child2_idx]
            coal_probs = (p1 * p2) / Ne
            lambda_sum = sum(coal_probs)
            event_prob = lambda_sum
            
            "Compute new parent state probs"
            if known_ancestral_states:
                parent_probs = np.zeros(pops)
                parent_probs[event.population] = 1.0
            else:
                parent_probs = coal_probs / lambda_sum
            
            "Update lineage arrays - overwriting child1 with parent"
            active_lines[child1_idx] = idx # name of parent
            active_rec_links[child1_idx] = get_line_links(idx,children,rights,lefts)
            line_state_probs[child1_idx] = parent_probs
            del active_lines[child2_idx]
            del active_rec_links[child2_idx]
            del line_state_probs[child2_idx]
        
        if "recombination" == event_type:
            
            """
                At a recombination event: a child node will have two different parents
                We need to find the child shared among these two parents
                Then replace child with left parent and add right parent
            """
            
            "Find child of parent node"
            child = children[parents == idx]
            child = np.unique(child)
            assert len(child) == 1
            
            "Remember that child may have already been removed"
            if child in active_lines:
            
                "Get indexes of both (left and right) parent of child"
                recomb_parents = parents[children == child]
                
                "Parents edges may occur more than once in the tree series if not in contiguous trees"
                recomb_parents = np.unique(recomb_parents)
                
                """
                    We're constructing the node/edge tables slightly differently here 
                    Because we’re not including recombination events in local trees besides those immediately adjacent to a breakpoint. 
                    So the children of a recombination node may change across the TS. 
                    So here we find the recomb_parents that are truly recombination events
                    Then make sure recombination event results in a child splitting into two parents"
                """
                recomb_parents = [x for x in recomb_parents if ts.tables.nodes[x].flags == 131072] # have to be recombination event
                assert len(recomb_parents) == 2
                
                left_parent = recomb_parents[0]
                right_parent = recomb_parents[1]
    
                child_idx = active_lines.index(child)
                
                "Can we check if child we are removing is involved in events deeper in the tree"
                #lines_to_keep = []
                #lines_to_keep_state_probs = []
                #deeper_event_nodes = parents[children == child]
                #deeper_event_nodes = [x for x in deeper_event_nodes if ts.tables.nodes[x].time > event_time]
                #if len(deeper_event_nodes) > 0:
                #    print('Removing recombining lineage that will coalesce at deeper node')
                #    lines_to_keep.append(child)
                #    lines_to_keep_state_probs.append(line_state_probs[child_idx])
                
                """
                    Compute recombination event prob
                    Links gives # of sites at which lineage carries material ancestral to the sample
                """
                links = active_rec_links[child_idx] # should be equivalent to above
                event_prob = rho * links / (genome_length - 1)
                
                "Compute new parent state probs"
                if known_ancestral_states:
                    parent_probs = np.zeros(pops)
                    parent_probs[event.population] = 1.0
                else:
                    """
                        Should parent state probs be weighted by prob of recomb event in each pop?
                    """
                    parent_probs = line_state_probs[child_idx]
                
                "Update lineage arrays - overwriting child with left parent"
                active_lines[child_idx] = left_parent # name of parent
                active_rec_links[child_idx] = get_line_links(left_parent,children,rights,lefts)
                line_state_probs[child_idx] = parent_probs
                
                "Add other parent"
                active_lines.append(right_parent)
                active_rec_links.append(get_line_links(right_parent,children,rights,lefts))
                line_state_probs.append(parent_probs)
                
                "Add back lines involved in events at deeper times"
                #for idx_ln, ln in enumerate(lines_to_keep):
                #    active_lines.append(ln)
                #    active_rec_links.append(get_line_links(ln,children,rights,lefts))
                #    line_state_probs.append(lines_to_keep_state_probs[idx_ln])  
        
        if 'migration' == event_type:
            
            "Have not yet added migration"
            mig_child = children[parents == idx] # parent has id == idx in parent column of edges table
            "The same parent/child edge may occur more than once in the tree series if not in contiguous local trees"
            mig_child = np.unique(mig_child)
            
            "Migration info from nodes list"
            curr_state = populations[mig_child[0]]
            new_state = populations[idx]
            
            migrant_idx = active_lines.index(mig_child) #change this for ts index
            
            "Update lineage arrays"
            active_lines[migrant_idx] = idx # name of parent
            
            "Compute event prob"
            if known_ancestral_states:
                new_probs = np.zeros(pops)
                new_probs[new_state] = 1.0 # event. population
                line_state_probs[migrant_idx] = new_probs
                event_prob = M[curr_state][new_state]
            else:
                event_prob = 1.0 # pretend as if we don't see migration events
            
        "Integrate lineage prob equations backwards" 
        
        "Compute prob of no coalescent over time interval"
        if not np.isclose(t_elapsed, 0):
            
            if known_ancestral_states:
                
                A = np.zeros(pops)
                for probs in line_state_probs: A += probs # sum line probs to get total number of lines in each state
                
                "Compute prob of no coalescent over time interval"
                pairs = (A * (A-1)) / 2 # number of pairs in each pop
                lambdas =  pairs * (1/Ne) # coal rate in each pop   
                prob_no_coal = np.exp(-np.sum(lambdas)*t_elapsed)
            
                "Compute prob of no migration over the time interval"
                sam = 0
                for i in range(pops):
                    for z in range(pops):
                        sam += (A[i])*(M[i][z])
                prob_no_mig = np.exp(-sam*t_elapsed)
                
                """
                    Compute prob of no recombination event over the time interval
                    Links are computed per population b/c we are assuming recombination can only happen in same pop
                    Vectorized product-sums using column-wise multiplication in numpy
                """
                line_prod = np.array(line_state_probs) * np.array(active_rec_links)[:, np.newaxis]
                sum_links = np.sum(np.sum(line_prod))
                          
                prob_no_recomb = np.exp(-sum_links * rho / (genome_length - 1) * t_elapsed) # assumes rho / genome_length is constant across pops
                
            else:
                
                "Should move everything below into seperate function because this will change depending on approximation used"
            
                "Integrate lineage prob equations backwards"
                dt_times = list(np.arange(event_time,next_time,dt_step)) # integration steps going backwards in time
                for idx,tx in enumerate(dt_times):
                    
                    "Fix this so index does not go out of bounds"
                    if (idx+1 < len(dt_times)):
                        dt = dt_times[idx+1] - tx # integration time step
                    else:
                        dt = next_time - tx
                    if debug:
                        print("dttimes",tx,dt,event_time,next_time)

                    "Should not need to exponentiate transition matrix if dt is small enough"
                    expQdt = expm(Q*dt) # exponentiate time-scaled transition rate matrix

                    "Update line state probs using Euler integration"
                    for ldx,probs in enumerate(line_state_probs):
                        line_state_probs[ldx] = np.matmul(probs,expQdt)
                    
                    A = np.zeros(pops)
                    for probs in line_state_probs: A += probs # sum line probs to get total number of lines in each state
                    
                    "Compute prob of no coalescent over time interval"
                    pairs = (A * (A-1)) / 2 # number of pairs in each pop
                    pairs = pairs.clip(min=0) # make sure non are negative
                    lambdas = pairs * (1/Ne) # coal rate in each pop
                    prob_no_coal *= np.exp(-np.sum(lambdas)*dt)
                    
                    "Compute prob of no migration over the time interal"
                    prob_no_mig = 1.0
                    
                    """
                        Compute prob of no recombination event over the time interval
                        Links are computed per population b/c we are assuming recombination can only happen in same pop
                        Vectorized product-sums using column-wise multiplication in numpy
                    """
                    line_prod = np.array(line_state_probs) * np.array(active_rec_links)[:, np.newaxis]
                    sum_links = np.sum(np.sum(line_prod))
                                        
                    prob_no_recomb *= np.exp(-sum_links * rho / (genome_length - 1) * dt)
        
        log_like += np.log(event_prob) + np.log(prob_no_coal) + np.log(prob_no_mig) + np.log(prob_no_recomb)
        
    return -log_like


"""
    Find MLE of single parameter (rho for now) using numerical optimization
"""
def opt_MLE(ts,params,bounds=(0,2)):
    
    "Convert params dict to tuple"
    if 'M' in params:
        M = np.transpose(np.array(params['M'])) # transpose to get reverse time matrix
    else:
        print('Need to specify migration rate matrix M')    
    
    if 'Ne' in params:
        Ne = np.array(params['Ne'])
    else:
        print('Need to specify eff pop sizes Ne')
        
    if 'genome_length' in params:
        genome_length = params['genome_length']
    else:
        print('Need to specify genome length')
    like_args = (ts,M,Ne,genome_length) # args need to be passed as tuple
    
    res = minimize_scalar(compute_neg_log_like, args=like_args, bounds=bounds, method='bounded')
    mle = res.x

    return mle

if __name__ == '__main__':
       
    import ARGSimulator
    
    "Specify sim params"
    samples = 10
    genome_length = 1e4
    rho = 5 #1e-1
    rho_per_site = rho / genome_length
    Ne = 1.0  # effective pop sizes
    
    "Migration and configuration of samples"
    val = 0.25
    #M = [[0.0,val,val], [val,0.0,val], [val,val,0.0]]  # migration rate matrix
    #M = [[0.0,val],[val,0.0]]  # migration rate matrix
    M = [[0]]
    
    "Store params in dict"
    params = {'Ne': Ne, 'rho': rho, 'M': M, 'genome_length': genome_length, 'sample_sizes':  samples}
    
    "Run sim(s)"
    ts = ARGSimulator.sim_ARG(sample_size=samples,Ne=Ne,length=genome_length,recombination_rate=rho_per_site,min_breakpoints=1)
    #ts = ARGSimulator.sim_ARG(params,min_breakpoints=1,plot=False)
    
    breaks = len(ts.breakpoints(as_array=True)) - 2 # minus 2 b/c tskit counts ends as breakpoints
    print('recombination breakpoints = ' + str(breaks))
    
    #mig_events = ts.num_migrations
    #print('Num migrations: ', str(ts.num_migrations))
    
    "Check numerical optimization for MLE of single param"
    bounds = (0.0,10)
    mle = opt_MLE(ts,params,bounds=bounds)
    print(mle)
    
    "Check likelihood is valid"
    #L = compute_like(ts,**params)
    
    "Run like profile on one param"
    #like_profile(ts,params,Ne)
    #like_profile_rho(ts,params,rho)
    #like_profile_M(ts,params,M)

