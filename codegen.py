import ast

class EmitContext:
    def __init__(self):
        self.instructions = []
        self.next_tmp = 0

    def reserve_tmp(self):
        cur = self.next_tmp
        self.next_tmp += 1
        return '_' + str(cur)

    def free_tmp(self, arg):
        if arg[0] == '_':
            self.next_tmp -= 1

    def emit_instruction(self, instruction, args):
        self.instructions.append(instruction + ' ' + ', '.join(args))

def get_short_type(type_):
    if isinstance(type_, ast.TypeReference):
        return 'ref'
    elif isinstance(type_, ast.TypeArray):
        return 'array'
    elif isinstance(type_, ast.BasicType):
        return str(type_)

def emit_list_literal(expr, ctx):
    pass
    # TODO

def emit_expression(expr, ctx):
    if isinstance(expr, ast.Variable):
        return '%' + expr.identifier
    elif isinstance(expr, ast.Literal):
        if expr.type_ == ast.BasicType.LIST:
            return emit_list_literal(expr, ctx)
        else:
            return '#' + str(expr.value)
    elif isinstance(expr, ast.UnaryOp):
        unary_ops = {
                'not': 'not', '&': 'ref'
                }
        short_type = get_short_type(expr.resolved_type)

        arg = emit_expression(expr.arg, ctx)

        ctx.free_tmp(arg)
        result = ctx.reserve_tmp()

        ctx.emit_instruction(unary_ops[expr.op_type] + '.' + short_type, (result, arg))
        return result
    elif isinstance(expr, ast.BinaryOp):
        binary_ops = {
                '+': 'add', '-': 'sub', '*': 'mul', '/': 'div', '%': 'mod',
                'and': 'and', 'or': 'or',
                '==': 'eq', '!=': 'neq',
                '<': 'lt', '<=': 'leq', '>': 'gt', '>=': 'gte'
                }
        short_type = get_short_type(expr.resolved_type)

        arg_b = emit_expression(expr.arg_b, ctx)
        arg_a = emit_expression(expr.arg_a, ctx)

        ctx.free_tmp(arg_a)
        ctx.free_tmp(arg_b)
        result = ctx.reserve_tmp()

        ctx.emit_instruction(binary_ops[expr.op_type] + '.' + short_type, (result, arg_a, arg_b))
        return result

def emit_statement(stmt, ctx):
    if isinstance(stmt, ast.InputStatement):
        pass
        # TODO
    elif isinstance(stmt, ast.OutputStatement):
        for expr in stmt.target_list:
            short_type = get_short_type(expr.resolved_type)
            arg = emit_expression(expr, ctx)

            ctx.free_tmp(arg)
            ctx.emit_instruction('output.' + short_type, (arg,))
    elif isinstance(stmt, ast.Assignment):
        pass
        # TODO
    elif isinstance(stmt, ast.ConditionCheck):
        arg = emit_expression(expr, ctx)

        ctx.free_tmp(arg)
        ctx.emit_instruction('test', (arg,))
