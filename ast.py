class Node:
    def accept(self, table):
        table[Node](self)

# Root node
class Program(Node):
    def __init__(self, statements):
        self.statements = statements # [Statement]

    def accept(self, table):
        super().accept(self, table)
        table[Program](self)

        for statement in self.statements:
            statement.accept(table)

### Types #################################################

class TypeExpression(Node):
    def accept(self, table):
        super().accept(self, table)
        table[TypeExpression](self)

class TypeReference(TypeExpression):
    def __init__(self, subtype):
        self.subtype = subtype # TypeExpression

    def __str__(self):
        return self.subtype.__str__() + '&'

    def accept(self, table):
        super().accept(self, table)
        table[TypeReference](self)

        self.subtype.accept(table)

class TypeArray(TypeExpression):
    def __init__(self, subtype, size):
        self.subtype = subtype # TypeExpression
        self.size = size # int

    def __str__(self):
        return self.subtype.__str__() + '[' + str(self.size) + ']'

    def accept(self, table):
        super().accept(self, table)
        table[TypeArray](self)

        self.subtype.accept(table)

class BasicType(TypeExpression):
    INT = 0
    REAL = 1
    CHAR = 2
    BOOL = 3
    STRING = 4
    LIST = 5
    MAP = 6

    def __init__(self, type_, generic=None):
        self.type_ = type_ # See enum above
        self.generic = generic # TypeExpression

    def __str__(self):
        #move along, nothing to see here
        return {BasicType.INT : 'int', BasicType.REAL : 'real', BasicType.CHAR : 'char',
            BasicType.BOOL : 'bool', BasicType.STRING : 'string', BasicType.LIST : 'list',
            BasicType.MAP : 'map'}[self.type_]

    def accept(self, table):
        super().accept(self, table)
        table[BasicType](self)

        self.generic.accept(table)

### l-values ##############################################

class LValue(Node):
    def accept(self, table):
        super().accept(self, table)
        table[LValue](self)

class LValueDereference(LValue):
    def __init__(self, subexpr):
        self.subexpr = subexpr # LValue

    def accept(self, table):
        super().accept(self, table)
        table[LValueDereference](self)

        self.subexpr.accept(table)

class LValueIndex(LValue):
    def __init__(self, subexpr, index_expression):
        self.subexpr = subexpr # LValue
        self.index_expression = index_expression # Expression

    def accept(self, table):
        super().accept(self, table)
        table[LValueIndex](self)

        self.subexpr.accept(table)
        self.index_expression.accept(table)

class LValueVariable(LValue):
    def __init__(self, identifier):
        self.identifier = identifier # str

    def accept(self, table):
        super().accept(self, table)
        table[LValueVariable](self)

### Expressions ###########################################

class Expression(Node):
    def __init__(self):
        self.type_ = None

    def accept(self, table):
        super().accept(self, table)
        table[Expression](self)

class BinaryOp(Expression):
    def __init__(self, op_type, arg_a, arg_b):
        super().__init__()
        self.op_type = op_type # str
        self.arg_a = arg_a # Expression
        self.arg_b = arg_b # Expression

    def accept(self, table):
        super().accept(self, table)
        table[BinaryOp](self)

        self.arg_a.accept(table)
        self.arg_b.accept(table)

class UnaryOp(Expression):
    def __init__(self, op_type, arg):
        super().__init__()
        self.op_type = op_type # str
        self.arg = arg # Expression

    def accept(self, table):
        super().accept(self, table)
        table[UnaryOp](self)

        self.arg.accept(table)

class Literal(Expression):
    def __init__(self, value, type_):
        super().__init__()
        self.value = value # Type depends on Literal type
        self.type_ = type_ # Enum in BasicType

    def accept(self, table):
        super().accept(self, table)
        table[Literal](self)

        if isinstance(self.value, Node):
            self.value.accept(table)

class Variable(Expression):
    def __init__(self, identifier):
        super().__init__()
        self.identifier = identifier # str

    def accept(self, table):
        super().accept(self, table)
        table[Variable](self)

### Statements ############################################

class Statement(Node):
    def accept(self, table):
        super().accept(self, table)
        table[Statement](self)

class InputStatement(Statement):
    def __init__(self, target_list):
        self.target_list = target_list # [LValue]

    def accept(self, table):
        super().accept(self, table)
        table[InputStatement](self)

        for target in self.target_list:
            target.accept(table)

class OutputStatement(Statement):
    def __init__(self, target_list):
        self.target_list = target_list # [Expression]

    def accept(self, table):
        super().accept(self, table)
        table[OutputStatement](self)

        for target in self.target_list:
            target.accept(table)

class IfStatement(Statement):
    def __init__(self, condition, then_body, else_body):
        self.condition = condition # Expression
        self.then_body = then_body # [Statement]
        self.else_body = else_body # [Statement]

    def accept(self, table):
        super().accept(self, table)
        table[IfStatement](self)

        self.condition.accept(table)
        for statement in self.then_body:
            statement.accept(table)
        for statement in self.else_body:
            statement.accept(table)

class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition # Expression
        self.body = body # [Statement]

    def accept(self, table):
        super().accept(self, table)
        table[WhileStatement](self)

        self.condition.accept(table)
        for statement in self.body:
            statement.accept(table)

class Assignment(Statement):
    def __init__(self, target, value):
        self.target = target # LValue
        self.value = value # Expression

    def accept(self, table):
        super().accept(self, table)
        table[Assignment](self)

        self.target.accept(table)
        self.target.accept(value)

class VariableDeclaration(Statement):
    def __init__(self, names, type_expr, initializer):
        self.names = names # [str]
        self.type_expr = type_expr # TypeExpression
        self.initializer = initializer # Expression

    def accept(self, table):
        super().accept(self, table)
        table[VariableDeclaration](self)

        self.type_expr.accept(table)
        self.initializer.accept(table)
