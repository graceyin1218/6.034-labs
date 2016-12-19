# MIT 6.034 Lab 6: Neural Nets
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), Jake Barnwell (jb16), and 6.034 staff

from nn_problems import *
from math import e
INF = float('inf')

#### NEURAL NETS ###############################################################

# Wiring a neural net

nn_half = [1]

nn_angle = [2,1]

nn_cross = [2,2,1]

nn_stripe = [3,1]

nn_hexagon = [6,1]

nn_grid = [4,2,1]

# Threshold functions
def stairstep(x, threshold=0):
    "Computes stairstep(x) using the given threshold (T)"
    if x >= threshold:
        return 1
    return 0

def sigmoid(x, steepness=1, midpoint=0):
    "Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
    return 1./(1 + (e)**(-1 * steepness * (x-midpoint)))

def ReLU(x):
    "Computes the threshold of an input using a rectified linear unit."
    return max(0, x)

# Accuracy function
def accuracy(desired_output, actual_output):
    "Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
    return -1./2 * (actual_output - desired_output)**2

# Forward propagation

def node_value(node, input_values, neuron_outputs):  # STAFF PROVIDED
    """Given a node, a dictionary mapping input names to their values, and a
    dictionary mapping neuron names to their outputs, returns the output value
    of the node."""
    if isinstance(node, basestring):
        return input_values[node] if node in input_values else neuron_outputs[node]
    return node  # constant input, such as -1

def forward_prop(net, input_values, threshold_fn=stairstep):
    """Given a neural net and dictionary of input values, performs forward
    propagation with the given threshold function to compute binary output.
    This function should not modify the input net.  Returns a tuple containing:
    (1) the final output of the neural net
    (2) a dictionary mapping neurons to their immediate outputs"""

    # use net.topological_sort() to get nodes in order
    # use net.get_incoming_neighbors(node) to get inputs
      # use net.get_wires(start, end) to get wires/weights
    # use node_value(node, input_values, neuron_outputs) to get output of node
    # store outputs of each neuron

    topo_sort = net.topological_sort()

    neuron_outputs = {}

    ans = None

    for node in topo_sort:

        # calculate node output

        inputs = net.get_incoming_neighbors(node)
        out = 0
        for i in inputs:
            out += net.get_wires(i,node)[0].get_weight() * node_value(i,input_values,neuron_outputs)

        out = threshold_fn(out)
        neuron_outputs[node] = out
        if net.is_output_neuron(node):
            ans = out

    return (ans, neuron_outputs)


# Backward propagation warm-up
def gradient_ascent_step(func, inputs, step_size):
    """Given an unknown function of three variables and a list of three values
    representing the current inputs into the function, increments each variable
    by +/- step_size or 0, with the goal of maximizing the function output.
    After trying all possible variable assignments, returns a tuple containing:
    (1) the maximum function output found, and
    (2) the list of inputs that yielded the highest function output."""
    options = [step_size, -1*step_size, 0]
    best_var_assignments = None
    best_output = -1 * INF

    for i in options:
        for j in options:
              for k in options:
                  x = inputs[0] + i
                  y = inputs[1] + j
                  z = inputs[2] + k
                  out = func(x, y, z)
                  if out > best_output:
                      best_output = out
                      best_var_assignments = [x, y, z]
    return (best_output, best_var_assignments)

def get_back_prop_dependencies(net, wire):
    """Given a wire in a neural network, returns a set of inputs, neurons, and
    Wires whose outputs/values are required to update this wire's weight."""
    res = []
    # get output of node A and output of node B
    res.append(wire.startNode)
    res.append(wire.endNode)

    # get current weight of the wird
    res.append(wire)

    # get all neurons and weights downstream to final layer
    queue = [wire.endNode] # contains the last nodes we've visited along that branch
    visited = []
    while len(queue) > 0:
        last_visited = queue.pop()
        if last_visited in visited:
            continue
        visited.append(last_visited)
        for node in net.get_outgoing_neighbors(last_visited):
            res.append(node)
            for wire in net.get_wires(last_visited, node):
                res.append(wire)
            if not net.is_output_neuron(node):
                queue.append(node)

    return set(res)

# Backward propagation
def calculate_deltas(net, desired_output, neuron_outputs):
    """Given a neural net and a dictionary of neuron outputs from forward-
    propagation, computes the update coefficient (delta_B) for each
    neuron in the net. Uses the sigmoid function to compute neuron output.
    Returns a dictionary mapping neuron names to update coefficient (the
    delta_B values). """
    deltas = {}
    topo = net.topological_sort()

    out = topo.pop()

    output = neuron_outputs[out]

    deltas[out] = output * (1. - output) * (desired_output - output)

    while len(topo) > 0:
        node = topo.pop()
        deltas[node] = neuron_outputs[node] * (1. - neuron_outputs[node])
        neighbors = net.get_outgoing_neighbors(node)

        s = 0

        for n in neighbors:
            wire = net.get_wires(node, n)[0]
            s += wire.get_weight() * deltas[n]
        deltas[node] *= s

    return deltas

def update_weights(net, input_values, desired_output, neuron_outputs, r=1):
    """Performs a single step of back-propagation.  Computes delta_B values and
    weight updates for entire neural net, then updates all weights.  Uses the
    sigmoid function to compute neuron output.  Returns the modified neural net,
    with the updated weights."""

    deltas = calculate_deltas(net, desired_output, neuron_outputs)

    wires = net.get_wires()
    for wire in wires:
        new_weight = wire.get_weight()
        new_weight += r * node_value(wire.startNode, input_values, neuron_outputs) * deltas[wire.endNode]
        wire.set_weight(new_weight)
    return net


def back_prop(net, input_values, desired_output, r=1, minimum_accuracy=-0.001):
    """Updates weights until accuracy surpasses minimum_accuracy.  Uses the
    sigmoid function to compute neuron output.  Returns a tuple containing:
    (1) the modified neural net, with trained weights
    (2) the number of iterations (that is, the number of weight updates)"""

    count = 0
    (output, neuron_outputs) = forward_prop(net, input_values, sigmoid)
    a = accuracy(desired_output, output)
    while a <= minimum_accuracy:
        net = update_weights(net, input_values, desired_output, neuron_outputs, r)
        count += 1

        (output, neuron_outputs) = forward_prop(net, input_values, sigmoid)
        a = accuracy(desired_output, output)
    return (net, count)

# Training a neural net

ANSWER_1 = 11
ANSWER_2 = 11
ANSWER_3 = 2
ANSWER_4 = 200
ANSWER_5 = 10

ANSWER_6 = 1
ANSWER_7 = "checkerboard"
ANSWER_8 = ["small", "medium", "large"]
ANSWER_9 = "B"

ANSWER_10 = "D"
ANSWER_11 = ["A","C"]
ANSWER_12 = ["A","E"]


#### SURVEY ####################################################################

NAME = "Grace Yin"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 5
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""
