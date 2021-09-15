import nltk
import utils
import walk
import match
import traverse
from utils import get_pos


def resolve(pronoun, trees):
    pos = get_pos(trees[-1], pronoun)
    pos = pos[:-1]
    tree = []
    if pronoun in utils.p:
        tree, pos = hobbs_algorithm(trees, pos)
    elif pronoun in utils.r:
        tree, pos = resolve_reflexive(trees, pos)
    print(pronoun + "probably refers to: " + tree[pos])
    for t in trees:
        t.draw()


def hobbs_algorithm(phrase, pos):
    """
    Args:
        phrase: list of sentences to be searched
        pos: the position of the pronoun to be resolved
    Returns:
        candidate: a tuple containing the tree and position of the
            proposed antecedent
    """

    # Step 1: begin at the NP node immediately dominating the pronoun
    tree, pos = utils.get_dom_np(phrase, pos)

    # Step 2: Go up the tree to the first NP or S node encountered
    path, pos = walk.walk_to_np_or_s(tree, pos)

    # String representation of the pronoun to be resolved
    pronoun = tree[pos].leaves()[0].lower()

    # Step 3: Traverse all branches below pos to the left of path
    # left-to-right, breadth-first. Propose as an antecedent any NP
    # node that is encountered which has an NP or S node between it and pos
    candidate = traverse.traverse_left(tree, pos, path, pronoun)

    # The index of the most recent sentence in sents
    phrase_index = len(phrase) - 1

    while candidate == (None, None):

        # Step 4: If pos is the highest S node in the sentence, 
        # traverse the surface parses of previous sentences in order
        # of recency, the most recent first; each tree is traversed in
        # a left-to-right, breadth-first manner, and when an NP node is
        # encountered, it is proposed as an antecedent
        if pos == ():
            # go to the previous sentence
            phrase_index -= 1
            # if there are no more sentences, no antecedent found
            if phrase_index < 0:
                return None
            # search new sentence
            candidate = traverse.traverse_tree(phrase[phrase_index], pronoun)
            if candidate != (None, None):
                return candidate

        # Step 5: If pos is not the highest S in the sentence, from pos,
        # go up the tree to the first NP or S node encountered. 
        path, pos = walk.walk_to_np_or_s(tree, pos)

        # Step 6: If pos is an NP node and if the path to pos did not pass 
        # through the nominal node that pos immediately dominates, propose pos 
        # as the antecedent.
        if "NP" in tree[pos].label() and tree[pos].label() not in utils.nominal_labels:
            for c in tree[pos]:
                if isinstance(c, nltk.Tree) and c.label() in utils.nominal_labels:
                    if utils.get_pos(tree, c) not in path and match.match(tree, pos, pronoun):
                        candidate = (tree, pos)
                        if candidate != (None, None):
                            return candidate

        # Step 7: Traverse all branches below pos to the left of path, 
        # in a left-to-right, breadth-first manner. Propose any NP node
        # encountered as the antecedent.
        candidate = traverse.traverse_left(tree, pos, path, pronoun, check=0)
        if candidate != (None, None):
            return candidate

        # Step 8: If pos is an S node, traverse all the branches of pos
        # to the right of path in a left-to-right, breadth-forst manner, but
        # do not go below any NP or S node encountered. Propose any NP node
        # encountered as the antecedent.
        if tree[pos].label() == "S":
            candidate = traverse.traverse_right(tree, pos, path, pronoun)
            if candidate != (None, None):
                return candidate

    return candidate


def resolve_reflexive(sents, pos):
    """ Resolves reflexive pronouns by going to the first S
    node above the NP dominating the pronoun and searching for
    a matching antecedent. If none is found in the lowest S
    containing the anaphor, then the sentence probably isn't 
    grammatical or the reflexive is being used as an intensifier.
    """
    tree, pos = utils.get_dom_np(sents, pos)

    pro = tree[pos].leaves()[0].lower()

    # local binding domain of a reflexive is the lowest clause 
    # containing the reflexive and a binding NP
    path, pos = walk.walk_to_s(tree, pos)

    candidate = traverse.traverse_tree(tree, pro)

    return candidate
