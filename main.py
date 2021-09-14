import sys
from nltk import Tree, RegexpParser, word_tokenize, pos_tag
import hobbs
from utils import get_pos
from demo import demo


def main(argv):
    if len(sys.argv) == 2 and argv[1] == "demo":
        demo()
    else:
        if len(sys.argv) > 5:
            print("Enter the file and the pronoun to resolve.")
        elif len(sys.argv) == 3:
            fname = sys.argv[1]
            pro = sys.argv[2]
            with open(fname) as f:
                sents = f.readlines()
            trees = [Tree.fromstring(s) for s in sents]
            pos = get_pos(trees[-1], pro)
            pos = pos[:-1]
            hobbs.resolve(pro, trees, pos)
        # elif len(sys.argv) == 4 and (sys.argv[1] == "--text-only" or sys.argv[1] == "-to"):
            # fname = sys.argv[2]
            # pro = sys.argv[3]
            # with open(fname) as f:
            #     sents = f.readlines()
            # grammar_np = r"NP: {<DT>?<JJ>*<NN>}"
            # chunk_parser = RegexpParser(grammar_np)
            # trees = []
            # for s in sents:
            #     tokens = pos_tag(word_tokenize(s))
            #     trees = chunk_parser.parse(tokens)
            # # print(repr(trees))
            # # t = repr(trees)
            # t = Tree(trees)
            # pos = get_pos(t[-1], pro)
            # pos = pos[:-1]
            # hobbs.resolve(pro, t, pos)
            # print(trees)


if __name__ == "__main__":
    main(sys.argv)
