def walk_to_s(tree, pos):
    """ Takes the tree being searched and the position from which
    the walk up is started. Returns the position of the first S
    encountered and the path taken to get there from the
    dominating NP. The path consists of a list of tree positions.

    Args:
        tree: the tree being searched
        pos: the position from which the walk is started
    Returns:
        path: the path taken to get the an S node
        pos: the position of the first S node encountered
    """
    path = [pos]
    still_looking = True
    while still_looking:
        # climb one level up the tree by removing the last element
        # from the current tree position
        pos = pos[:-1]
        path.append(pos)
        # if an S node is encountered, return the path and pos
        if tree[pos].label() == "S":
            still_looking = False
    return path, pos


def walk_to_np_or_s(tree, pos):
    """ Takes the tree being searched and the position from which
    the walk up is started. Returns the position of the first NP
    or S encountered and the path taken to get there from the
    dominating NP. The path consists of a list of tree positions.

    Args:
        tree: the tree being searched
        pos: the position from which the walk is started
    Returns:
        path: the path taken to get the an NP or S node
        pos: the position of the first NP or S node encountered
    """
    path = [pos]
    still_looking = True
    while still_looking:
        # climb one level up the tree by removing the last element
        # from the current tree position
        pos = pos[:-1]
        path.append(pos)
        # if an NP or S node is encountered, return the path and pos
        if "NP" in tree[pos].label() or tree[pos].label() == "S":
            still_looking = False
    return path, pos
