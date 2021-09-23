from nltk import Tree

nominal_labels = ["NN", "NNS", "NNP", "NNPS", "PRP"]
pronouns = ["He", "he", "Him", "him", "She", "she", "Her", "her", "It", "it", "They", "they"]
reflexive_pronouns = ["Himself", "himself", "Herself", "herself", "Itself", "itself", "Themselves", "themselves"]
pronoun_numbers = {
    "NN": "singular",
    "NNP": "singular",
    "he": "singular",
    "she": "singular",
    "him": "singular",
    "her": "singular",
    "it": "singular",
    "himself": "singular",
    "herself": "singular",
    "itself": "singular",
    "NNS": "plural",
    "NNPS": "plural",
    "they": "plural",
    "them": "plural",
    "themselves": "plural",
    "PRP": None
}
male_p = ["he", "him", "himself"]
female_p = ["she", "her", "herself"]
neuter_p = ["it", "itself"]


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
    for pos in tree.treepositions():
        if tree[pos] == node:
            return pos
    return None


def get_pronoun(tree, pos):
    return tree[pos].leaves()[0].lower()


def get_dom_np(sents, pos):
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
