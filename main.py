import sys
from nltk import Tree, ShiftReduceParser, CFG
from nltk.parse import CoreNLPParser
import hobbs
from utils import get_trees, read_from_file


def main(argv):
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Parameter Error: enter the file name or the target string and the pronoun to resolve.")
        exit(-1)
    else:
        if argv[1] in ["--core-nlp", "-c"]:
            parser = CoreNLPParser(url='http://localhost:9000')
            trees = None
            if argv[2] in ["--file", "-f"]:
                sentences = read_from_file(argv[3])
                trees = [list(parser.raw_parse(s)).pop() for s in sentences]
            elif argv[2] in ["--string", "s"]:
                trees = [list(parser.raw_parse(argv[3])).pop()]
            else:
                print("Error in parameters")
                exit(-1)
            hobbs.resolve(sys.argv[4], trees)
        elif argv[1] in ["--with-tags", "-w"]:
            trees = get_trees(argv[2])
            hobbs.resolve(sys.argv[3], trees)
        elif argv[1] in ["--grammar", "-g"]:
            sentences = read_from_file(argv[2])
            grammar = CFG.fromstring(sentences)
            sr_parser = ShiftReduceParser(grammar)
            sent = argv[3].split()
            parse_string = ""
            for tree in sr_parser.parse(sent):
                parse_string = ' '.join(str(tree).split())
            trees = [Tree.fromstring(parse_string)]
            hobbs.resolve(sys.argv[4], trees)


if __name__ == "__main__":
    main(sys.argv)
