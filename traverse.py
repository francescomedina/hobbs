import nltk
import queue as Queue
import utils
import match


def count_np_nodes(tree):
    if not isinstance(tree, nltk.Tree):
        return 0
    elif "NP" in tree.label() and tree.label() not in utils.nominal_labels:
        return 1 + sum(count_np_nodes(c) for c in tree)
    else:
        return sum(count_np_nodes(c) for c in tree)


# Here it is implemented a Breath First Search of the tree and it returns a list of the nodes in left to right level order.
def bft(tree):
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
                    if check_for_intervening_np(tree, pos, p, pro):
                        return tree, p

    elif check == 0:
        for p in bf_pos:
            if p < path[0] and p not in path:
                if "NP" in tree[p].label() and match.match(tree, p, pro):
                    return tree, p

    return None, None


def traverse_right(tree, pos, path, pro):
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
