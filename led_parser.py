import ast
import lexer

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
        t, v = self.next()
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
    return ast.InputStatement(util_parse_list(tokens, parse_expression))

def parse_statement_list(tokens):
    statements = []

    t, v = tokens.peek()
    while t != '@@eof':
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
    tokens_info = {
        "@@skip" : r"(?:\s*(?://[^\n]*\n)?)*",
        "@token-id" : r"(@@?[a-z]+(?:-[a-z]+)*)",
        "@rule-id" : r"(#?[a-z]+(?:-[a-z]+)*)",
        "@token-literal" : r"'((?:\\.|[^'\n])+)'",
        "@token-match" : '"' + r"((?:\\.|[^\"\n])+)" + '"'
    }

    literals = [':=', '(', ')', '?', '*', '=>', '|', ';']
    lexer.add_literal_tokens(tokens_info, literals)

    return lexer.Tokenizer(tokens_info)

__all__ = ['parse_grammar', 'create_lexer', 'ParseError']
