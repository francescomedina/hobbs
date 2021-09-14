import nltk
from nltk.corpus import names
import utils


def match(tree, pos, pro):
    """ Takes a proposed antecedent and checks whether it matches
    the pronoun in number and gender

    Args:
        tree: the tree in which a potential antecedent has been found
        pos: the position of the potential antecedent
        pro: the pronoun being resolved (string)
    Returns:
        True if the antecedent and pronoun match
        False otherwise
    """
    if number_match(tree, pos, pro) and gender_match(tree, pos, pro):
        return True
    return False


def number_match(tree, pos, pro):
    """ Takes a proposed antecedent and pronoun and checks whether
    they match in number.
    """
    m = {"NN": "singular",
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
         "PRP": None}

    # if the label of the nominal dominated by the proposed NP and
    # the pronoun both map to the same number feature, they match
    for c in tree[pos]:
        if isinstance(c, nltk.Tree) and c.label() in utils.nominal_labels:
            if m[c.label()] == m[pro]:
                return True
    return False


def gender_match(tree, pos, pro):
    """ Takes a proposed antecedent and pronoun and checks whether
    they match in gender. Only checks for mismatches between singular
    proper name antecedents and singular pronouns.
    """
    male_names = (name.lower() for name in names.words('male.txt'))
    female_names = (name.lower() for name in names.words('female.txt'))
    male_pronouns = ["he", "him", "himself"]
    female_pronouns = ["she", "her", "herself"]
    neuter_pronouns = ["it", "itself"]

    for c in tree[pos]:
        if isinstance(c, nltk.Tree) and c.label() in utils.nominal_labels:
            # If the proposed antecedent is a recognized male name,
            # but the pronoun being resolved is either female or
            # neuter, they don't match
            if c.leaves()[0].lower() in male_names:
                if pro in female_pronouns:
                    return False
                elif pro in neuter_pronouns:
                    return False
            # If the proposed antecedent is a recognized female name,
            # but the pronoun being resolved is either male or
            # neuter, they don't match
            elif c.leaves()[0].lower() in female_names:
                if pro in male_pronouns:
                    return False
                elif pro in neuter_pronouns:
                    return False
            # If the proposed antecedent is a numeral, but the
            # pronoun being resolved is not neuter, they don't match
            elif c.leaves()[0].isdigit():
                if pro in male_pronouns:
                    return False
                elif pro in female_pronouns:
                    return False

    return True
