import nltk
from nltk.corpus import names
import utils


def match(tree, pos, pro):
    return number_match(tree, pos, pro) and gender_match(tree, pos, pro)


def number_match(tree, pos, pro):
    for c in tree[pos]:
        if isinstance(c, nltk.Tree) and c.label() in utils.nominal_labels:
            if utils.pronoun_numbers[c.label()] == utils.pronoun_numbers[pro]:
                return True
    return False


#
def gender_match(tree, pos, pro):

    male_names = (name.lower() for name in names.words('male.txt'))
    female_names = (name.lower() for name in names.words('female.txt'))
    male_pronouns = utils.male_p
    female_pronouns = utils.female_p
    neuter_pronouns = utils.neuter_p

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
