class Node:
    pass

# Root node
class Program(Node):
    def __init__(self, statements):
        self.statements = statements # [Statement]

### Types #################################################

class TypeExpression(Node):
    pass

class TypeReference(TypeExpression):
    def __init__(self, subtype):
        self.subtype = subtype # TypeExpression

class TypeArray(TypeExpression):
    def __init__(self, subtype, size):
        self.subtype = subtype # TypeExpression
        self.size = size # int

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

### l-values ##############################################

class LValue(Node):
    pass

class LValueDereference(LValue):
    def __init__(self, subexpr):
        self.subexpr = subexpr # LValue

class LValueIndex(LValue):
    def __init__(self, subexpr, index_expression):
        self.subexpr = subexpr # LValue
        self.index_expression = index_expression # Expression

class LValueVariable(LValue):
    def __init__(self, identifier):
        self.identifier = identifier # str

### Expressions ###########################################

class Expression(Node):
	def __init__(self):
		self.type_ = None

class BinaryOp(Expression):
    def __init__(self, op_type, arg_a, arg_b):
        self.op_type = op_type # str
        self.arg_a = arg_a # Expression
        self.arg_b = arg_b # Expression
		super.__init__()

class UnaryOp(Expression):
    def __init__(self, op_type, arg):
        self.op_type = op_type # str
        self.arg = arg # Expression
		super.__init__()

class Literal(Expression):
    def __init__(self, value, type_):
        self.value = value
        self.type_ = type_ # Enum in BasicType
		super.__init__()

class Variable(Expression):
    def __init__(self, identifier):
        self.identifier = identifier # str
		super.__init__()

### Statements ############################################

class Statement(Node):
    pass

class InputStatement(Statement):
    def __init__(self, target_list):
        self.target_list = target_list # [LValue]

class OutputStatement(Statement):
    def __init__(self, target_list):
        self.target_list = target_list # [Expression]

class IfStatement(Statement):
    def __init__(self, condition, then_body, else_body):
        self.condition = condition # Expression
        self.then_body = then_body # [Statement]
        self.else_body = else_body # [Statement]

class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition # Expression
        self.body = body # [Statement]

class Assignment(Statement):
    def __init__(self, target, value):
        self.target = target # LValue
        self.value = value # Expression

class VariableDeclaration(Statement):
    def __init__(self, names, type_expr, initializer):
        self.names = names # [str]
        self.type_expr = type_expr # TypeExpression
        self.initializer = initializer # Expression
