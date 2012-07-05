class Node:
    def accept(self, table):
        table[Node](self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

# Root node
class Program(Node):
    def __init__(self, statements):
        self.statements = statements # [Statement]

    def __str__(self):
        return '\n'.join(map(str, self.statements))

    def accept(self, table):
        super().accept(table)
        table[Program](self)

        for statement in self.statements:
            statement.accept(table)

### Types #################################################

class TypeExpression(Node):
    def accept(self, table):
        super().accept(table)
        table[TypeExpression](self)

class TypeReference(TypeExpression):
    def __init__(self, subtype):
        self.subtype = subtype # TypeExpression

    def __str__(self):
        return str(self.subtype) + '&'

    def accept(self, table):
        super().accept(table)
        table[TypeReference](self)

        self.subtype.accept(table)

class TypeArray(TypeExpression):
    def __init__(self, subtype, size):
        self.subtype = subtype # TypeExpression
        self.size = size # int

    def __str__(self):
        return str(self.subtype) + '[' + str(self.size) + ']'

    def accept(self, table):
        super().accept(table)
        table[TypeArray](self)

        self.subtype.accept(table)

class BasicType(TypeExpression):
    INT = 0
    REAL = 1
    CHAR = 2
    BOOL = 3
    STRING = 4
    LIST = 5

    def __init__(self, type_, generic=None):
        self.type_ = type_ # See enum above
        self.generic = generic # TypeExpression

    def __str__(self):
        #move along, nothing to see here
        s = {BasicType.INT : 'int', BasicType.REAL : 'real', BasicType.CHAR : 'char',
            BasicType.BOOL : 'bool', BasicType.STRING : 'string', BasicType.LIST : 'list'}[self.type_]
        if self.generic is not None:
            s += '<' + str(self.generic) + '>'
        return s

    def accept(self, table):
        super().accept(table)
        table[BasicType](self)

        if self.generic is not None:
            self.generic.accept(table)

### l-values ##############################################

class LValue(Node):
    def accept(self, table):
        super().accept(table)
        table[LValue](self)

class LValueDereference(LValue):
    def __init__(self, subexpr):
        self.subexpr = subexpr # LValue

    def __str__(self):
        return str(self.subexpr) + '&'

    def accept(self, table):
        super().accept(table)
        table[LValueDereference](self)
        self.resolved_type = None
        self.subexpr.accept(table)

class LValueIndex(LValue):
    def __init__(self, subexpr, index_expression):
        self.subexpr = subexpr # LValue
        self.resolved_type = None
        self.index_expression = index_expression # Expression

    def __str__(self):
        return str(self.subexpr) + '[' + str(self.index_expression) + ']'

    def accept(self, table):
        super().accept(table)
        table[LValueIndex](self)

        self.subexpr.accept(table)
        self.index_expression.accept(table)

class LValueVariable(LValue):
    def __init__(self, identifier):
        self.identifier = identifier # str
        self.resolved_type = None
    def __str__(self):
        return self.identifier

    def accept(self, table):
        super().accept(table)
        table[LValueVariable](self)

### Expressions ###########################################

class Expression(Node):
    def __init__(self):
        self.resolved_type = None

    def accept(self, table):
        super().accept(table)
        table[Expression](self)

class BinaryOp(Expression):
    def __init__(self, op_type, arg_a, arg_b):
        super().__init__()
        self.op_type = op_type # str
        self.arg_a = arg_a # Expression
        self.arg_b = arg_b # Expression

    def __str__(self):
        return '({0}) {1} ({2})'.format(self.arg_a, self.op_type, self.arg_b)

    def accept(self, table):
        super().accept(table)
        table[BinaryOp](self)

        self.arg_a.accept(table)
        self.arg_b.accept(table)

class UnaryOp(Expression):
    def __init__(self, op_type, arg):
        super().__init__()
        self.op_type = op_type # str
        self.arg = arg # Expression

    def __str__(self):
        return '{0} ({1})'.format(self.op_type, self.arg)

    def accept(self, table):
        super().accept(table)
        table[UnaryOp](self)

        self.arg.accept(table)

class Literal(Expression):
    def __init__(self, value, type_):
        super().__init__()
        self.value = value # Type depends on Literal type
        self.type_ = type_ # Enum in BasicType

    def __str__(self):
        if isinstance(self.value, list):
            return '[' + ', '.join(map(str, self.value)) + ']'
        else:
            return str(self.value)

    def accept(self, table):
        super().accept(table)
        table[Literal](self)

        if isinstance(self.value, Node):
            self.value.accept(table)

class Variable(Expression):
    def __init__(self, identifier):
        super().__init__()
        self.identifier = identifier # str

    def __str__(self):
        return self.identifier

    def accept(self, table):
        super().accept(table)
        table[Variable](self)

### Statements ############################################

class Statement(Node):
    def accept(self, table):
        super().accept(table)
        table[Statement](self)

class InputStatement(Statement):
    def __init__(self, target_list):
        self.target_list = target_list # [LValue]

    def __str__(self):
        return 'input ' + ', '.join(map(str, self.target_list)) + ';'

    def accept(self, table):
        super().accept(table)
        table[InputStatement](self)

        for target in self.target_list:
            target.accept(table)

class OutputStatement(Statement):
    def __init__(self, target_list):
        self.target_list = target_list # [Expression]

    def __str__(self):
        return 'output ' + ', '.join(map(str, self.target_list)) + ';'

    def accept(self, table):
        super().accept(table)
        table[OutputStatement](self)

        for target in self.target_list:
            target.accept(table)

class IfStatement(Statement):
    def __init__(self, condition, then_body, else_body):
        self.condition = condition # Expression
        self.then_body = then_body # [Statement]
        self.else_body = else_body # [Statement]

    def __str__(self):
        s = 'if ' + str(self.condition) + ' then\n'
        s += '\n'.join(map(str, self.then_body)) + '\n'
        if self.else_body is not None:
            s += 'else\n'
            s += '\n'.join(map(str, self.else_body)) + '\n'
        s += 'end;'
        return s

    def accept(self, table):
        super().accept(table)
        table[IfStatement](self)

        self.condition.accept(table)
        for statement in self.then_body:
            statement.accept(table)
        if self.else_body is not None:
            for statement in self.else_body:
                statement.accept(table)

class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition # Expression
        self.body = body # [Statement]

    def __str__(self):
        return ('while ' + str(self.condition) + ' do\n' +
            '\n'.join(map(str, self.body)) + '\n' +
            'end;')

    def accept(self, table):
        super().accept(table)
        table[WhileStatement](self)

        self.condition.accept(table)
        for statement in self.body:
            statement.accept(table)

class Assignment(Statement):
    def __init__(self, target, value):
        self.target = target # LValue
        self.value = value # Expression

    def __str__(self):
        return str(self.target) + ' := ' + str(self.value) + ';'

    def accept(self, table):
        super().accept(table)
        table[Assignment](self)

        self.target.accept(table)
        self.value.accept(table)

class VariableDeclaration(Statement):
    def __init__(self, names, type_expr, initializer):
        self.names = names # [str]
        self.type_expr = type_expr # TypeExpression
        self.initializer = initializer # Expression

    def __str__(self):
        s = 'var ' + ', '.join(map(str, self.names)) + ' : ' + str(self.type_expr)
        if self.initializer is not None:
            s += ' := ' + str(self.initializer)
        return s + ';'

    def accept(self, table):
        super().accept(table)
        table[VariableDeclaration](self)

        self.type_expr.accept(table)
        if self.initializer is not None:
            self.initializer.accept(table)

class ConditionCheck(Statement):
    def __init__(self, condition):
        self.condition = condition # Expression

    def __str__(self):
        return str(self.condition) + '?'

    def accept(self, table):
        super().accept(table)
        table[ConditionCheck](self)

        self.condition.accept(table)
