# MIT 6.034 Lab 4: Constraint Satisfaction Problems
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from constraint_api import *
from test_problems import get_pokemon_problem

#### PART 1: WRITE A DEPTH-FIRST SEARCH CONSTRAINT SOLVER

def has_empty_domains(csp) :
    "Returns True if the problem has one or more empty domains, otherwise False"
    for variable in csp.domains:
        if len(csp.get_domain(variable)) == 0:
            return True
    return False

def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    assigned_values = csp.assigned_values
    for var1 in assigned_values:
        for var2 in assigned_values:
            if var1 == var2:
                continue
            for constraint in csp.constraints_between(var1, var2):
                if not constraint.check(assigned_values[var1], assigned_values[var2]):
                    return False

    return True

def solve_constraint_dfs(problem) :
    """Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values), and
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple."""

    # should be a list of problem states to examine for solutions.
    agenda = [problem]

    extension_count = 0

    while len(agenda) > 0:
        next_problem = agenda.pop(0)
        extension_count += 1
        if has_empty_domains(next_problem) or not check_all_constraints(next_problem):
            #this won't work
            continue
        if len(next_problem.unassigned_vars) == 0:
            return (next_problem.assigned_values, extension_count)

        new_var = next_problem.pop_next_unassigned_var()

        i = 0
        for val in next_problem.get_domain(new_var):
            new_prob = next_problem.copy().set_assigned_value(new_var, val)
            agenda.insert(i, new_prob)
            i += 1
    return (None, extension_count)

#### PART 2: DOMAIN REDUCTION BEFORE SEARCH

def eliminate_from_neighbors(csp, var) :
    """Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None."""
    var_domain = csp.get_domain(var)
    reduced = []
    for neighbor in csp.get_neighbors(var):
        neighbor_domain = csp.get_domain(neighbor)[:]
        for val1 in neighbor_domain:
            # violates *A* constraint with *EVERYTHING* in var's domain
            violates_everything = True
            for val2 in var_domain:
                no_violations = True
                for constraint in csp.constraints_between(var, neighbor):
                    if not constraint.check(val2, val1):
                        no_violations = False
                        break
                if no_violations:
                    violates_everything = False
                    break
            if violates_everything:
                csp.eliminate(neighbor, val1)
                if not neighbor in reduced:
                    reduced.append(neighbor)
                if has_empty_domains(csp):
                    return None
    return sorted(reduced)

def domain_reduction(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    If queue is None, initializes propagation queue by adding all variables in
    their default order.  Returns a list of all variables that were dequeued,
    in the order they were removed from the queue.  Variables may appear in the
    list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None."""
    if queue == None:
        queue = csp.get_all_variables()

    to_return = []
    while len(queue) > 0:
        var = queue.pop(0)
        var_domain = csp.get_domain(var)
        to_return.append(var)

        for neighbor in csp.get_neighbors(var):
            #if this neighbor has values that are incompatible with the constraints between
            # var and n, remove incompatible values from neighbor's domain

            # most of this was copied from above
            neighbor_domain = csp.get_domain(neighbor)[:]
            for val1 in neighbor_domain:
                # violates *A* constraint with *EVERYTHING* in var's domain
                violates_everything = True
                for val2 in var_domain:
                    no_violations = True
                    for constraint in csp.constraints_between(var, neighbor):
                        if not constraint.check(val2, val1):
                            no_violations = False
                            break
                    if no_violations:
                        violates_everything = False
                        break
                if violates_everything:
                    csp.eliminate(neighbor, val1)
                    #if you reduce the neighbor's domain, add the neighbor to the queue 
                    # (if it isn't there already)
                    if not neighbor in queue:
                        queue.append(neighbor) 
                    if has_empty_domains(csp):
                        return None
    return to_return

# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DON'T use domain reduction before solving it?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.

#solve_constraint_dfs(get_pokemon_problem())[1]

ANSWER_1 = 20


# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DO use domain reduction before solving it?

# domain_reduction_problem = get_pokemon_problem()
# domain_reduction(domain_reduction_problem)
# print(solve_constraint_dfs(domain_reduction_problem))

ANSWER_2 = 6



#### PART 3: PROPAGATION THROUGH REDUCED DOMAINS

def solve_constraint_propagate_reduced_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs."""
    
    agenda = [problem]

    extension_count = 0

    while len(agenda) > 0:
        next_problem = agenda.pop(0)
        extension_count += 1
        if has_empty_domains(next_problem) or not check_all_constraints(next_problem):
            #this won't work
            continue
        if len(next_problem.unassigned_vars) == 0:
            return (next_problem.assigned_values, extension_count)

        new_var = next_problem.pop_next_unassigned_var()

        i = 0
        for val in next_problem.get_domain(new_var):
            new_prob = next_problem.copy().set_assigned_value(new_var, val)
            domain_reduction(new_prob, [new_var])
            agenda.insert(i, new_prob)
            i += 1
    return (None, extension_count)

# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with propagation through reduced domains? (Don't use domain reduction
#    before solving it.)

# prob = get_pokemon_problem()
# solve_constraint_propagate_reduced_domains(prob)

ANSWER_3 = 7


#### PART 4: PROPAGATION THROUGH SINGLETON DOMAINS

def domain_reduction_singleton_domains(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Only propagates through singleton domains.
    Same return type as domain_reduction."""
    if queue == None:
        queue = csp.get_all_variables()

    to_return = []
    while len(queue) > 0:
        var = queue.pop(0)
        var_domain = csp.get_domain(var)

        to_return.append(var)

        for neighbor in csp.get_neighbors(var):
            #if this neighbor has values that are incompatible with the constraints between
            # var and n, remove incompatible values from neighbor's domain

            # most of this was copied from above
            neighbor_domain = csp.get_domain(neighbor)[:]
            for val1 in neighbor_domain:
                # violates *A* constraint with *EVERYTHING* in var's domain
                violates_everything = True
                for val2 in var_domain:
                    no_violations = True
                    for constraint in csp.constraints_between(var, neighbor):
                        if not constraint.check(val2, val1):
                            no_violations = False
                            break
                    if no_violations:
                        violates_everything = False
                        break
                if violates_everything:
                    csp.eliminate(neighbor, val1)
                    #if you reduce the neighbor's domain, add the neighbor to the queue 
                    # (if it isn't there already)
                    if not neighbor in queue:
                        if len(csp.get_domain(neighbor)) == 1:
                            queue.append(neighbor) 
                    if has_empty_domains(csp):
                        return None
    return to_return

def solve_constraint_propagate_singleton_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through singleton domains.  Same return type as
    solve_constraint_dfs."""
    agenda = [problem]

    extension_count = 0

    while len(agenda) > 0:
        next_problem = agenda.pop(0)
        extension_count += 1
        if has_empty_domains(next_problem) or not check_all_constraints(next_problem):
            #this won't work
            continue
        if len(next_problem.unassigned_vars) == 0:
            return (next_problem.assigned_values, extension_count)

        new_var = next_problem.pop_next_unassigned_var()

        i = 0
        for val in next_problem.get_domain(new_var):
            new_prob = next_problem.copy().set_assigned_value(new_var, val)
            domain_reduction_singleton_domains(new_prob, [new_var])
            agenda.insert(i, new_prob)
            i += 1
    return (None, extension_count)

# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with propagation through singleton domains? (Don't use domain reduction
#    before solving it.)


# prob = get_pokemon_problem()
# solve_constraint_propagate_singleton_domains(prob)


ANSWER_4 = 8


#### PART 5: FORWARD CHECKING

def propagate(enqueue_condition_fn, csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced.  Same return type as domain_reduction."""

    if queue == None:
        queue = csp.get_all_variables()

    to_return = []
    while len(queue) > 0:
        var = queue.pop(0)
        var_domain = csp.get_domain(var)

        to_return.append(var)

        for neighbor in csp.get_neighbors(var):
            #if this neighbor has values that are incompatible with the constraints between
            # var and n, remove incompatible values from neighbor's domain

            # most of this was copied from above
            neighbor_domain = csp.get_domain(neighbor)[:]
            for val1 in neighbor_domain:
                # violates *A* constraint with *EVERYTHING* in var's domain
                violates_everything = True
                for val2 in var_domain:
                    no_violations = True
                    for constraint in csp.constraints_between(var, neighbor):
                        if not constraint.check(val2, val1):
                            no_violations = False
                            break
                    if no_violations:
                        violates_everything = False
                        break
                if violates_everything:
                    if csp.get_assigned_value(neighbor) != val1:
                        csp.eliminate(neighbor, val1)
                    #if you reduce the neighbor's domain, add the neighbor to the queue 
                    # (if it isn't there already) 
                    if has_empty_domains(csp):
                        return None
                    if not neighbor in queue:
                        if enqueue_condition_fn(csp, neighbor) and csp.get_assigned_value(neighbor) == None:
                            queue.append(neighbor)
    return to_return

def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    return len(csp.get_domain(var)) == 1

def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### PART 6: GENERIC CSP SOLVER

def solve_constraint_generic(problem, enqueue_condition=None) :
    """Solves the problem, calling propagate with the specified enqueue
    condition (a function).  If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs."""
    agenda = [problem]
    extension_count = 0

    while len(agenda) > 0:
        next_problem = agenda.pop(0)
        extension_count += 1
        if has_empty_domains(next_problem) or not check_all_constraints(next_problem):
            #this won't work
            continue
        if len(next_problem.unassigned_vars) == 0:
            return (next_problem.assigned_values, extension_count)

        new_var = next_problem.pop_next_unassigned_var()

        i = 0
        for val in next_problem.get_domain(new_var):
            new_prob = next_problem.copy().set_assigned_value(new_var, val)
            if enqueue_condition != None:
                propagate(enqueue_condition, new_prob, [new_var])
            agenda.insert(i, new_prob)
            i += 1
    return (None, extension_count)

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking, but no propagation? (Don't use domain
#    reduction before solving it.)

# prob = get_pokemon_problem()
# solve_constraint_generic(prob, condition_forward_checking)

ANSWER_5 = 9


#### PART 7: DEFINING CUSTOM CONSTRAINTS

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    return abs(m-n) == 1

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    return abs(m-n) != 1

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    constraints = []
    for i in range(len(variables)):
        for j in range(i+1, len(variables)):
            constraints.append(Constraint(variables[i], variables[j], constraint_different))
    return constraints


#### PART 8: MOOSE PROBLEM (OPTIONAL)

moose_problem = ConstraintSatisfactionProblem(["You", "Moose", "McCain",
                                               "Palin", "Obama", "Biden"])

# Add domains and constraints to your moose_problem here:


# To test your moose_problem AFTER implementing all the solve_constraint
# methods above, change TEST_MOOSE_PROBLEM to True:
TEST_MOOSE_PROBLEM = False


#### SURVEY ###################################################

NAME = "Grace Yin"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = "3-4?"
WHAT_I_FOUND_INTERESTING = "Pokemon!!! :D"
WHAT_I_FOUND_BORING = "Not much. I liked this lab."
SUGGESTIONS = "The hint below domain_reduction would have been helpful for eliminate_from_neighbors..."


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

if TEST_MOOSE_PROBLEM:
    # These lines are used in the local tester iff TEST_MOOSE_PROBLEM is True
    moose_answer_dfs = solve_constraint_dfs(moose_problem.copy())
    moose_answer_propany = solve_constraint_propagate_reduced_domains(moose_problem.copy())
    moose_answer_prop1 = solve_constraint_propagate_singleton_domains(moose_problem.copy())
    moose_answer_generic_dfs = solve_constraint_generic(moose_problem.copy(), None)
    moose_answer_generic_propany = solve_constraint_generic(moose_problem.copy(), condition_domain_reduction)
    moose_answer_generic_prop1 = solve_constraint_generic(moose_problem.copy(), condition_singleton)
    moose_answer_generic_fc = solve_constraint_generic(moose_problem.copy(), condition_forward_checking)
    moose_instance_for_domain_reduction = moose_problem.copy()
    moose_answer_domain_reduction = domain_reduction(moose_instance_for_domain_reduction)
    moose_instance_for_domain_reduction_singleton = moose_problem.copy()
    moose_answer_domain_reduction_singleton = domain_reduction_singleton_domains(moose_instance_for_domain_reduction_singleton)
