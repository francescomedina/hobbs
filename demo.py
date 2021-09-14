from nltk import Tree, word_tokenize, pos_tag, RegexpParser
from nltk.draw.tree import TreeView
import os
import time
import hobbs


def demo():

    txt = "Judge Curry ordered the refunds to begin Feb. 1 and said that he wouldn't entertain any appeals or other " \
          "attempts to block his order by Commonwealth Edison."
    tokens = pos_tag(word_tokenize(txt))
    grammar_np = r"NP: {<DT>?<JJ>*<NN>}"
    chunk_parser = RegexpParser(grammar_np)
    tree1 = chunk_parser.parse(tokens)
    tree1.draw()

    # tree1 = Tree.fromstring('(S (NP (NNP John) ) (VP (VBD said) (SBAR (-NONE- 0) \
    #     (S (NP (PRP he) ) (VP (VBD likes) (NP (NNS dogs) ) ) ) ) ) )')
    tree2 = Tree.fromstring('(S (NP (NNP John) ) (VP (VBD said) (SBAR (-NONE- 0) \
        (S (NP (NNP Mary) ) (VP (VBD likes) (NP (PRP him) ) ) ) ) ) )')
    tree3 = Tree.fromstring('(S (NP (NNP John)) (VP (VBD saw) (NP (DT a) \
        (JJ flashy) (NN hat)) (PP (IN at) (NP (DT the) (NN store)))))')
    tree4 = Tree.fromstring('(S (NP (PRP He)) (VP (VBD showed) (NP (PRP it)) \
        (PP (IN to) (NP (NNP Terrence)))))')
    tree5 = Tree.fromstring("(S(NP-SBJ (NNP Judge) (NNP Curry))\
        (VP(VP(VBD ordered)(NP-1 (DT the) (NNS refunds))\
        (S(NP-SBJ (-NONE- *-1))(VP (TO to) (VP (VB begin)\
        (NP-TMP (NNP Feb.) (CD 1))))))(CC and)\
        (VP(VBD said)(SBAR(IN that)(S(NP-SBJ (PRP he))(VP(MD would)\
        (RB n't)(VP(VB entertain)(NP(NP (DT any) (NNS appeals))(CC or)\
        (NP(NP(JJ other)(NNS attempts)(S(NP-SBJ (-NONE- *))(VP(TO to)\
        (VP (VB block) (NP (PRP$ his) (NN order))))))(PP (IN by)\
        (NP (NNP Commonwealth) (NNP Edison)))))))))))(. .))")
    tree6 = Tree.fromstring('(S (NP (NNP John) ) (VP (VBD said) (SBAR (-NONE- 0) \
        (S (NP (NNP Mary) ) (VP (VBD likes) (NP (PRP herself) ) ) ) ) ) )')

    print("Sentence 1:")
    print(tree1)
    tree, pos = hobbs.hobbs([tree1], (1, 1, 1, 0, 0))
    print("Proposed antecedent for 'he':", tree[pos], '\n')

    print("Sentence 2:")
    print(tree2)
    tree, pos = hobbs.hobbs([tree2], (1, 1, 1, 1, 1, 0))
    print("Proposed antecedent for 'him':", tree[pos], '\n')

    print("Sentence 3:")
    print(tree3)
    print("Sentence 4:")
    print(tree4)
    tree, pos = hobbs.hobbs([tree3, tree4], (1, 1, 0))
    print("Proposed antecedent for 'it':", tree[pos])
    tree, pos = hobbs.hobbs([tree3, tree4], (0, 0))
    print("Proposed antecedent for 'he':", tree[pos], '\n')

    print("Sentence 5:")
    print(tree5)
    tree, pos = hobbs.hobbs([tree5], (1, 2, 1, 1, 0, 0))
    print("Proposed antecedent for 'he':", tree[pos], '\n')

    print("Sentence 6:")
    print(tree6)
    tree, pos = hobbs.resolve_reflexive([tree6], (1, 1, 1, 1, 1, 0))
    print("Proposed antecedent for 'herself':", tree[pos], '\n')
