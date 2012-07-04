###################python##################

def identifierlist_node():
    pass
def generic_node():
    pass
def basic_type_node():
    pass
def type_decoration_node():
    pass
def type_expression_node():
    pass 
def bool_literal_node():
    pass 
def list_literal_node():
    pass 
def map_entry_node():
    pass
def map_literal_node():
    pass
def value_node():
    pass
def expr_e_node():
    pass
def expr_d_node():
    pass
def expr_c_node():
    pass
def expr_b_node():
    pass
def relational_op_node():
    pass
def expr_a_node():
    pass
def expression_node():
    pass
def boolean_expression_node():
    pass
def l_value_decoration_node():
    pass
def l_value_node():
    pass
def io_statement_node():
    pass
def if_statement_node():
    pass
def while_statement_node():
    pass
def assignment_node():
    pass
def declaration_node():
    pass
def statement_node():
    pass
    
################YAPP grammar###############

parser LED:
	ignore: "(?:\s*(?://[^\n]*\n)?)*"
	token identifier: "([a-zA-Z_][a-zA-Z0-9_]*)"
	token int_literal: "([0-9]+)"
	token real_literal: "([0-9]+\.[0-9]+)"
	token char_literal: "'(.)'"
	token string_literal: "\"([^\"]*)\""
    
	rule identifier_list: identifier ( "," identifier )*

	rule generic: "[" type_expression "]"
	rule basic_type: "int" | "real" | "char" | "bool" | "string" | "list" generic | "map" generic generic
	rule type_decoration: "&" | ( "[" int_literal "]" )
	rule type_expression: basic_type type_decoration*

	rule bool_literal: "true" | "false"
	rule list_literal: "[" ( expression [("," expression)*] ) " ]"
	rule map_entry: expression ":" expression
	rule map_literal: "{" [ map_entry ("," map_entry )* ] "}"

	rule value: identifier | real_literal | char_literal | bool_literal | string_literal | list_literal | map_literal
	rule expr_e: value | "(" expression ")"
	rule expr_d: ["not"] ["&"] expr_e [ "[" expression "]" ]
	rule expr_c: expr_d ( ( "*" | "/" | "%" ) expr_d )*
	rule expr_b: expr_c ( ( "+" | "-" ) expr_c )*
	rule relational_op: "==" | "!=" | "<" | "<=" | ">" | ">="
	rule expr_a: expr_b (relational_op expr_b )*
	rule expression: expr_a ( ( "and" | "or" )  expr_a )*
    rule boolean_expression: (identifier relational_op identifier)
    rule l_value_decoration: "&" | ( "[" expression "]" ) 
    rule l_value: identifier l_value_decoration*
    
    rule io_statement: ( "input" | "output" ) identifier_list
	rule if_statement: "if" boolean_expression "then" statement* "end"
	rule while_statement: "while" boolean_expression "do" statement* "end"
	rule assignment: l_value ":=" expression
	rule declaration: "var" identifier_list ":" type_expression [ ":=" expression ]

	rule statement: io_statement | if_statement | while_statement | assignment | declaration";"

	rule program: statement* {{ ast = []}}}
