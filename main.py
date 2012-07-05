import sys
import argparse
import led_parser
import symbolTable

#initializes the command line argument parser
def init_clp():
    parser = argparse.ArgumentParser(
        description='Generates intermediary code for a given source code. Code must follow specific syntax.')
    parser.add_argument('source', metavar='SOURCE', type=str, dest='source',
        help='Path to source code files')  
    parser.add_argument('-o', '--output', metavar='grammar', type=str, 
        help='The output file for generated code.', dest='output_f')i
    return parser

if __name__ == '__main__':
    arg_parser = init_clp()
    args = arg_parser.parse_args()

    lexer = led_parser.create_lexer()
    src = None

    if args.sources != None:
        with open(args.source) as code: 
            src = code.read()
    else:
        src = sys.stdin.read()

    tokens = lexex.parse_program(src)
    root = led_parser.parse_program(tokens)
    symbol_table = symbolTable.SymbolTable() 
    symbol_table.buildSymbolTableNode(root)

    symbol_table.printSymbolTable()
