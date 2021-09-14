import sys
from nltk import Tree, RegexpParser, word_tokenize, pos_tag, ShiftReduceParser, CFG
from nltk.parse import CoreNLPParser
import hobbs
from utils import get_pos


def main(argv):
    if len(sys.argv) == 3 and argv[1] == "demo":
        pro = sys.argv[2]
        parser = CoreNLPParser(url='http://localhost:9000')
        parsed = list(parser.raw_parse('John said Mary likes herself'))
        one = parsed.pop()
        one.draw()
        pos = get_pos(one[-1], pro)
        pos = pos[:-1]
        hobbs.resolve(pro, one, pos)
        # grammar1 = CFG.fromstring("""
        #   S -> NP VP
        #   VP -> V NP | V NP PP
        #   PP -> P NP
        #   V -> "saw" | "ate" | "walked"
        #   NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
        #   Det -> "a" | "an" | "the" | "my"
        #   N -> "man" | "dog" | "cat" | "telescope" | "park"
        #   P -> "in" | "on" | "by" | "with"
        #   """)
        # grammar2 = CFG.fromstring("""
        #   S  -> NP VP
        #   NP -> Det Nom | PropN | PRP
        #   Nom -> Adj Nom | N
        #   VP -> V Adj | V NP | V S | V NP PP
        #   PP -> P NP
        #   PropN -> 'Buster' | 'Maria' | 'Joe'
        #   PRP -> 'he' | 'she' | 'it'
        #   Det -> 'the' | 'a'
        #   N -> 'bear' | 'squirrel' | 'tree' | 'fish' | 'log'
        #   Adj  -> 'angry' | 'frightened' |  'little' | 'tall'
        #   V ->  'chased'  | 'saw' | 'said' | 'thought' | 'was' | 'put'
        #   P -> 'on'
        #   """)
        # sr_parser = ShiftReduceParser(grammar2)
        # sent = "Maria saw a little frightened bear she was angry".split()
        # parse_string = ""
        # for tree in sr_parser.parse(sent):
        #     tree.draw()
        #     parse_string = ' '.join(str(tree).split())
        # t = [Tree.fromstring(parse_string)]
        # pos = get_pos(t[-1], pro)
        # pos = pos[:-1]
        # hobbs.resolve(pro, t, pos)
    else:
        if len(sys.argv) > 5:
            print("Enter the file and the pronoun to resolve.")
        # elif len(sys.argv) == 3:
        #     fname = sys.argv[1]
        #     pro = sys.argv[2]
        #     with open(fname) as f:
        #         sents = f.readlines()
        #     trees = [Tree.fromstring(s) for s in sents]
        #     pos = get_pos(trees[-1], pro)
        #     pos = pos[:-1]
        #     hobbs.resolve(pro, trees, pos)
        # elif len(sys.argv) == 4 \
        #         and (sys.argv[1] == "--shift-reduce-parser" or sys.argv[1] == "-srp") \
        #         and (sys.argv[2] == "--default-grammar" or sys.argv[2] == "-d" or sys.argv[2] == "--path" or sys.argv[2] == "-p"):
        #     # fname = sys.argv[3]
        #     grammar1 = CFG.fromstring("""
        #       S -> NP VP
        #       VP -> V NP | V NP PP
        #       PP -> P NP
        #       V -> "saw" | "ate" | "walked"
        #       NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
        #       Det -> "a" | "an" | "the" | "my"
        #       N -> "man" | "dog" | "cat" | "telescope" | "park"
        #       P -> "in" | "on" | "by" | "with"
        #       """)
        #     sr_parser = ShiftReduceParser(grammar1)
        #     sent = 'Mary saw a dog'.split()
        #     for tree in sr_parser.parse(sent):
        #         print(tree)
            # pro = sys.argv[4]
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
