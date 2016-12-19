# MIT 6.034 Lab 7: Support Vector Machines
# Written by Jessica Noss (jmn) and 6.034 staff

from svm_data import *
import math

# Vector math
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

# Equation 1
def positiveness(svm, point):
    "Computes the expression (w dot x + b) for the given point"
    return dot_product(svm.w, point.coords) + svm.b

def classify(svm, point):
    """Uses given SVM to classify a Point.  Assumes that point's true
    classification is unknown.  Returns +1 or -1, or 0 if point is on boundary"""
    p = positiveness(svm, point)
    if p > 0:
        return 1
    elif p < 0:
        return -1
    return 0

# Equation 2
def margin_width(svm):
    "Calculate margin width based on current boundary."
    return 2./norm(svm.w)

# Equation 3
def check_gutter_constraint(svm):
    """Returns the set of training points that violate one or both conditions:
        * gutter constraint (positiveness == classification for support vectors)
        * training points must not be between the gutters
    Assumes that the SVM has support vectors assigned."""
    violations = []
    for point in svm.support_vectors:
        p = positiveness(svm, point)
        if p != point.classification:
            violations.append(point)
    for point in svm.training_points:
        if abs(positiveness(svm, point)) < 1:
            violations.append(point)
    return set(violations)

# Equations 4, 5
def check_alpha_signs(svm):
    """Returns the set of training points that violate either condition:
        * all non-support-vector training points have alpha = 0
        * all support vectors have alpha > 0
    Assumes that the SVM has support vectors assigned, and that all training
    points have alpha values assigned."""
    violations = []
    for point in svm.support_vectors:
        if point.alpha <= 0:
            violations.append(point)
    for point in svm.training_points:
        if point in svm.support_vectors:
            continue
        if point.alpha != 0:
            violations.append(point)
    return set(violations)

def check_alpha_equations(svm):
    """Returns True if both Lagrange-multiplier equations are satisfied,
    otherwise False.  Assumes that the SVM has support vectors assigned, and
    that all training points have alpha values assigned."""
    eq4 = 0
    eq5 = []

    for i in svm.training_points[0]:
        eq5.append(0)

    for point in svm.training_points:
        val = point.classification * point.alpha
        eq4 += val
        eq5 = vector_add(eq5, scalar_mult(val, point.coords))

    if eq4 != 0:
        return False
    if eq5 != svm.w:
        return False

    return True

# Classification accuracy
def misclassified_training_points(svm):
    """Returns the set of training points that are classified incorrectly
    using the current decision boundary."""
    violations = []
    for point in svm.training_points:
        if classify(svm, point) != point.classification:
            violations.append(point)

    return set(violations)

# Training
def update_svm_from_alphas(svm):
    """Given an SVM with training data and alpha values, use alpha values to
    update the SVM's support vectors, w, and b.  Return the updated SVM."""

    svm.support_vectors = []
    minB = 100000000
    maxB = -100000000
    eq5 = []
    for i in svm.training_points[0].coords:
        eq5.append(0)
    for point in svm.training_points:
        val = point.alpha * point.classification
        eq5 = vector_add(eq5, scalar_mult(val, point.coords))
        if point.alpha > 0:
            svm.support_vectors.append(point)

    svm.w = eq5
    for point in svm.support_vectors:
        wx = dot_product(svm.w, point.coords)
        b = point.classification - wx

        if b > maxB and point.alpha > 0 and point.classification == 1:
            maxB = b
        if b < minB and point.alpha > 0 and point.classification == -1:
            minB = b
    svm.b = (minB + maxB)/2.
    return svm

# Multiple choice
ANSWER_1 = 11
ANSWER_2 = 6
ANSWER_3 = 3
ANSWER_4 = 2

ANSWER_5 = ["A", "D"]
ANSWER_6 = ["A", "B", "D"]
ANSWER_7 = ["A", "B", "D"]
ANSWER_8 = []
ANSWER_9 = ["A", "B", "D"]
ANSWER_10 = ["A", "B", "D"]

ANSWER_11 = False
ANSWER_12 = True
ANSWER_13 = False
ANSWER_14 = False
ANSWER_15 = False
ANSWER_16 = True

ANSWER_17 = [1, 3, 6, 8]
ANSWER_18 = [1, 2, 4, 5, 6, 7, 8]
ANSWER_19 = [1, 2, 4, 5, 6, 7, 8]

ANSWER_20 = 6


#### SURVEY ####################################################################

NAME = "Grace Yin"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = "2"
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""
