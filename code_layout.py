import ast

class BasicBlock:
    def __init__(self):
        self.statements = []
        self.exit = None

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
