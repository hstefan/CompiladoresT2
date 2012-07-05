import ast

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

def flatten_blocks(bBlock):
    flattened_blocks = []
    to_visit = [bBlock]
    label_block = 0
    bBlock.label = label_block
    label_block += 1

    while len(to_visit) > 0:
        to_visit[0].visited = True
        to_visit[0].statements.insert(0,'.L' + ('%d' % to_visit[0].label).zfill(4))
        if to_visit[0].exit != None:
            if isinstance(to_visit[0].exit, tuple):
                if to_visit[0].exit[0].visited == False:
                    to_visit[0].exit[0].label = label_block
                    label_block += 1
                    to_visit.append(to_visit[0].exit[0])
                    
                if to_visit[0].exit[1].visited == False:
                    to_visit[0].exit[1].label = label_block
                    label_block += 1
                    to_visit.append(to_visit[0].exit[1])
                to_visit[0].statements.append('jtrue .L' + ('%d' % to_visit[0].exit[0].label).zfill(4))
                to_visit[0].statements.append('jfalse .L' + ('%d' % to_visit[0].exit[1].label).zfill(4))
            else:
                if to_visit[0].exit.visited == False:
                    to_visit[0].exit.label = label_block
                    label_block += 1
                    to_visit.append(to_visit[0].exit)
                to_visit[0].statements.append('jump .L' + ('%d' % to_visit[0].exit.label).zfill(4))
        else:
            to_visit[0].statements.append('halt')
        flattened_blocks.append(to_visit[0].statements)
        to_visit.remove(to_visit[0])
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
                

