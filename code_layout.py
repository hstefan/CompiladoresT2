import ast
import codegen

class BasicBlock:
    def __init__(self):
        self.statements = []
        self.exit = None
        self.visited = False
        self.label = -1

def split_statement_list(statements):
    head_block = BasicBlock()
    current_block = head_block

    for stmt in statements:
        if isinstance(stmt, (ast.InputStatement, ast.OutputStatement, ast.Assignment)):
            current_block.statements.append(stmt)
        elif isinstance(stmt, ast.VariableDeclaration):
            # Convert variable declarations with initializers to assignments
            if stmt.initializer is not None:
                current_block.statements += [
                        ast.Assignment(ast.LValueVariable(name), stmt.initializer)
                        for name in stmt.names]
        elif isinstance(stmt, ast.IfStatement):
            new_block = BasicBlock()

            current_block.statements.append(ast.ConditionCheck(stmt.condition))

            then_head, then_tail = split_statement_list(stmt.then_body)
            then_tail.exit = new_block

            if stmt.else_body is not None:
                else_head, else_tail = split_statement_list(stmt.else_body)
                else_tail.exit = new_block
                current_block.exit = (then_head, else_head)
            else:
                current_block.false_exit = new_block
                current_block.exit = (then_head, new_block)

            current_block = new_block
        elif isinstance(stmt, ast.WhileStatement):
            new_block = BasicBlock()

            head, tail = split_statement_list(stmt.body)

            check = ast.ConditionCheck(stmt.condition)

            current_block.statements.append(check)
            tail.statements.append(check)

            current_block.exit = (head, new_block)
            tail.exit = (head, new_block)

            current_block = new_block

    return head_block, current_block

def codegen_block(block):
    ctx = codegen.EmitContext()
    for stmt in block.statements:
        codegen.emit_statement(stmt, ctx)
    block.statements = ctx.instructions

def flatten_blocks(bBlock):
    flattened_blocks = []
    to_visit = [bBlock]
    next_label = 0

    def get_label(b):
        if b.label is None:
            b.label = next_label
            next_label += 1
        return b.label

    while len(to_visit) > 0:
        current = to_visit.pop(0)
        if current.visited:
            continue
        current.visited = True

        codegen_block(current)

        flattened_blocks.insert(0, '.L%3d' % get_label(current))
        flattened_blocks += current.statements
        if current.exit != None:
            if isinstance(current.exit, tuple):
                true_exit, false_exit = current.exit
                current.statements.append('jtrue .L%3d' % get_label(true_exit))
                current.statements.append('jfalse .L%3d' % get_label(false_exit))
            else:
                current.statements.append('jump .L%3d' % get_label(current.exit))
        else:
            current.statements.append('halt')
    return flattened_blocks

def tester_flatten_blocks():
    b = BasicBlock()
    b.statements.append("int i = 0");
    c = BasicBlock()
    c.statements.append("while x < 10")
    c.statements.append("x++;")
    cf = BasicBlock()
    cf.statements.append("FALSE")
    b.exit = (c)
    c.exit = (c, cf)
    l = flatten_blocks(b)
    for x in l:
        for command in x:
            if(command[0] != '.'):
                print("    " + command)
            else:
                print(command)
