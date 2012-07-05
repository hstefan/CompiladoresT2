import ast
from collections import defaultdict

op_table = []

sz_table = {ast.BasicType.INT : 4, ast.BasicType.REAL : 4, ast.BasicType.CHAR : 1, ast.BasicType.BOOL : 1,
        ast.BasicType.STRING : 8, ast.BasicType.LIST : 8}

class InferenceError(Exception):
    pass

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
   
   return expr_nod.type_
def match_binary(arg_a, arg_b, op_type):
    inf_a = infer_expression(arg_a)
    inf_b = infer_expression(arg_b)

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
        return type_size(type_node.subtype * type_node.size)

