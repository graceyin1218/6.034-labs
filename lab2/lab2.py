# MIT 6.034 Lab 2: Search
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from search import Edge, UndirectedGraph, do_nothing_fn, make_generic_search
import read_graphs

all_graphs = read_graphs.get_graphs()
GRAPH_0 = all_graphs['GRAPH_0']
GRAPH_1 = all_graphs['GRAPH_1']
GRAPH_2 = all_graphs['GRAPH_2']
GRAPH_3 = all_graphs['GRAPH_3']
GRAPH_FOR_HEURISTICS = all_graphs['GRAPH_FOR_HEURISTICS']


#### PART 1: Helper Functions ##################################################

def path_length(graph, path):
    """Returns the total length (sum of edge weights) of a path defined by a
    list of nodes coercing an edge-linked traversal through a graph.
    (That is, the list of nodes defines a path through the graph.)
    A path with fewer than 2 nodes should have length of 0.
    You can assume that all edges along the path have a valid numeric weight."""
    if len(path) == 1:
        return 0

    length = 0
    prev = None
    for point in path:
        if prev == None:
            prev = point
            continue
        length += graph.get_edge(prev, point).length
        prev = point
    return length


def has_loops(path):
    """Returns True if this path has a loop in it, i.e. if it
    visits a node more than once. Returns False otherwise."""
    pathLength = len(path)
    setTrick = set(path)
    if len(setTrick) < pathLength:
        return True
    return False


def extensions(graph, path):
    """Returns a list of paths. Each path in the list should be a one-node
    extension of the input path, where an extension is defined as a path formed
    by adding a neighbor node (of the final node in the path) to the path.
    Returned paths should not have loops, i.e. should not visit the same node
    twice. The returned paths should be sorted in lexicographic order."""
    neighbors = graph.get_neighbors(path[-1])
    extensions = []
    for point in neighbors:
        if point in path:
            continue

        # there must be a better way to copy path..
        newPath = []
        for p in path:
            newPath.append(p)

        newPath.append(point)
        extensions.append(newPath)

    return sorted(extensions)


def sort_by_heuristic(graph, goalNode, nodes):
    """Given a list of nodes, sorts them best-to-worst based on the heuristic
    from each node to the goal node. Here, and in general for this lab, we
    consider a lower heuristic to be "better" because it represents a shorter
    potential path to the goal. Break ties lexicographically by node name."""
    nodes.sort()
    return sorted(nodes, key= lambda node: graph.get_heuristic_value(node, goalNode))


# You can ignore the following line.  It allows generic_search (PART 2) to
# access the extensions and has_loops functions that you just defined in PART 1.
generic_search = make_generic_search(extensions, has_loops)  # DO NOT CHANGE


#### PART 2: Generic Search ####################################################

# Note: If you would prefer to get some practice with implementing search
# algorithms before working on Generic Search, you are welcome to do PART 3
# before PART 2.

# Define your custom path-sorting functions here.
# Each path-sorting function should be in this form:

# def my_sorting_fn(graph, goalNode, paths):
#     # YOUR CODE HERE
#     return sorted_paths
def sort_by_heuristic_fn(graph, goalNode, paths):
    return sorted(paths, key=lambda path: graph.get_heuristic_value(path[-1], goalNode))

def sort_by_path_length_fn(graph, goalNode, paths):
    return sorted(paths, key=lambda path: path_length(graph, path))

def sort_by_path_length_and_heuristic_fn(graph, goalNode, paths):
    return sorted(paths, key=lambda path: path_length(graph, path) + graph.get_heuristic_value(path[-1], goalNode))

generic_dfs = [do_nothing_fn, True, do_nothing_fn, False]

generic_bfs = [do_nothing_fn, False, do_nothing_fn, False]

generic_hill_climbing = [sort_by_heuristic_fn, True, do_nothing_fn, False]

generic_best_first = [do_nothing_fn, True, sort_by_heuristic_fn, False]

generic_branch_and_bound = [do_nothing_fn, True, sort_by_path_length_fn, False]

generic_branch_and_bound_with_heuristic = [do_nothing_fn, True, sort_by_path_length_and_heuristic_fn, False]

generic_branch_and_bound_with_extended_set = [do_nothing_fn, True, sort_by_path_length_fn, True]

generic_a_star = [do_nothing_fn, True, sort_by_path_length_and_heuristic_fn, True]

# Here is an example of how to call generic_search (uncomment to run):
#my_dfs_fn = generic_search(*generic_dfs)
#my_dfs_path = my_dfs_fn(GRAPH_2, 'S', 'G')
#print my_dfs_path

# Or, combining the first two steps:
#my_dfs_path = generic_search(*generic_dfs)(GRAPH_2, 'S', 'G')
#print my_dfs_path


### OPTIONAL: Generic Beam Search
# If you want to run local tests for generic_beam, change TEST_GENERIC_BEAM to True:
TEST_GENERIC_BEAM = True

# The sort_agenda_fn for beam search takes fourth argument, beam_width:
# def my_beam_sorting_fn(graph, goalNode, paths, beam_width):
#     # YOUR CODE HERE
#     return sorted_beam_agenda

def beam_fn(graph, goalNode, paths, beam_width):
    #check if an entire level has been expanded
    prev_length = None
    for path in paths:
        if prev_length == None:
            prev_length = len(path)
            continue
        if len(path) != prev_length:
            return paths
    #sort the paths by their last node's heuristic
    sorted_paths = sorted(paths, key=lambda path: graph.get_heuristic_value(path[-1], goalNode))
    #return the best beam_width paths
    return sorted_paths[:beam_width]

generic_beam = [do_nothing_fn, False, beam_fn, False]

# Uncomment this to test your generic_beam search:
#print generic_search(*generic_beam)(GRAPH_2, 'S', 'G', beam_width=2)


#### PART 3: Search Algorithms #################################################

# Note: It's possible to implement the following algorithms by calling
# generic_search with the arguments you defined in PART 2.  But you're also
# welcome to code them without using generic_search if you would prefer to
# implement the algorithms by yourself.


def dfs(graph, startNode, goalNode):
    search_algorithm = generic_search(generic_dfs[0], generic_dfs[1], generic_dfs[2], generic_dfs[3])
    return search_algorithm(graph, startNode, goalNode)


def bfs(graph, startNode, goalNode):
    search_algorithm = generic_search(generic_bfs[0], generic_bfs[1], generic_bfs[2], generic_bfs[3])
    return search_algorithm(graph, startNode, goalNode)


def hill_climbing(graph, startNode, goalNode):
    search_algorithm = generic_search(generic_hill_climbing[0], generic_hill_climbing[1], generic_hill_climbing[2], generic_hill_climbing[3])
    return search_algorithm(graph, startNode, goalNode)


def best_first(graph, startNode, goalNode):
    search_algorithm = generic_search(generic_best_first[0], generic_best_first[1], generic_best_first[2], generic_best_first[3])
    return search_algorithm(graph, startNode, goalNode)


def beam(graph, startNode, goalNode, beam_width):
    search_algorithm = generic_search(generic_beam[0], generic_beam[1], generic_beam[2], generic_beam[3])
    return search_algorithm(graph, startNode, goalNode, beam_width)


def branch_and_bound(graph, startNode, goalNode):
    search_algorithm = generic_search(generic_branch_and_bound[0], generic_branch_and_bound[1], generic_branch_and_bound[2], generic_branch_and_bound[3])
    return search_algorithm(graph, startNode, goalNode)


def branch_and_bound_with_heuristic(graph, startNode, goalNode):
    search_algorithm = generic_search(generic_branch_and_bound_with_heuristic[0], generic_branch_and_bound_with_heuristic[1], generic_branch_and_bound_with_heuristic[2], generic_branch_and_bound_with_heuristic[3])
    return search_algorithm(graph, startNode, goalNode)


def branch_and_bound_with_extended_set(graph, startNode, goalNode):
    search_algorithm = generic_search(generic_branch_and_bound_with_extended_set[0], generic_branch_and_bound_with_extended_set[1], generic_branch_and_bound_with_extended_set[2], generic_branch_and_bound_with_extended_set[3])
    return search_algorithm(graph, startNode, goalNode)


def a_star(graph, startNode, goalNode):
    search_algorithm = generic_search(generic_a_star[0], generic_a_star[1], generic_a_star[2], generic_a_star[3])
    return search_algorithm(graph, startNode, goalNode)


#### PART 4: Heuristics ########################################################

def is_admissible(graph, goalNode):
    """Returns True if this graph's heuristic is admissible; else False.
    A heuristic is admissible if it is either always exactly correct or overly
    optimistic; it never over-estimates the cost to the goal."""
    for node in graph.nodes:
        if graph.get_heuristic_value(node, goalNode) > path_length(graph, bfs(graph, node, goalNode)):
            return False
    return True


def is_consistent(graph, goalNode):
    """Returns True if this graph's heuristic is consistent; else False.
    A consistent heuristic satisfies the following property for all
    nodes v in the graph:
        Suppose v is a node in the graph, and N is a neighbor of v,
        then, heuristic(v) <= heuristic(N) + edge_weight(v, N)
    In other words, moving from one node to a neighboring node never unfairly
    decreases the heuristic.
    This is equivalent to the heuristic satisfying the triangle inequality."""
    for edge in graph.edges:
        if edge.length < abs(graph.get_heuristic_value(edge.startNode, goalNode) - graph.get_heuristic_value(edge.endNode, goalNode)):
            return False
    return True


### OPTIONAL: Picking Heuristics
# If you want to run local tests on your heuristics, change TEST_HEURISTICS to True:
TEST_HEURISTICS = False

# heuristic_1: admissible and consistent

[h1_S, h1_A, h1_B, h1_C, h1_G] = [None, None, None, None, None]

heuristic_1 = {'G': {}}
heuristic_1['G']['S'] = h1_S
heuristic_1['G']['A'] = h1_A
heuristic_1['G']['B'] = h1_B
heuristic_1['G']['C'] = h1_C
heuristic_1['G']['G'] = h1_G


# heuristic_2: admissible but NOT consistent

[h2_S, h2_A, h2_B, h2_C, h2_G] = [None, None, None, None, None]

heuristic_2 = {'G': {}}
heuristic_2['G']['S'] = h2_S
heuristic_2['G']['A'] = h2_A
heuristic_2['G']['B'] = h2_B
heuristic_2['G']['C'] = h2_C
heuristic_2['G']['G'] = h2_G


# heuristic_3: admissible but A* returns non-optimal path to G

[h3_S, h3_A, h3_B, h3_C, h3_G] = [None, None, None, None, None]

heuristic_3 = {'G': {}}
heuristic_3['G']['S'] = h3_S
heuristic_3['G']['A'] = h3_A
heuristic_3['G']['B'] = h3_B
heuristic_3['G']['C'] = h3_C
heuristic_3['G']['G'] = h3_G


# heuristic_4: admissible but not consistent, yet A* finds optimal path

[h4_S, h4_A, h4_B, h4_C, h4_G] = [None, None, None, None, None]

heuristic_4 = {'G': {}}
heuristic_4['G']['S'] = h4_S
heuristic_4['G']['A'] = h4_A
heuristic_4['G']['B'] = h4_B
heuristic_4['G']['C'] = h4_C
heuristic_4['G']['G'] = h4_G


##### PART 5: Multiple Choice ##################################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '1'

ANSWER_4 = '3'


#### SURVEY ####################################################################

NAME = "Grace Yin"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = "2"
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = "I feel bad about using generic_search in part 3, and I would have tried to implement them myself if I had the time... Speaking of which, could we please not have 3 psets due in one week? Thanks :)"


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the online tester. DO NOT CHANGE!

generic_dfs_sort_new_paths_fn = generic_dfs[0]
generic_bfs_sort_new_paths_fn = generic_bfs[0]
generic_hill_climbing_sort_new_paths_fn = generic_hill_climbing[0]
generic_best_first_sort_new_paths_fn = generic_best_first[0]
generic_branch_and_bound_sort_new_paths_fn = generic_branch_and_bound[0]
generic_branch_and_bound_with_heuristic_sort_new_paths_fn = generic_branch_and_bound_with_heuristic[0]
generic_branch_and_bound_with_extended_set_sort_new_paths_fn = generic_branch_and_bound_with_extended_set[0]
generic_a_star_sort_new_paths_fn = generic_a_star[0]

generic_dfs_sort_agenda_fn = generic_dfs[2]
generic_bfs_sort_agenda_fn = generic_bfs[2]
generic_hill_climbing_sort_agenda_fn = generic_hill_climbing[2]
generic_best_first_sort_agenda_fn = generic_best_first[2]
generic_branch_and_bound_sort_agenda_fn = generic_branch_and_bound[2]
generic_branch_and_bound_with_heuristic_sort_agenda_fn = generic_branch_and_bound_with_heuristic[2]
generic_branch_and_bound_with_extended_set_sort_agenda_fn = generic_branch_and_bound_with_extended_set[2]
generic_a_star_sort_agenda_fn = generic_a_star[2]
