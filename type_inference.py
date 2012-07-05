import ast
from collections import defaultdict

class InferenceError(Exception):
    pass

class Placeholder:
    def __init__(self):
        self.placed = False
    def __eq__(self, other):
        if self.placed:
            return other == self.model
        else:
            self.model = other
            self.placed = False
            return True
    def reset(self):
        self.placed = False
        self.model = None

class Any:
    def __init__(self, *args):
        self.args = args
    def __eq__(self, other):
        return other in self.args

class PlaceholderAny:
    def __init__(self, *args):
        self.args = args
        self.placed = True
    def __eq__(self, other):
        if self.placed:
            return other == self.model
        else:
            if other in self.args:
                self.model = other
                self.placed = True
                return True
            else:
                return False
    def reset(self):
        self.placed = False
        self.model = None

sz_table = {ast.BasicType.INT : 4, ast.BasicType.REAL : 4, ast.BasicType.CHAR : 1, ast.BasicType.BOOL : 1,
        ast.BasicType.STRING : 8, ast.BasicType.LIST : 8}

any_rel = Any('==', '!=', '<', '<=', '>', '>=')
any_math = Any('+', '-', '*', '/', '%')
any_bool = Any('and', 'or')

placeholder = Placeholder()
p_math = PlaceholderAny(ast.BasicType(ast.BasicType.INT), ast.BasicType(ast.BasicType.INT))

op_table = [
        (placeholder, any_rel, placeholder, lambda: ast.BasicType.BOOL),
        (p_math, any_math, p_math, lambda: p_math.model),
        (ast.BasicType(ast.BasicType.LIST), '+', placeholder, lambda: placeholder.model),
        (ast.BasicType(ast.BasicType.STRING), '+', Any(ast.BasicType(ast.BasicType.CHAR), ast.BasicType(ast.BasicType.STRING)),
            lambda: ast.BasicType(ast.BasicType.STRING)),
        (ast.BasicType(ast.BasicType.BOOL), any_bool, ast.BasicType(ast.BasicType.BOOL), lambda: ast.BasicType(ast.BasicType.BOOL)),
        (ast.BasicType(ast.BasicType.INT), any_math, ast.BasicType(ast.BasicType.REAL), lambda: ast.BasicType(ast.BasicType.REAL)),
        (ast.BasicType(ast.BasicType.REAL), any_math, ast.BasicType(ast.BasicType.INT), lambda: ast.BasicType(ast.BasicType.REAL)),
        ]

def infer_type(expr_node, var_table):
    table = defaultdict(null, {ast.Expression : infer_expression})
    expr_node.accept(table)

def infer_expression(expr_node, var_table):
    if isinstance(expr_node, ast.BinaryOp):
        expr_node.type_ = match_binary(infer_expression(expr_node.arg_a),
        infer_expression(expr_node.arg_b), expr_node.op_type)
    elif isinstance(expr_node, ast.UnaryOp):
        expr_node.type_ = match_unary(infer_expression(expr_node.arg), expr_node.op_type)
    elif isinstance(expr_node, ast.Variable):
        expr_node.type_ = var_table[expr_node.identifier]
    return expr_node.type_

def match_binary(arg_a, arg_b, op_type):
    cur_left = infer_expression(arg_a)
    cur_right = infer_expression(arg_b)

    for i in range(0, len(op_table)):
        placeholder.reset()
        p_math.reset()
        match = op_table[i][1] == op_type and op_table[i][0] == cur_left and op_table[i][2] == cur_right
        if match:
            return op_table[i][3]
    raise InferenceException("No matches for %s %s %s", cur_left.__str__(), op_type, cur_right.__str__())

def match_unary(arg, op):
    if op_type == 'not':
        infered = infer_expression(arg)
        if infered == ast.BasicType.BOOL:
            return ast.BasicType(st.BasicType.BOOL)
        else:
            raise InferenceError("Expected boolean argument, got %s", infered.__str__())
    elif op_type == '&':
        return ast.TypeReference(arg)

def type_size(type_node):
    if isinstance(type_node, ast.BasicType):
        return sz_table[type_node.type_]
    elif isinstance(type_node, ast.TypeReference):
        return 8 #ptr size
    elif isinstance(type_node, ast.TypeArray):
        return type_size(type_node.subtype) * type_node.size
    elif isinstance(type_node, int):
        return sz_table[type_node]
