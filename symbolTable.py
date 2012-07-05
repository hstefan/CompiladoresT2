import ast
import type_inference

table_name_symbom = ['int', 'rea', 'char', 'bool', 'string', 'list']

class SymbolTable:
    def __init__(self):
        self.tabela_simbolos = {} #(escopo, nomevar) : (tipo, tamanho, endereço)
        self.endereco = 0

    def buildSymbolTableNode(self, node):
        if isinstance( node, ast.VariableDeclaration):
            tamanho = type_inference.type_size(node.type_expr)
            if isinstance(node.type_expr, ast.TypeArray):
                type_expr_node = node.type_expr.subtype
            elif isinstance(node.type_expr, ast.TypeReference):
                type_expr_node = node.type_expr.subtype
            else:
                type_expr_node = node.type_expr
            
            #Caso o tamanho não é compatível na hora de colocar na tabela
            #arrumar o endereço que a variável será adicionada
            if tamanho % 4 == 0:
                while self.endereco % 4 != 0:
                    self.endereco += 1

            #se já existe uma variável com o mesmo nome, chama uma exception
            if self.tabela_simbolos.get(('escopo', node.names)) == None:
                self.tabela_simbolos[('escopo', node.names)] = (type_expr_node, tamanho, self.endereco)
                self.endereco += tamanho
            else:
                raise Exception("Dual statement occured!")
            
    def printSymbolTable(self):
        print("|------------------------------------------------------|")
        print("|                    Symbol Table                      |")
        print("|------------------------------------------------------|")
        print("|     escopo      nomevar       tipo  tamanho endereço |")
        print("|------------------------------------------------------|")
        for x in self.tabela_simbolos:
            print("|" , "%10s" % str(x[0]) ,  "%12s" % str(x[1]),  "%10s" % table_name_symbom[self.tabela_simbolos[x][0]] ,
                  "%8s" % str(self.tabela_simbolos[x][1]) , "%8s" % str(self.tabela_simbolos[x][2]) ,"|")
        print("|------------------------------------------------------|")
        
    def testCase(self):
        a = ast.VariableDeclaration('a', ast.BasicType.INT, 2)
        a2 = ast.VariableDeclaration('a2', ast.BasicType.INT, 2)
        c = ast.VariableDeclaration('c', ast.BasicType.CHAR, 'c')
        c2 = ast.VariableDeclaration('c2', ast.BasicType.CHAR, 'c2')
        b = ast.VariableDeclaration('b', ast.BasicType.BOOL, "true")
        l = ast.VariableDeclaration('vetornovo', ast.TypeArray(ast.BasicType.INT, 15), '[15]')
        b2 = ast.VariableDeclaration('b2', ast.BasicType.BOOL, "false")
        self.buildSymbolTableNode(a)
        self.buildSymbolTableNode(c)
        self.buildSymbolTableNode(c2)
        self.buildSymbolTableNode(a2)
        self.buildSymbolTableNode(b)
        self.buildSymbolTableNode(l)
        self.buildSymbolTableNode(b2)
        self.tabela_simbolos
        self.printSymbolTable()
