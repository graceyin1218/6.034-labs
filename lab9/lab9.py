# MIT 6.034 Lab 9: Boosting (Adaboost)
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and 6.034 staff

from math import log as ln
from utils import *


#### BOOSTING (ADABOOST) #######################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""
    N = len(training_points)
    ans = {}
    for p in training_points:
        ans[p] = make_fraction(1, N)
    return ans

def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""
    ans = {}
    for c in classifier_to_misclassified:
        misclassified = classifier_to_misclassified[c]
        ans[c] = 0
        for p in misclassified:
            ans[c] += point_to_weight[p]
    return ans

def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier, or raises NoGoodClassifiersError if best* classifier has
    error rate 1/2.  best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""
    best_classifier = None
    if use_smallest_error:
      best_classifier = min(classifier_to_error_rate, key=classifier_to_error_rate.get)
    else:
      best_classifier = max(classifier_to_error_rate, key=lambda x : abs(classifier_to_error_rate[x]-0.5))

    if make_fraction(classifier_to_error_rate[best_classifier]) == make_fraction(1,2):
        raise NoGoodClassifiersError

    #find a classifier that comes before this one alphabetically
    for c in classifier_to_error_rate:
        if use_smallest_error and classifier_to_error_rate[c] == classifier_to_error_rate[best_classifier]:
            if c < best_classifier:
                best_classifier = c
        if not use_smallest_error:
            error = make_fraction(abs(classifier_to_error_rate[best_classifier] - 0.5))
            check_error = make_fraction(abs(classifier_to_error_rate[c] -0.5))
            if error == check_error:
                if c < best_classifier:
                    best_classifier = c
    return best_classifier

def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""
    if error_rate == 0:
        return INF
    if error_rate == 1:
        return -INF
    return 0.5*ln(make_fraction(1-error_rate, error_rate))

def get_overall_misclassifications(H, training_points, classifier_to_misclassified):
    """Given an overall classifier H, a list of all training points, and a
    dictionary mapping classifiers to the training points they misclassify,
    returns a set containing the training points that H misclassifies.
    H is represented as a list of (classifier, voting_power) tuples."""
    misclassified = []

    for p in training_points:
        score = 0
        for tup in H:
            c = tup[0]
            voting_power = tup[1]
            if p in classifier_to_misclassified[c]:
                score -= voting_power
            else:
                score += voting_power
        if score <= 0:
            misclassified.append(p)
    return set(misclassified)

def is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance=0):
    """Given an overall classifier H, a list of all training points, a
    dictionary mapping classifiers to the training points they misclassify, and
    a mistake tolerance (the maximum number of allowed misclassifications),
    returns False if H misclassifies more points than the tolerance allows,
    otherwise True.  H is represented as a list of (classifier, voting_power)
    tuples."""
    misclassified = get_overall_misclassifications(H, training_points, classifier_to_misclassified)
    if len(misclassified) > mistake_tolerance:
        return False
    return True

def update_weights(point_to_weight, misclassified_points, error_rate):
    """Given a dictionary mapping training points to their old weights, a list
    of training points misclassified by the current weak classifier, and the
    error rate of the current weak classifier, returns a dictionary mapping
    training points to their new weights.  This function is allowed (but not
    required) to modify the input dictionary point_to_weight."""
    for p in point_to_weight:
        if p in misclassified_points:
            point_to_weight[p] *= make_fraction(1,2)*make_fraction(1, error_rate)
        else:
            point_to_weight[p] *= make_fraction(1,2)*make_fraction(1, 1-error_rate)
    return point_to_weight

def adaboost(training_points, classifier_to_misclassified,
             use_smallest_error=True, mistake_tolerance=0, max_rounds=INF):
    """Performs the Adaboost algorithm for up to max_rounds rounds.
    Returns the resulting overall classifier H, represented as a list of
    (classifier, voting_power) tuples."""
    point_to_weight = initialize_weights(training_points)
    H = [] # (classifier, voting_power)

    while True:
        # exit conditions
        if is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance):
            break
        if max_rounds == 0:
            break
        classifier_to_error_rate = calculate_error_rates(point_to_weight, classifier_to_misclassified)
        best_classifier = None
        try:
            best_classifier = pick_best_classifier(classifier_to_error_rate, use_smallest_error)
        except NoGoodClassifiersError:
            break

        max_rounds -= 1
        error_rate = classifier_to_error_rate[best_classifier]

        H.append((best_classifier, calculate_voting_power(error_rate)))

        point_to_weight = update_weights(point_to_weight, classifier_to_misclassified[best_classifier], error_rate)
    return H


#### SURVEY ####################################################################

NAME = "Grace Yin"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = "2"
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = "I think I'm going to miss these labs :( "
