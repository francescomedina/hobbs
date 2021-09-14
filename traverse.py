import nltk
import queue as Queue
import utils
import match
import traverse


def count_np_nodes(tree):
    """ Function from class to count NP nodes.
    """
    np_count = 0
    if not isinstance(tree, nltk.Tree):
        return 0
    elif "NP" in tree.label() and tree.label() not in utils.nominal_labels:
        return 1 + sum(count_np_nodes(c) for c in tree)
    else:
        return sum(count_np_nodes(c) for c in tree)


def bft(tree):
    """ Perform a breadth-first traversal of a tree.
    Return the nodes in a list in level-order.

    Args:
        tree: a tree node
    Returns:
        lst: a list of tree nodes in left-to-right level-order
    """
    lst = []
    queue = Queue.Queue()
    queue.put(tree)
    while not queue.empty():
        node = queue.get()
        lst.append(node)
        for child in node:
            if isinstance(child, nltk.Tree):
                queue.put(child)
    return lst


def check_for_intervening_np(tree, pos, proposal, pro):
    """ Check if subtree rooted at pos contains at least
    three NPs, one of which is:
        (i)   not the proposal,
        (ii)  not the pronoun, and
        (iii) greater than the proposal

    Args:
        tree: the tree being searched
        pos: the position of the root subtree being searched
        proposal: the position of the proposed NP antecedent
        pro: the pronoun being resolved (string)
    Returns:
        True if there is an NP between the proposal and the  pronoun
        False otherwise
    """
    bf = bft(tree[pos])
    bf_pos = [utils.get_pos(tree, node) for node in bf]

    if count_np_nodes(tree[pos]) >= 3:
        for node_pos in bf_pos:
            if "NP" in tree[node_pos].label() \
                    and tree[node_pos].label() not in utils.nominal_labels:
                if node_pos != proposal and node_pos != utils.get_pos(tree, pro):
                    if node_pos < proposal:
                        return True
    return False


def traverse_left(tree, pos, path, pro, check=1):
    """ Traverse all branches below pos to the left of path in a
    left-to-right, breadth-first fashion. Returns the first potential
    antecedent found.

    If check is set to 1, propose as an antecedent any NP node
    that is encountered which has an NP or S node between it and pos.

    If check is set to 0, propose any NP node encountered as the antecedent.

    Args:
        tree: the tree being searched
        pos: the position of the root of the subtree being searched
        path: the path taked to get to pos
        pro: the pronoun being resolved (string)
        check: whether or not there must be an intervening NP
    Returns:
        tree: the tree containing the antecedent
        p: the position of the proposed antecedent
    """
    # get the results of breadth first search of the subtree
    # iterate over them
    breadth_first = bft(tree[pos])

    # convert the treepositions of the subtree rooted at pos
    # to their equivalents in the whole tree
    bf_pos = [utils.get_pos(tree, node) for node in breadth_first]

    if check == 1:
        for p in bf_pos:
            if p < path[0] and p not in path:
                if "NP" in tree[p].label() and match.match(tree, p, pro):
                    if traverse.check_for_intervening_np(tree, pos, p, pro):
                        return tree, p

    elif check == 0:
        for p in bf_pos:
            if p < path[0] and p not in path:
                if "NP" in tree[p].label() and match.match(tree, p, pro):
                    return tree, p

    return None, None


def traverse_right(tree, pos, path, pro):
    """ Traverse all the branches of pos to the right of path p in a
    left-to-right, breadth-first manner, but do not go below any NP
    or S node encountered. Propose any NP node encountered as the
    antecedent. Returns the first potential antecedent.

    Args:
        tree: the tree being searched
        pos: the position of the root of the subtree being searched
        path: the path taken to get to pos
        pro: the pronoun being resolved (string)
    Returns:
        tree: the tree containing the antecedent
        p: the position of the antecedent
    """
    breadth_first = bft(tree[pos])
    bf_pos = [utils.get_pos(tree, node) for node in breadth_first]

    for p in bf_pos:
        if p > path[0] and p not in path:
            if "NP" in tree[p].label() or tree[p].label() == "S":
                if "NP" in tree[p].label() and tree[p].label() not in utils.nominal_labels:
                    if match.match(tree, p, pro):
                        return tree, p
                return None, None


def traverse_tree(tree, pro):
    """ Traverse a tree in a left-to-right, breadth-first manner,
    proposing any NP encountered as an antecedent. Returns the
    tree and the position of the first possible antecedent.

    Args:
        tree: the tree being searched
        pro: the pronoun being resolved (string)
    """
    # Initialize a queue and enqueue the root of the tree
    queue = Queue.Queue()
    queue.put(tree)
    while not queue.empty():
        node = queue.get()
        # if the node is an NP, return it as a potential antecedent
        if "NP" in node.label() and match.match(tree, utils.get_pos(tree, node), pro):
            return tree, utils.get_pos(tree, node)
        for child in node:
            if isinstance(child, nltk.Tree):
                queue.put(child)
    # if no antecedent is found, return None
    return None, None
