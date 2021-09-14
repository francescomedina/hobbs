# Labels for nominal heads
nominal_labels = ["NN", "NNS", "NNP", "NNPS", "PRP"]

p = ["He", "he", "Him", "him", "She", "she", "Her", "her", "It", "it", "They", "they"]
r = ["Himself", "himself", "Herself", "herself", "Itself", "itself", "Themselves", "themselves"]


def get_pos(tree, node):
    """ Given a tree and a node, return the tree position
    of the node.
    """
    for pos in tree.treepositions():
        if tree[pos] == node:
            return pos


def get_dom_np(sents, pos):
    """ Finds the position of the NP that immediately dominates
    the pronoun.

    Args:
        sents: list of trees (or tree) to search
        pos: the tree position of the pronoun to be resolved
    Returns:
        tree: the tree containing the pronoun
        dom_pos: the position of the NP immediately dominating
            the pronoun
    """
    # start with the last tree in sents
    tree = sents[-1]
    # get the NP's position by removing the last element from
    # the pronoun's
    dom_pos = pos[:-1]
    return tree, dom_pos