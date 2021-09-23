import nltk
import utils
import match
import traverse


def resolve(pronoun, trees):
    pos = utils.get_pos(trees[-1], pronoun)
    pos = pos[:-1]
    tree = []
    if pronoun in utils.pronouns:
        tree, pos = hobbs_algorithm(trees, pos)
    elif pronoun in utils.reflexive_pronouns:
        tree, pos = resolve_reflexive(trees, pos)
    if (tree, pos) != (None, None):
        print("The pronoun " + "\"" + pronoun + "\"" + " probably refers to: " + str(tree[pos]))
        for t in trees:
            t.draw()
        return
    return print("No antecedent found")


def hobbs_algorithm(sentences, pos):

    sentence_index = len(sentences) - 1  # Get the most recent sentence index

    tree, pos = utils.get_dom_np(sentences, pos)  # A
    pronoun = utils.get_pronoun(tree, pos)
    path, pos = utils.walk_up_to(tree, pos, ["NP", "S", "ROOT"])  # B
    candidate = traverse.traverse_left(tree, pos, path, pronoun)   # C

    while candidate == (None, None):

        if pos == ():
            # go to the previous sentence
            sentence_index -= 1
            if sentence_index < 0:
                return None
            candidate = traverse.traverse_tree(sentences[sentence_index], pronoun)  # D
            if candidate != (None, None):
                return candidate

        path, pos = utils.walk_up_to(tree, pos, ["NP", "S", "ROOT"])  # E

        if "NP" in tree[pos].label() and tree[pos].label() not in utils.nominal_labels:  # F
            for c in tree[pos]:
                if isinstance(c, nltk.Tree) and c.label() in utils.nominal_labels:
                    if utils.get_pos(tree, c) not in path and match.match(tree, pos, pronoun):
                        candidate = (tree, pos)
                        if candidate != (None, None):
                            return candidate

        candidate = traverse.traverse_left(tree, pos, path, pronoun, check=0)  # G
        if candidate != (None, None):
            return candidate

        if tree[pos].label() in ["S"]:  # H
            candidate = traverse.traverse_right(tree, pos, path, pronoun)
            if candidate != (None, None):
                return candidate
    return candidate


def resolve_reflexive(sents, pos):

    tree, pos = utils.get_dom_np(sents, pos)
    pro = utils.get_pronoun(tree, pos)

    # local binding domain of a reflexive is the lowest clause 
    # containing the reflexive and a binding NP
    path, pos = utils.walk_up_to(tree, pos, ["S"])

    return traverse.traverse_tree(tree, pro)
