import ast
import led_parser
from collections import defaultdict

def test_parse(fname="example.txt"):
    txt = open(fname, 'r').read()
    lex = led_parser.create_lexer()

    tokens = lex.lex_input(txt)
    root = led_parser.parse_program(tokens)

    def null(o):
        pass

    def print_node(o):
        print(o.__class__.__name__, o.__dict__)

    d = defaultdict(lambda: null, {ast.Node: print_node})
    root.accept(d)
