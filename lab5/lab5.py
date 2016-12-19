# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and Jake Barnwell (jb16)

from api import *
from data import *
import math
log2 = lambda x: math.log(x, 2)
INF = float('inf')

################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################

def id_tree_classify_point(point, id_tree):
    """Uses the input ID tree (an IdentificationTreeNode) to classify the point.
    Returns the point's classification."""
    if id_tree.is_leaf():
        return id_tree.get_node_classification()
    return id_tree_classify_point(point, id_tree.apply_classifier(point))

def split_on_classifier(data, classifier):
    """Given a set of data (as a list of points) and a Classifier object, uses
    the classifier to partition the data.  Returns a dict mapping each feature
    values to a list of points that have that value."""
    ans = {}
    for d in data:
        key = classifier.classify(d)
        if key in ans:
            ans[key].append(d)
        else:
            ans[key] = [d]
    return ans


#### CALCULATING DISORDER

def branch_disorder(data, target_classifier):
    """Given a list of points representing a single branch and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the branch."""
    categories = {}
    total = len(data)
    for d in data:
        key = target_classifier.classify(d)
        if key in categories:
            categories[key] += 1
        else:
            categories[key] = 1
    ans = 0
    for key in categories:
        frac = (1.0 * categories[key]) / total
        ans -= frac * log2(frac)
    return ans



def average_test_disorder(data, test_classifier, target_classifier):
    """Given a list of points, a feature-test Classifier, and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the feature-test stump."""

    branches = {}
    total = len(data)
    for d in data:
        key = test_classifier.classify(d)
        if key in branches:
            branches[key].append(d)
        else:
            branches[key] = [d]
    ans = 0
    for key in branches:
        weight = float(len(branches[key])) / total
        ans += weight * branch_disorder(branches[key], target_classifier)
    return ans



## To use your functions to solve part A2 of the "Identification of Trees"
## problem from 2014 Q2, uncomment the lines below and run lab5.py:
#for classifier in tree_classifiers:
#    print classifier.name, average_test_disorder(tree_data, classifier, feature_test("tree_type"))


#### CONSTRUCTING AN ID TREE

def find_best_classifier(data, possible_classifiers, target_classifier):
    """Given a list of points, a list of possible Classifiers to use as tests,
    and a Classifier for determining the true classification of each point,
    finds and returns the classifier with the lowest disorder.  Breaks ties by
    preferring classifiers that appear earlier in the list.  If the best
    classifier has only one branch, raises NoGoodClassifiersError."""

    classifiers = []
    for c in possible_classifiers:
        disorder = average_test_disorder(data, c, target_classifier)
        classifiers.append((c, disorder))
    classifiers = sorted(classifiers, key = lambda x: x[1])

    best_classifier = classifiers[0][0]
    data_classifications = {}
    for d in data:
        key = best_classifier.classify(d)
        if key in data_classifications:
            continue
        data_classifications[key] = True
    if len(data_classifications) == 1:
        raise NoGoodClassifiersError
    return classifiers[0][0]


## To find the best classifier from 2014 Q2, Part A, uncomment:
#print find_best_classifier(tree_data, tree_classifiers, feature_test("tree_type"))


def construct_greedy_id_tree(data, possible_classifiers, target_classifier, id_tree_node=None):
    """Given a list of points, a list of possible Classifiers to use as tests,
    a Classifier for determining the true classification of each point, and
    optionally a partially completed ID tree, returns a completed ID tree by
    adding classifiers and classifications until either perfect classification
    has been achieved, or there are no good classifiers left."""
    if id_tree_node == None:
        id_tree_node = IdentificationTreeNode(target_classifier)

    # if the node is homogeneous then it should be a leaf node, so add the classification to the node
    # recurse
    homogeneous = True
    prev = None
    for d in data:
        if prev == None:
            prev = d[target_classifier.name]
        if d[target_classifier.name] != prev:
            homogeneous = False
            break
    if homogeneous:
        id_tree_node.set_node_classification(target_classifier.classify(data[0]))
        return id_tree_node


    # if the node is not homogeneous and the data can be difided further, add the best classifier to the node
    # recurse
    try :
        best_classifier = find_best_classifier(data, possible_classifiers, target_classifier)

        partitions = split_on_classifier(data, best_classifier)

        id_tree_node.set_classifier_and_expand(best_classifier, partitions)
        subtrees = id_tree_node.get_branches()

        possible_classifiers.remove(best_classifier)

        for branch in subtrees:
            construct_greedy_id_tree(partitions[branch], possible_classifiers, target_classifier, subtrees[branch])
    # if the node is not homogeneous but there are no good classifiers left (i.e. no classifiers with more than one branch)
    # leave the node's classification unassigned.
    except NoGoodClassifiersError :
        id_tree_node.set_node_classification(None)

    return id_tree_node


## To construct an ID tree for 2014 Q2, Part A:
#print construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))

## To use your ID tree to identify a mystery tree (2014 Q2, Part A4):
#tree_tree = construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))
#print id_tree_classify_point(tree_test_point, tree_tree)

## To construct an ID tree for 2012 Q2 (Angels) or 2013 Q3 (numeric ID trees):
#print construct_greedy_id_tree(angel_data, angel_classifiers, feature_test("Classification"))
#print construct_greedy_id_tree(numeric_data, numeric_classifiers, feature_test("class"))


#### MULTIPLE CHOICE

ANSWER_1 = "bark_texture"
ANSWER_2 = "leaf_shape"
ANSWER_3 = "orange_foliage"

ANSWER_4 = [2,3]
ANSWER_5 = [3]
ANSWER_6 = [2]
ANSWER_7 = 2

ANSWER_8 = "No"
ANSWER_9 = "No"


################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

#### MULTIPLE CHOICE: DRAWING BOUNDARIES

BOUNDARY_ANS_1 = 3

BOUNDARY_ANS_2 = 4

BOUNDARY_ANS_3 = 1
BOUNDARY_ANS_4 = 2

BOUNDARY_ANS_5 = 2
BOUNDARY_ANS_6 = 4
BOUNDARY_ANS_7 = 1
BOUNDARY_ANS_8 = 4
BOUNDARY_ANS_9 = 4


BOUNDARY_ANS_10 = 4
BOUNDARY_ANS_11 = 2    
BOUNDARY_ANS_12 = 1
BOUNDARY_ANS_13 = 4
BOUNDARY_ANS_14 = 4


#### WARM-UP: DISTANCE METRICS

def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    ans = 0
    for i in range(len(u)):
        ans += u[i] * v[i]
    return ans

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    return math.sqrt(dot_product(v, v))


def euclidean_distance(point1, point2):
    "Given two Points, computes and returns the Euclidean distance between them."
    v = []
    for i in range(len(point1.coords)):
        v.append(point1.coords[i] - point2.coords[i])
    return norm(v)

def manhattan_distance(point1, point2):
    "Given two Points, computes and returns the Manhattan distance between them."
    ans = 0
    for i in range(len(point1.coords)):
        ans += abs(point1.coords[i] - point2.coords[i])
    return ans

def hamming_distance(point1, point2):
    "Given two Points, computes and returns the Hamming distance between them."
    ans = 0
    for i in range(len(point1.coords)):
        if point1.coords[i] != point2.coords[i]:
            ans += 1
    return ans


def cosine_distance(point1, point2):
    """Given two Points, computes and returns the cosine distance between them,
    where cosine distance is defined as 1-cos(angle_between(point1, point2))."""
    v = point1.coords
    u = point2.coords
    return 1. - dot_product(u, v) / (norm(v) * norm(u))


#### CLASSIFYING POINTS

def get_k_closest_points(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns a list containing the k points
    from the data that are closest to the test point, according to the distance
    metric.  Breaks ties lexicographically by coordinates."""
    distances = []
    for d in data:
        distances.append((d, distance_metric(point, d)))
    distances = map(lambda x : x[0], sorted(sorted(distances, key=lambda x: x[0].coords), key = lambda x: x[1]))
    return distances[:k]


def knn_classify_point(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns the classification of the test
    point based on its k nearest neighbors, as determined by the distance metric.
    Assumes there are no ties."""
    closest = map(lambda point: point.classification, get_k_closest_points(point, data, k, distance_metric))
    distinct_points = set(closest)
    mode = None
    mode_count = 0
    for p in distinct_points:
        if closest.count(p) > mode_count:
            mode_count = closest.count(p)
            mode = p
    return mode




## To run your classify function on the k-nearest neighbors problem from 2014 Q2
## part B2, uncomment the line below and try different values of k:
#print knn_classify_point(knn_tree_test_point, knn_tree_data, 5, euclidean_distance)


#### CHOOSING k

def cross_validate(data, k, distance_metric):
    """Given a list of points (the data), an int 0 < k <= len(data), and a
    distance metric (a function), performs leave-one-out cross-validation.
    Return the fraction of points classified correctly, as a float."""

    correct = 0

    for i in range(len(data)):
        d = data[i]
        data.pop(i)
        classification = knn_classify_point(d, data, k, distance_metric)
        if classification == d.classification:
            correct += 1
        data.insert(i, d)

    return float(correct)/len(data)


def find_best_k_and_metric(data):
    """Given a list of points (the data), uses leave-one-out cross-validation to
    determine the best value of k and distance_metric, choosing from among the
    four distance metrics defined above.  Returns a tuple (k, distance_metric),
    where k is an int and distance_metric is a function."""

    metrics = [euclidean_distance, manhattan_distance, hamming_distance, cosine_distance]
    best_score = 0
    best_k = None
    best_metric = None
    for k in range(len(data)):
        for distance_metric in metrics:
            score = cross_validate(data, k, distance_metric)
            if score > best_score:
                best_k = k
                best_metric = distance_metric
                best_score = score
    return (best_k, best_metric)


## To find the best k and distance metric for 2014 Q2, part B, uncomment:
#print find_best_k_and_metric(knn_tree_data)


#### MORE MULTIPLE CHOICE

kNN_ANSWER_1 = "Overfitting"
kNN_ANSWER_2 = "Underfitting"
kNN_ANSWER_3 = 4

kNN_ANSWER_4 = 4
kNN_ANSWER_5 = 1
kNN_ANSWER_6 = 3
kNN_ANSWER_7 = 3

#### SURVEY ###################################################

NAME = "Grace Yin"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 5
WHAT_I_FOUND_INTERESTING = "Too tired to figure out what exactly was interesting..... but I guess I must have found this lab interesting enough to bash it all out this weekend... :D "
WHAT_I_FOUND_BORING = "Writing euclidian_distance, manhattan_distance, etc was a bit tedious... and reminded me of 6.006 :( :( :(  (document distance...)"
SUGGESTIONS = "Maybe for knn_classify_point, state explicitly that you want us to classify a point based on the most common classification in the list of k points? It took me a while to figure out how exactly you wanted us to classify a point...   Also, this probably sounds really silly, but could you guys make the psets themed too? Like, creating ID trees for Pokemon or something? (Oak/maple trees aren't that exciting... vampires aren't bad... but yeah. Pokemon. :D ) "
