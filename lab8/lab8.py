# MIT 6.034 Lab 8: Bayesian Inference
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from nets import *


#### ANCESTORS, DESCENDANTS, AND NON-DESCENDANTS ###############################

def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    ancestors = []
    queue = list(net.get_parents(var))
    while len(queue) > 0:
        a = queue.pop(len(queue)-1)
        ancestors.append(a)
        l = net.get_parents(a)
        for n in l:
            if n in ancestors:
                continue
            queue.append(n)
    return set(ancestors)

def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    descendants = []
    queue = list(net.get_children(var))
    while len(queue) > 0:
        a = queue.pop(len(queue)-1)
        descendants.append(a)
        l = net.get_children(a)
        for n in l:
            if n in descendants:
                continue
            queue.append(n)
    return set(descendants)

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    nondescendants = net.get_variables()
    nondescendants.remove(var)
    descendants = []
    queue = list(net.get_children(var))
    while len(queue) > 0:
        a = queue.pop(len(queue)-1)
        descendants.append(a)
        nondescendants.remove(a)
        l = net.get_children(a)
        for n in l:
            if n in descendants:
                continue
            queue.append(n)
    return set(nondescendants)

def simplify_givens(net, var, givens):
    """If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens."""
    parents = net.get_parents(var)
    descendants = get_descendants(net, var)
    count_parents = 0
    for g in givens:
        if g in parents:
            count_parents += 1
        elif g in descendants:
            return givens
    if count_parents == len(parents):
        new_dict = {}
        for g in givens:
            if g in parents:
                new_dict[g] = givens[g]
        return new_dict
    return givens


#### PROBABILITY ###############################################################

def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"
    try:
      if givens == None:
          return net.get_probability(hypothesis)
      key = None
      for k in hypothesis:
          key = k
      simplified_givens = simplify_givens(net, key, givens)
      return net.get_probability(hypothesis, simplified_givens)
    except ValueError:
      raise LookupError

def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    ans = 1
    new_givens = hypothesis
    topo = net.topological_sort()
    topo.reverse()
    for var in topo:
        if var in hypothesis:
            new_hypothesis = {}
            new_hypothesis[var] = hypothesis[var]
            new_givens.pop(var)
            ans *= probability_lookup(net, new_hypothesis, new_givens)
    return ans

def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"
    variables = net.get_variables()
    ans = 0

    for k in hypothesis:
        variables.remove(k)

    combinations = net.combinations(variables)

    for c in combinations:
        ans += probability_joint(net, dict(c, **hypothesis))

    return ans

def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"
    if givens == None:
        return probability_marginal(net, hypothesis)
    # check for conflicts in hypothesis and givens

    for k in hypothesis:
        if k in givens:
            if hypothesis[k] != givens[k]:
                return 0.0
    return probability_marginal(net, dict(givens, **hypothesis))/probability_marginal(net, givens)

def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    if givens == None:
        return probability_marginal(net, hypothesis)
    return probability_conditional(net, hypothesis, givens)


#### PARAMETER-COUNTING AND INDEPENDENCE #######################################

def number_of_parameters(net):
    "Computes minimum number of parameters required for net"

    variables = net.get_variables()
    ans = 0
    for v in variables:
        parents = net.get_parents(v)
        temp = 1
        for p in parents:
            temp *= len(net.get_domain(p))
        ans += (len(net.get_domain(v))-1)*temp
    return ans


def is_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    otherwise False.  Uses numerical independence."""
    if givens == None:
        givens = {}
    for v1 in net.get_domain(var1):
        hypothesis = {var1:v1}
        for v2 in net.get_domain(var2):
            new_given = dict(givens, **{var2:v2})
            if not approx_equal(probability_conditional(net, hypothesis, givens),probability_conditional(net, hypothesis, new_given)):
                return False
    return True

def is_structurally_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence)."""

    if var1 == var2:
        return False

    #make ancestral graph
    variables = [var1, var2]
    variables.extend(net.get_parents(var1))
    variables.extend(net.get_parents(var2))
    if givens == None:
        givens = {}
    for g in givens:
        variables.append(g)
        variables.extend(net.get_parents(g))
    ag = net.subnet(variables)

    avariables = ag.get_variables()
    new_ag = ag.copy()
    for x in avariables:
        xchildren = ag.get_children(x)
        for y in avariables:
            ychildren = ag.get_children(y)
            if len(xchildren.intersection(ychildren)) > 0:
                new_ag = new_ag.link(x, y)

    ag = new_ag.make_bidirectional()

    for g in givens:
        ag = ag.remove_variable(g)

    if var1 not in ag.get_variables() or var2 not in ag.get_variables():
        return True
    if ag.find_path(var1, var2) == None:
        return True
    return False


#### SURVEY ####################################################################

NAME = "Grace Yin"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = "3"
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = None
