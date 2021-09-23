from nltk import Tree

# Labels for nominal heads
nominal_labels = ["NN", "NNS", "NNP", "NNPS", "PRP"]

p = ["He", "he", "Him", "him", "She", "she", "Her", "her", "It", "it", "They", "they"]
r = ["Himself", "himself", "Herself", "herself", "Itself", "itself", "Themselves", "themselves"]


def read_from_file(file_name):
    if file_name and file_name != "":
        with open(file_name) as f:
            sentences = f.readlines()
        return sentences
    print("Error trying to read from file")
    exit(-1)


def get_trees(file_name):
    return [Tree.fromstring(s) for s in read_from_file(file_name)]


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


def walk_up_to(tree, pos, targets):
    path = [pos]
    still_looking = True
    while still_looking:
        # climb one level up the tree by removing the last element
        # from the current tree position
        pos = pos[:-1]
        path.append(pos)
        # if an S node is encountered, return the path and pos
        if tree[pos].label() in targets:
            still_looking = False
    return path, pos
