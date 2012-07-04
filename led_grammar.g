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

	rule identifier_list: identifier ( "," identifier )*                                                  {{return (identifier)}}

	rule generic: "\[" type_expression "\]"                                                               {{return ("TODO","lapergunta")}}
	rule basic_type: "int"      {{return "int"}}
	| "real"                    {{return "real"}}
	| "char"                    {{return "char"}}
	| "bool"                    {{return "bool"}}
	|	"string"                {{return "string"}}
	| "list" generic            {{return "listTODO"}}
	| "map" generic generic     {{return "mapTODO"}}
	rule type_decoration: "&"   {{return ("&TODO")}}
	| ( "\[" int_literal "\]" ) {{return ("type","decorationTODO")}}
	rule type_expression: basic_type type_decoration*     {{return basic_type}}

	rule bool_literal: "true" {{return ("bool_literal", "true")}}
					| "false" {{return ("bool_literal", "false")}}

	rule list_literal: "\[" ( expression [("," expression)*] ) " \]"                                      {{return ("TODO","lapergunta")}}
	rule map_entry: expression ":" expression                                                             {{return ("TODO","lapergunta")}}
	rule map_literal: "{" [ map_entry ("," map_entry )* ] "}"                                             {{return ("TODO","lapergunta")}}

	rule value: identifier {{return ("TODO","lapergunta")}}
	| real_literal {{return ("TODO","lapergunta")}}
	| char_literal {{return ("TODO","lapergunta")}}
	| bool_literal {{return ("TODO","lapergunta")}}
	| string_literal {{return ("TODO","lapergunta")}}
	| list_literal {{return ("TODO","lapergunta")}}
	| map_literal   {{return ("TODO","lapergunta")}}

	rule expr_e: value | "\(" expression "\)"    {{return ("TODO","lapergunta")}}
	rule expr_d: ["not"] ["&"] expr_e [ "\[" expression "\]" ] {{return ("TODO","lapergunta")}}
	rule expr_c: expr_d ( ( "\*" | "/" | "%" ) expr_d )*       {{return ("TODO","lapergunta")}}
	rule expr_b: expr_c ( ( "\+" | "-" ) expr_c )*             {{return ("TODO","lapergunta")}}
	rule relational_op: "==" | "!=" | "<" | "<=" | ">" | ">="  {{return ("TODO","lapergunta")}}
	rule expr_a: expr_b (relational_op expr_b )*               {{return ("TODO","lapergunta")}}
	rule expression: expr_a ( ( "and" | "or" )  expr_a )*      {{return ("TODO","lapergunta")}}

    rule boolean_expression: (identifier relational_op identifier) {{return ("TODO","lapergunta")}}
    rule l_value_decoration: "&" | ( "\[" expression "\]" )  {{return ("TODO","lapergunta")}}
    rule l_value: identifier l_value_decoration*    {{return ("TODO","lapergunta")}}    rule io_statement: ( "input" | "output" ) identifier_list                      {{return ("TODO","lapergunta")}}
	rule if_statement: "if" boolean_expression "then" statement* "end"             {{return ("TODO","lapergunta")}}
	rule while_statement: "while" boolean_expression "do" statement* "end"         {{return ("TODO","lapergunta")}}
	rule assignment: l_value ":=" expression                                       {{return ("TODO","lapergunta")}}
	rule declaration: "var" identifier_list ":" type_expression [":=" expression] {{return (type_expression, identifier_list) }}

	rule statement: ( io_statement ) ";"  {{return ("io_statement","TODO")}}
                  | ( if_statement ) ";" {{return ("if_statement","TODO")}}
				  | ( while_statement ) ";" {{return ("while_statement","TODO")}}
				  | ( assignment ) ";" {{return ("assignment","TODO")}}
				  | ( declaration ) ";" {{return ("declaration", declaration)}}


	rule program:
                             {{e = [] }}
				   statement {{ e.append(statement) }}
				             {{return e }}

