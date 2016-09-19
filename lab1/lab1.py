# MIT 6.034 Lab 1: Rule-Based Systems
# Written by 6.034 staff

from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain
from data import *

#### Part 1: Multiple Choice #########################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '2'

ANSWER_4 = '0'

ANSWER_5 = '3'

ANSWER_6 = '1'

ANSWER_7 = '0'

#### Part 2: Transitive Rule #########################################

transitive_rule = IF( AND('(?x) beats (?y)', '(?y) beats (?z)'), THEN('(?x) beats (?z)') )

# You can test your rule by uncommenting these print statements:
#print forward_chain([transitive_rule], abc_data)
#print forward_chain([transitive_rule], poker_data)
#print forward_chain([transitive_rule], minecraft_data)


#### Part 3: Family Relations #########################################

# Define your rules here:

self = IF( 'person (?x)', THEN('self (?x) (?x)'))
sibling = IF( AND('parent (?x) (?y)', 'parent (?x) (?z)', NOT('self (?y) (?z)')), THEN('sibling (?y) (?z)', 'sibling (?z) (?y)'))
child = IF( 'parent (?x) (?y)', THEN ('child (?y) (?x)'))
grandparent_grandchild = IF( AND( 'parent (?x) (?y)', 'parent (?y) (?z)'), THEN ('grandparent (?x) (?z)', 'grandchild (?z) (?x)'))
cousin = IF (AND ('parent (?x) (?y)', 'parent (?a) (?b)', 'sibling (?x) (?a)', NOT ('sibling (?y) (?b)')), THEN ('cousin (?y) (?b)', 'cousin (?b) (?y)') )


# Add your rules to this list:
family_rules = [
    self,
    sibling,
    child,
    grandparent_grandchild,
    cousin
]

# Uncomment this to test your data on the Simpsons family:
#print forward_chain(family_rules, simpsons_data, verbose=False)

# These smaller datasets might be helpful for debugging:
#print forward_chain(family_rules, sibling_test_data, verbose=True)
#print forward_chain(family_rules, grandparent_test_data, verbose=True)

# The following should generate 14 cousin relationships, representing 7 pairs
# of people who are cousins:
black_family_cousins = [
    relation for relation in
    forward_chain(family_rules, black_data, verbose=False)
    if "cousin" in relation ]

# To see if you found them all, uncomment this line:
#print black_family_cousins


#### Part 4: Backward Chaining #########################################

# Import additional methods for backchaining
from production import PASS, FAIL, match, populate, simplify, variables

def backchain_to_goal_tree(rules, hypothesis):
    """
    Takes a hypothesis (string) and a list of rules (list
    of IF objects), returning an AND/OR tree representing the
    backchain of possible statements we may need to test
    to determine if this hypothesis is reachable or not.

    This method should return an AND/OR tree, that is, an
    AND or OR object, whose constituents are the subgoals that
    need to be tested. The leaves of this tree should be strings
    (possibly with unbound variables), *not* AND or OR objects.
    Make sure to use simplify(...) to flatten trees where appropriate.
    """

    toReturnTrees = []
    matches = False
    for rule in rules:
        print(rule)
        for consequent in rule.consequent():
            variables = match(consequent, hypothesis)

            if variables == None:
                continue

            if variables == {}:
                continue

            matches = True

            # the thing you have to prove is true,
            # in order to prove your hypothesis is true
            antecedent = populate(rule.antecedent(), variables)

            # the subtree you will return
            tree = None

            if isinstance(antecedent, str):
                tree = backchain_to_goal_tree(rules, antecedent)
            elif isinstance(antecedent, AND):
                tree = AND([simplify(backchain_to_goal_tree(rules, clause)) for clause in antecedent])
            elif isinstance(antecedent, OR):
                tree = OR([simplify(backchain_to_goal_tree(rules, clause)) for clause in antecedent])
            tree = simplify(tree)

            # print(tree)
            # print()

            toReturnTrees.append(tree)

    if not matches:
        return hypothesis
    return simplify(OR([toReturnTrees]))

    """
    ans = AND()
    matches = False
    for rule in rules:
        for consequent in rule.consequent():
            # get variables that could make the hypothesis work
            print(consequent, " " , hypothesis)
            variables = match(consequent, hypothesis)
            
            # if variables 
            if variables == None:
                continue
            if variables == {}:
                continue

            matches = True

            newHypothesis = populate(rule.antecedent(), variables)

            # AND node
            if isinstance(newHypothesis, AND):
                result = AND()
                for element in newHypothesis:
                    res = backchain_to_goal_tree(rules, newHypothesis)
                    result = AND(res, result)
                ans = simplify(OR(result, ans))

            # OR node
            elif isinstance(newHypothesis, OR):
                result = OR()
                for element in newHypothesis:
                    res = backchain_to_goal_tree(rules, newHypothesis)
                    result = OR(res, result)
                ans = simplify(OR(result, ans))

            # it must be a string
            else:
                ans = simplify(OR(backchain_to_goal_tree(rules, newHypothesis), ans))
    if not matches:
        return hypothesis
    return ans
    """
    



# Uncomment this to run your backward chainer:
print backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin')


#### Survey #########################################

NAME = "Grace Yin"
COLLABORATORAS = "Arezu Esmaili, Aneesh Agrawal"
HOW_MANY_HOURS_THIS_LAB_TOOK = "3"
WHAT_I_FOUND_INTERESTING = "ANDs shouldn't be used in THENs.."
WHAT_I_FOUND_BORING = "Well.. I wanted a poker problem... :("
SUGGESTIONS = "POKER!!"


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!
transitive_rule_poker = forward_chain([transitive_rule], poker_data)
transitive_rule_abc = forward_chain([transitive_rule], abc_data)
transitive_rule_minecraft = forward_chain([transitive_rule], minecraft_data)
family_rules_simpsons = forward_chain(family_rules, simpsons_data)
family_rules_black = forward_chain(family_rules, black_data)
family_rules_sibling = forward_chain(family_rules, sibling_test_data)
family_rules_grandparent = forward_chain(family_rules, grandparent_test_data)
family_rules_anonymous_family = forward_chain(family_rules, anonymous_family_test_data)
