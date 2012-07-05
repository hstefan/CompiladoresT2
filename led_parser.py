import ast
import lexer
from collections import OrderedDict

class ParseError(Exception):
    pass

class TokenPeek:
    def __init__(self, token_gen):
        self.token_iter = iter(token_gen)
        self.top = next(self.token_iter)

    def peek(self):
        return self.top

    def next(self):
        try:
            self.top = next(self.token_iter)
        except StopIteration:
            self.top = ('@@eof', None)

    def pop(self):
        tmp = self.peek()
        self.next()
        return tmp

    def expect(self, tok_id):
        t, v = self.pop()
        if t != tok_id:
            raise ParseError("Expected %s; got %s." % (tok_id, t))
        return v

    def peek_id(self):
        t, v = self.peek()
        return t

###########################################################

def util_parse_list(tokens, func, sep_token='@$,'):
    items = [func(tokens)]

    while True:
        t, v = tokens.peek()
        if t != sep_token:
            break
        tokens.next()
        items.append(func(tokens))

    return items

def parse_identifier(tokens):
    return tokens.expect('@identifier')

def parse_int(tokens):
    return int(tokens.expect('@int-literal'))

def parse_real(tokens):
    return float(tokens.expect('@real-literal'))

def parse_char(tokens):
    return tokens.expect('@char-literal')

def parse_string(tokens):
    return tokens.expect('@string-literal')

def parse_basic_type(tokens):
    t, v = tokens.pop()

    generic = None

    types = {
            '@$int': (ast.BasicType.INT, False),
            '@$real': (ast.BasicType.REAL, False),
            '@$char': (ast.BasicType.CHAR, False),
            '@$bool': (ast.BasicType.BOOL, False),
            '@$string': (ast.BasicType.STRING, False),
            '@$list': (ast.BasicType.LIST, True)
            }

    try:
        type_, has_generic = types[t]
    except KeyError:
        raise ParseError("Expected type; got {0}.".format(t))

    if has_generic:
        tokens.expect('@$<')
        generic = parse_type_expression(tokens)
        tokens.expect('@$>')
    else:
        generic = None

    return ast.BasicType(type_, generic)

def parse_type_expression(tokens):
    node = parse_basic_type(tokens)

    t, v = tokens.peek()
    while t in ('@$&', '@$['):
        tokens.next()
        if t == '@$&':
            node = ast.TypeReference(node)
        elif t == '@$[':
            size = parse_int(tokens)
            node = ast.TypeArray(node, size)
            tokens.expect('@$]')
        t, v = tokens.peek()

    return node

def parse_list_literal(tokens):
    tokens.expect('@$[')

    items = []

    t, v = tokens.peek()
    if t == '@$]':
        tokens.next()
    else:
        items.append(parse_expression(tokens))

        t, v = tokens.peek()
        while t == '@$,':
            tokens.expect('@$,')
            items.append(parse_expression(tokens))
            t, v = tokens.peek()

        tokens.expect('@$]')

    return ast.Literal(items, ast.BasicType.LIST)

def parse_expr_e(tokens):
    t, v = tokens.peek()

    if t == '@$(':
        tokens.next()
        node = parse_expression(tokens)
        tokens.expect('@$)')
    elif t == '@identifier':
        node = ast.Variable(parse_identifier(tokens))
    elif t == '@int-literal':
        node = ast.Literal(parse_int(tokens), ast.BasicType.INT)
    elif t == '@real-literal':
        node = ast.Literal(parse_real(tokens), ast.BasicType.REAL)
    elif t == '@char-literal':
        node = ast.Literal(parse_char(tokens), ast.BasicType.CHAR)
    elif t == '@string-literal':
        node = ast.Literal(parse_string(tokens), ast.BasicType.STRING)
    elif t == '@$true':
        tokens.next()
        node = ast.Literal(True, ast.BasicType.BOOL)
    elif t == '@$false':
        tokens.next()
        node = ast.Literal(False, ast.BasicType.BOOL)
    elif t == '@$[':
        node = parse_list_literal(tokens)
    else:
        raise ParseError("Expected identifier or literal; got {0}.".format(t))

    return node

def parse_expr_d(tokens):
    if tokens.peek_id() == '@$not':
        tokens.next()
        should_not = True
    else:
        should_not = False

    node = parse_expr_e(tokens)

    t, v = tokens.peek()
    while t in ('@$&', '@$['):
        tokens.next()
        if t == '@$&':
            node = ast.UnaryOp('&', node)
        elif t == '@$[':
            index = parse_expression(tokens)
            node = ast.BinaryOp('[]', node, index)
            tokens.expect('@$]')
        t, v = tokens.peek()

    if should_not:
        node = ast.UnaryOp('not', node)

    return node

def parse_expr_c(tokens):
    lhs = parse_expr_d(tokens)

    t, op_type = tokens.peek()
    if t in ('@$*', '@$/', '@$%'):
        tokens.next()
        rhs = parse_expr_c(tokens)
        return ast.BinaryOp(op_type, lhs, rhs)
    else:
        return lhs

def parse_expr_b(tokens):
    lhs = parse_expr_c(tokens)

    t, op_type = tokens.peek()
    if t in ('@$+', '@$-'):
        tokens.next()
        rhs = parse_expr_b(tokens)
        return ast.BinaryOp(op_type, lhs, rhs)
    else:
        return lhs

def parse_expr_a(tokens):
    lhs = parse_expr_b(tokens)

    t, op_type = tokens.peek()
    if t in ('@$==', '@$!=', '@$<', '@$<=', '@$>', '@$>='):
        tokens.next()
        rhs = parse_expr_a(tokens)
        return ast.BinaryOp(op_type, lhs, rhs)
    else:
        return lhs

def parse_expression(tokens):
    lhs = parse_expr_a(tokens)

    t, op_type = tokens.peek()
    if t in ('@$and', '@$or'):
        tokens.next()
        rhs = parse_expression(tokens)
        return ast.BinaryOp(op_type, lhs, rhs)
    else:
        return lhs

def parse_lvalue(tokens):
    node = ast.LValueVariable(parse_identifier(tokens))

    t, v = tokens.peek()
    while t in ('@$&', '@$['):
        tokens.next()
        if t == '@$&':
            node = ast.LValueDereference(node)
        elif t == '@$[':
            index = parse_expression(tokens)
            node = ast.LValueIndex(node, index)
            tokens.expect('@$]')
        t, v = tokens.peek()

    return node

def parse_assignment(tokens):
    target = parse_lvalue(tokens)
    tokens.expect('@$:=')
    value = parse_expression(tokens)

    return ast.Assignment(target, value)

def parse_declaration(tokens):
    tokens.expect('@$var')
    names = util_parse_list(tokens, parse_identifier)
    tokens.expect('@$:')
    type_expr = parse_type_expression(tokens)

    if tokens.peek_id() == '@$:=':
        tokens.next()
        initializer = parse_expression(tokens)
    else:
        initializer = None

    return ast.VariableDeclaration(names, type_expr, initializer)

def parse_while_statement(tokens):
    tokens.expect('@$while')
    condition = parse_expression(tokens)
    tokens.expect('@$do')
    body = parse_statement_list(tokens)
    tokens.expect('@$end')

    return ast.WhileStatement(condition, body)

def parse_if_statement(tokens):
    tokens.expect('@$if')
    condition = parse_expression(tokens)
    tokens.expect('@$then')
    body = parse_statement_list(tokens)

    if tokens.peek_id() == '@$else':
        tokens.next()
        else_body = parse_statement_list(tokens)
    else:
        else_body = None

    tokens.expect('@$end')

    return ast.IfStatement(condition, body, else_body)

def parse_input_statement(tokens):
    tokens.expect('@$input')
    return ast.InputStatement(util_parse_list(tokens, parse_lvalue))

def parse_output_statement(tokens):
    tokens.expect('@$output')
    return ast.OutputStatement(util_parse_list(tokens, parse_expression))

def parse_statement_list(tokens):
    statements = []

    t, v = tokens.peek()
    while t not in ('@@eof', '@$end', '@$else'):
        if t == '@$input':
            statements.append(parse_input_statement(tokens))
        elif t == '@$output':
            statements.append(parse_output_statement(tokens))
        elif t == '@$if':
            statements.append(parse_if_statement(tokens))
        elif t == '@$while':
            statements.append(parse_while_statement(tokens))
        elif t == '@$var':
            statements.append(parse_declaration(tokens))
        elif t == '@identifier':
            statements.append(parse_assignment(tokens))
        else:
            raise ParseError("Expected input, output, if, while, variable declaration or assignment; got {0}.".format(t))

        tokens.expect('@$;')
        t, v = tokens.peek()

    return statements

def parse_program(token_iter):
    return ast.Program(parse_statement_list(TokenPeek(token_iter)))

def create_lexer():
    tokens_info = OrderedDict()

    literals = {'int', 'real', 'char', 'bool', 'string', 'list',
            'true', 'false',
            'not', 'and', 'or',
            'input', 'output', 'if', 'then', 'else', 'end', 'while', 'do', 'var',
            '&', '[', ']', '(', ')',
            '+', '-', '*', '/', '%',
            '==', '!=', '<', '<=', '>', '>=',
            ',', ':=', ':', ';'
            }
    lexer.add_literal_tokens(tokens_info, literals)

    tokens_info.update([
        ("@@skip", r"(?:\s*(?://[^\n]*\n)?)*"),
        ("@identifier", r"([a-zA-Z_][a-zA-Z0-9_]*)"),
        ("@real-literal", r"([0-9]+\.[0-9]+)"),
        ("@int-literal", r"([0-9]+)"),
        ("@char-literal", r"'(.)'"),
        ("@string-literal", '"' + r"([^\"]*)" + '"')
        ])

    return lexer.Tokenizer(tokens_info)

__all__ = ['parse_grammar', 'create_lexer', 'ParseError']
