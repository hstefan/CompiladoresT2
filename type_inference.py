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
            self.placed = True
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
        self.placed = False

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
        self.modl = None

sz_table = {ast.BasicType.INT : 4, ast.BasicType.REAL : 4, ast.BasicType.CHAR : 1, ast.BasicType.BOOL : 1,
        ast.BasicType.STRING : 8, ast.BasicType.LIST : 8}

any_rel = Any('==', '!=', '<', '<=', '>', '>=')
any_math = Any('+', '-', '*', '/', '%')
any_bool = Any('and', 'or')

placeholder = Placeholder()
p_math = PlaceholderAny(ast.BasicType(ast.BasicType.INT), ast.BasicType(ast.BasicType.REAL))

op_table = [
        (placeholder, any_rel, placeholder, lambda: ast.BasicType(ast.BasicType.BOOL)),
        (p_math, any_math, p_math, lambda: p_math.model),
        (ast.BasicType(ast.BasicType.LIST), '+', placeholder, lambda: placeholder.model),
        (ast.BasicType(ast.BasicType.STRING), '+', Any(ast.BasicType(ast.BasicType.CHAR), ast.BasicType(ast.BasicType.STRING)),
            lambda: ast.BasicType(ast.BasicType.STRING)),
        (ast.BasicType(ast.BasicType.BOOL), any_bool, ast.BasicType(ast.BasicType.BOOL), lambda: ast.BasicType(ast.BasicType.BOOL)),
        (ast.BasicType(ast.BasicType.INT), any_math, ast.BasicType(ast.BasicType.REAL), lambda: ast.BasicType(ast.BasicType.REAL)),
        (ast.BasicType(ast.BasicType.REAL), any_math, ast.BasicType(ast.BasicType.INT), lambda: ast.BasicType(ast.BasicType.REAL)),
        (placeholder, '[]', ast.BasicType(ast.BasicType.INT), lambda: placeholder.model),
        ]

def infer_type(expr_node, var_table):
    table = defaultdict(null, {ast.Expression : infer_expression})
    expr_node.accept(table)

def infer_lvalue(expr_node, var_table):
    if expr_node.resolved_type is None:
        if isinstance(expr_node, ast.LValueDereference):
            expr_node.resolved_type = infer_lvalue(expr_node.subexpr, var_table)
        elif isinstance(expr_node, ast.LValueIndex):
            sub_expr_t = infer_lvalue(expr_node.subexpr, var_table)
            index_t = infer_expression(expr_node.index_expression, var_table)

            if not isinstance(index_t, ast.BasicType) or index_t.type_ != ast.BasicType.INT:
                raise InferenceError("Index must be int.")

            print(type(expr_node.subexpr), str(expr_node.subexpr))
            print(type(sub_expr_t))
            if isinstance(sub_expr_t, ast.BasicType) and sub_expr_t.type_ == ast.BasicType.LIST:
                    expr_node.resolved_type = infer_lvalue(sub_expr_t.generic, var_table)
            elif isinstance(sub_expr_t, ast.TypeArray):
                    expr_node.resolved_type = sub_expr_t.subtype
            else:
                raise InferenceError('Index lvalues are defined only for lists and arrays.')
        elif isinstance(expr_node, ast.LValueVariable):
            expr_node.resolved_type = var_table[expr_node.identifier][0]
        else:
            raise InferenceError(str(expr_node))

    return expr_node.resolved_type

def infer_expression(expr_node, var_table):
    if expr_node.resolved_type is None:
        if isinstance(expr_node, ast.BinaryOp):
            expr_node.resolved_type = match_binary(
                    infer_expression(expr_node.arg_a, var_table),
                    infer_expression(expr_node.arg_b, var_table),
                    expr_node.op_type)
        elif isinstance(expr_node, ast.UnaryOp):
            expr_node.resolved_type = match_unary(
                    infer_expression(expr_node.arg, var_table),
                    expr_node.op_type)
        elif isinstance(expr_node, ast.Variable):
            expr_node.resolved_type = var_table[expr_node.identifier][0]
        elif isinstance(expr_node, ast.Literal):
            if expr_node.type_ == ast.BasicType.LIST:
                res_type = None
                for expr in expr_node.value:
                    if not res_type:
                        res_type = infer_expression(expr, var_table)
                    else:
                        if infer_expression(expr, var_table) != res_type:
                            raise InferenceError("List must have only one type.")
                if not res_type:
                    raise InferenceError("List literals must have at least one expression.")
                else:
                    expr_node.resolved_type = ast.BasicType(ast.BasicType.LIST, res_type)
            else:
                expr_node.resolved_type = ast.BasicType(expr_node.type_)

    return expr_node.resolved_type

def match_binary(type_left, type_right, op_type):
    for entry in op_table:
        placeholder.reset()
        p_math.reset()

        e_left, e_op, e_right, e_result = entry
        if e_op == op_type and e_left == type_left and e_right == type_right:
            return e_result()

    raise InferenceError("No matches for {0} {1} {2}".format(type_left, op_type, type_right))

def match_unary(type_, op_type):
    if op_type == 'not':
        if type_ == ast.BasicType(ast.BasicType.BOOL):
            return type_
        else:
            raise InferenceError("Expected boolean argument, got %s", infered.__str__())
    elif op_type == '&':
        return ast.TypeReference(type_)

def type_size(type_node):
    if isinstance(type_node, ast.BasicType):
        return sz_table[type_node.type_]
    elif isinstance(type_node, ast.TypeReference):
        return 8 #ptr size
    elif isinstance(type_node, ast.TypeArray):
        return type_size(type_node.subtype) * type_node.size
    elif isinstance(type_node, int):
        return sz_table[type_node]

