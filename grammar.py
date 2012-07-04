from string import *
import re
from yappsrt import *

class LEDScanner(Scanner):
    patterns = [
        ('";"', re.compile(';')),
        ('"var"', re.compile('var')),
        ('":="', re.compile(':=')),
        ('"do"', re.compile('do')),
        ('"while"', re.compile('while')),
        ('"end"', re.compile('end')),
        ('"then"', re.compile('then')),
        ('"if"', re.compile('if')),
        ('"output"', re.compile('output')),
        ('"input"', re.compile('input')),
        ('"or"', re.compile('or')),
        ('"and"', re.compile('and')),
        ('">="', re.compile('>=')),
        ('">"', re.compile('>')),
        ('"<="', re.compile('<=')),
        ('"<"', re.compile('<')),
        ('"!="', re.compile('!=')),
        ('"=="', re.compile('==')),
        ('"-"', re.compile('-')),
        ('"+"', re.compile('+')),
        ('"%"', re.compile('%')),
        ('"/"', re.compile('/')),
        ('"*"', re.compile('*')),
        ('"not"', re.compile('not')),
        ('")"', re.compile(')')),
        ('"("', re.compile('(')),
        ('"}"', re.compile('}')),
        ('"{"', re.compile('{')),
        ('":"', re.compile(':')),
        ('" ]"', re.compile(' ]')),
        ('"false"', re.compile('false')),
        ('"true"', re.compile('true')),
        ('"&"', re.compile('&')),
        ('"map"', re.compile('map')),
        ('"list"', re.compile('list')),
        ('"string"', re.compile('string')),
        ('"bool"', re.compile('bool')),
        ('"char"', re.compile('char')),
        ('"real"', re.compile('real')),
        ('"int"', re.compile('int')),
        ('"]"', re.compile(']')),
        ('"["', re.compile('[')),
        ('","', re.compile(',')),
        ('(?:\\s*(?://[^\n]*\n)?)*', re.compile('(?:\\s*(?://[^\n]*\n)?)*')),
        ('identifier', re.compile('([a-zA-Z_][a-zA-Z0-9_]*)')),
        ('int_literal', re.compile('([0-9]+)')),
        ('real_literal', re.compile('([0-9]+\\.[0-9]+)')),
        ('char_literal', re.compile("'(.)'")),
        ('string_literal', re.compile('"([^"]*)"')),
    ]
    def __init__(self, str):
        Scanner.__init__(self,None,['(?:\\s*(?://[^\n]*\n)?)*'],str)

class LED(Parser):
    def identifier_list(self):
        identifier = self._scan('identifier')
        while self._peek('","', '":"', '"*"', '"/"', '"%"', '"+"', '"-"', '"=="', '"!="', '"<"', '"<="', '">"', '">="', '"and"', '"or"', '";"', '")"', '"]"', '" ]"', '"}"') == '","':
            self._scan('","')
            identifier = self._scan('identifier')

    def generic(self):
        self._scan('"["')
        type_expression = self.type_expression()
        self._scan('"]"')

    def basic_type(self):
        _token_ = self._peek('"int"', '"real"', '"char"', '"bool"', '"string"', '"list"', '"map"')
        if _token_ == '"int"':
            self._scan('"int"')
        elif _token_ == '"real"':
            self._scan('"real"')
        elif _token_ == '"char"':
            self._scan('"char"')
        elif _token_ == '"bool"':
            self._scan('"bool"')
        elif _token_ == '"string"':
            self._scan('"string"')
        elif _token_ == '"list"':
            self._scan('"list"')
            generic = self.generic()
        else:# == '"map"'
            self._scan('"map"')
            generic = self.generic()
            generic = self.generic()

    def type_decoration(self):
        _token_ = self._peek('"&"', '"["')
        if _token_ == '"&"':
            self._scan('"&"')
        else:# == '"["'
            self._scan('"["')
            int_literal = self._scan('int_literal')
            self._scan('"]"')

    def type_expression(self):
        basic_type = self.basic_type()
        while self._peek('"&"', '"["', '"]"', '":="') in ['"&"', '"["']:
            type_decoration = self.type_decoration()

    def bool_literal(self):
        _token_ = self._peek('"true"', '"false"')
        if _token_ == '"true"':
            self._scan('"true"')
        else:# == '"false"'
            self._scan('"false"')

    def list_literal(self):
        self._scan('"["')
        expression = self.expression()
        if 1:
            while self._peek('","', '"*"', '"/"', '"%"', '"+"', '"-"', '"=="', '"!="', '"<"', '"<="', '">"', '">="', '"and"', '"or"', '":"', '")"', '"]"', '" ]"', '";"', '"}"') == '","':
                self._scan('","')
                expression = self.expression()
        self._scan('" ]"')

    def map_entry(self):
        expression = self.expression()
        self._scan('":"')
        expression = self.expression()

    def map_literal(self):
        self._scan('"{"')
        if self._peek('","', '"}"', '"not"', '"&"', 'identifier', 'real_literal', 'char_literal', '"true"', '"false"', 'string_literal', '"["', '"{"', '"("', '"*"', '"/"', '"%"', '"+"', '"-"', '"=="', '"!="', '"<"', '"<="', '">"', '">="', '"and"', '"or"', '":"', '")"', '"]"', '" ]"', '";"') in ['"not"', '"&"', 'identifier', 'real_literal', 'char_literal', '"true"', '"false"', 'string_literal', '"["', '"{"', '"("']:
            map_entry = self.map_entry()
            while self._peek('","', '"*"', '"/"', '"%"', '"+"', '"-"', '"=="', '"!="', '"<"', '"<="', '">"', '">="', '"and"', '"or"', '":"', '")"', '"]"', '"}"', '" ]"', '";"') == '","':
                self._scan('","')
                map_entry = self.map_entry()
        self._scan('"}"')

    def value(self):
        _token_ = self._peek('identifier', 'real_literal', 'char_literal', '"true"', '"false"', 'string_literal', '"["', '"{"')
        if _token_ == 'identifier':
            identifier = self._scan('identifier')
        elif _token_ == 'real_literal':
            real_literal = self._scan('real_literal')
        elif _token_ == 'char_literal':
            char_literal = self._scan('char_literal')
        elif _token_ not in ['string_literal', '"["', '"{"']:
            bool_literal = self.bool_literal()
        elif _token_ == 'string_literal':
            string_literal = self._scan('string_literal')
        elif _token_ == '"["':
            list_literal = self.list_literal()
        else:# == '"{"'
            map_literal = self.map_literal()

    def expr_e(self):
        _token_ = self._peek('identifier', 'real_literal', 'char_literal', '"true"', '"false"', 'string_literal', '"["', '"{"', '"("')
        if _token_ != '"("':
            value = self.value()
        else:# == '"("'
            self._scan('"("')
            expression = self.expression()
            self._scan('")"')

    def expr_d(self):
        if self._peek('"not"', '"&"', 'identifier', 'real_literal', 'char_literal', '"true"', '"false"', 'string_literal', '"["', '"{"', '"("') == '"not"':
            self._scan('"not"')
        if self._peek('"&"', 'identifier', 'real_literal', 'char_literal', '"true"', '"false"', 'string_literal', '"["', '"{"', '"("') == '"&"':
            self._scan('"&"')
        expr_e = self.expr_e()
        if self._peek('"["', '"*"', '"/"', '"%"', '"+"', '"-"', '"=="', '"!="', '"<"', '"<="', '">"', '">="', '"and"', '"or"', '","', '":"', '")"', '"]"', '" ]"', '";"', '"}"') == '"["':
            self._scan('"["')
            expression = self.expression()
            self._scan('"]"')

    def expr_c(self):
        expr_d = self.expr_d()
        while self._peek('"*"', '"/"', '"%"', '"+"', '"-"', '"=="', '"!="', '"<"', '"<="', '">"', '">="', '"and"', '"or"', '","', '":"', '")"', '"]"', '" ]"', '";"', '"}"') in ['"*"', '"/"', '"%"']:
            _token_ = self._peek('"*"', '"/"', '"%"')
            if _token_ == '"*"':
                self._scan('"*"')
            elif _token_ == '"/"':
                self._scan('"/"')
            else:# == '"%"'
                self._scan('"%"')
            expr_d = self.expr_d()

    def expr_b(self):
        expr_c = self.expr_c()
        while self._peek('"*"', '"/"', '"%"', '"+"', '"-"', '"=="', '"!="', '"<"', '"<="', '">"', '">="', '"and"', '"or"', '","', '":"', '")"', '"]"', '" ]"', '";"', '"}"') in ['"+"', '"-"']:
            _token_ = self._peek('"+"', '"-"')
            if _token_ == '"+"':
                self._scan('"+"')
            else:# == '"-"'
                self._scan('"-"')
            expr_c = self.expr_c()

    def relational_op(self):
        _token_ = self._peek('"=="', '"!="', '"<"', '"<="', '">"', '">="')
        if _token_ == '"=="':
            self._scan('"=="')
        elif _token_ == '"!="':
            self._scan('"!="')
        elif _token_ == '"<"':
            self._scan('"<"')
        elif _token_ == '"<="':
            self._scan('"<="')
        elif _token_ == '">"':
            self._scan('">"')
        else:# == '">="'
            self._scan('">="')

    def expr_a(self):
        expr_b = self.expr_b()
        while self._peek('"*"', '"/"', '"%"', '"+"', '"-"', '"=="', '"!="', '"<"', '"<="', '">"', '">="', '"and"', '"or"', '","', '":"', '")"', '"]"', '" ]"', '";"', '"}"') in ['"=="', '"!="', '"<"', '"<="', '">"', '">="']:
            relational_op = self.relational_op()
            expr_b = self.expr_b()

    def expression(self):
        expr_a = self.expr_a()
        while self._peek('"*"', '"/"', '"%"', '"+"', '"-"', '"=="', '"!="', '"<"', '"<="', '">"', '">="', '"and"', '"or"', '","', '":"', '")"', '"]"', '" ]"', '";"', '"}"') in ['"and"', '"or"']:
            _token_ = self._peek('"and"', '"or"')
            if _token_ == '"and"':
                self._scan('"and"')
            else:# == '"or"'
                self._scan('"or"')
            expr_a = self.expr_a()

    def boolean_expression(self):
        identifier = self._scan('identifier')
        relational_op = self.relational_op()
        identifier = self._scan('identifier')

    def l_value_decoration(self):
        _token_ = self._peek('"&"', '"["')
        if _token_ == '"&"':
            self._scan('"&"')
        else:# == '"["'
            self._scan('"["')
            expression = self.expression()
            self._scan('"]"')

    def l_value(self):
        identifier = self._scan('identifier')
        while self._peek('"&"', '"["', '":="') != '":="':
            l_value_decoration = self.l_value_decoration()

    def io_statement(self):
        _token_ = self._peek('"input"', '"output"')
        if _token_ == '"input"':
            self._scan('"input"')
        else:# == '"output"'
            self._scan('"output"')
        identifier_list = self.identifier_list()

    def if_statement(self):
        self._scan('"if"')
        boolean_expression = self.boolean_expression()
        self._scan('"then"')
        while self._peek('"end"', '"input"', '"output"', '"if"', '"while"', 'identifier', '"var"') != '"end"':
            statement = self.statement()
        self._scan('"end"')

    def while_statement(self):
        self._scan('"while"')
        boolean_expression = self.boolean_expression()
        self._scan('"do"')
        while self._peek('"end"', '"input"', '"output"', '"if"', '"while"', 'identifier', '"var"') != '"end"':
            statement = self.statement()
        self._scan('"end"')

    def assignment(self):
        l_value = self.l_value()
        self._scan('":="')
        expression = self.expression()

    def declaration(self):
        self._scan('"var"')
        identifier_list = self.identifier_list()
        self._scan('":"')
        type_expression = self.type_expression()
        self._scan('":="')
        expression = self.expression()

    def statement(self):
        _token_ = self._peek('"input"', '"output"', '"if"', '"while"', 'identifier', '"var"')
        if _token_ in ['"input"', '"output"']:
            io_statement = self.io_statement()
        elif _token_ == '"if"':
            if_statement = self.if_statement()
        elif _token_ == '"while"':
            while_statement = self.while_statement()
        elif _token_ == 'identifier':
            assignment = self.assignment()
        else:# == '"var"'
            declaration = self.declaration()
        self._scan('";"')

    def program(self):
        while self._peek('"input"', '"output"', '"if"', '"while"', 'identifier', '"var"', '"end"') != '"end"':
            statement = self.statement()


def parse(rule, text):
    P = LED(LEDScanner(text))
    return wrap_error_reporter(P, rule)

if __name__ == '__main__':
    from sys import argv, stdin
    if len(argv) >= 2:
        if len(argv) >= 3:
            f = open(argv[2],'r')
        else:
            f = stdin
        print(parse(argv[1], f.read()))
    else: print('Args:  <rule> [<filename>]')
