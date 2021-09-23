import sys
from nltk.parse import CoreNLPParser
import hobbs
from utils import get_trees, read_from_file


if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print('\033[91m' + "Parameters Error" + '\033[0m')
        exit(-1)
    else:
        if sys.argv[1] in ["--core-nlp", "-c"]:
            parser = CoreNLPParser(url='http://localhost:9000')
            trees, sentences = None, None
            if sys.argv[2] in ["--file", "-f"]:
                sentences = read_from_file(sys.argv[3])
            elif sys.argv[2] in ["--string", "-s"]:
                sentences = sys.argv[3].split(". ")
            else:
                print('\033[91m' + "Parameters Error" + '\033[0m')
                exit(-1)
            # for simplicity it always choose the first proposed result
            trees = [list(parser.raw_parse(s)).pop() for s in sentences]
            hobbs.resolve(sys.argv[4], trees)
        elif sys.argv[1] in ["--treebank-tags", "-t"]:
            trees = get_trees(sys.argv[2])
            hobbs.resolve(sys.argv[3], trees)
        else:
            print('\033[91m' + "Parameters Error" + '\033[0m')
            exit(-1)
