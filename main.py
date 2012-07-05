import sys
import argparse
import led_parser
import symbolTable
import ast
import code_layout
import type_inference
from collections import defaultdict

#initializes the command line argument parser
def init_clp():
    parser = argparse.ArgumentParser(
        description='Generates intermediary code for a given source code. Code must follow specific syntax.')
    parser.add_argument('-i', '--input', metavar='SOURCE', type=str, dest='source',
        help='Path to source code files.')  
    parser.add_argument('-o', '--output', metavar='grammar', type=str, 
        help='The output file for generated code.', dest='output_f')
    return parser

if __name__ == '__main__':
    arg_parser = init_clp()
    args = arg_parser.parse_args()

    lexer = led_parser.create_lexer()
    src = ""

    if args.source != None:
        with open(args.source) as code: 
            src = code.read()
    else:
        src = sys.stdin.read()

    tokens = lexer.lex_input(src)
    root = led_parser.parse_program(tokens)
    symbol_table = symbolTable.SymbolTable()

    def null(o):
        pass
    d = defaultdict(lambda: null, {ast.Node: lambda x: symbol_table.buildSymbolTableNode(x)})
    root.accept(d)

    d = defaultdict(lambda: null, {
        ast.LValue: lambda x: type_inference.infer_lvalue(x, symbol_table.tabela_simbolos),
        ast.Expression: lambda x: type_inference.infer_expression(x, symbol_table.tabela_simbolos)
        })
    root.accept(d)

    symbol_table.printSymbolTable()

    tuple_Blocks = code_layout.split_statement_list(root.statements)

    generated_code = code_layout.flatten_blocks(tuple_Blocks[0])
    for x in generated_code:
        s = ''
        if (x[0] != '.'):
            s = '    '
        print(s+x)
