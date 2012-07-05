import ast

class SymbolTable:
    def __init__(self):
        self.tabela_simbolos = {} #(escopo, nomevar) : (tipo, tamanho, endereço)
        self.endereco = 0
        self.tamanhos = {'int' : 4 , 'char' : 1 , 'bool' : 1 }

    def buildSymbolTableNode(self, node):
        if isinstance( node, ast.VariableDeclaration):
            tamanho = self.tamanhos[node.type_expr]

            #Caso o tamanho não é compatível na hora de colocar na tabela
            #arrumar o endereço que a variável será adicionada
            while self.endereco % tamanho != 0:
                 self.endereco += 1

            #se já existe uma variável com o mesmo nome, chama uma exception
            if self.tabela_simbolos.get(('escopo', node.names)) == None:
                self.tabela_simbolos[('escopo', node.names)] = (node.type_expr, tamanho, self.endereco)
                self.endereco += tamanho
            else:
                raise Exception("Dual statement occured!")
            
    def printSymbolTable(self):
        print("Symbol Table:")
        print("(escopo, nomevar, tipo, tamanho, endereço)")
        for x in self.tabela_simbolos:
            print(x + self.tabela_simbolos[x])

a = ast.VariableDeclaration('a','int',2)
a2 = ast.VariableDeclaration('a2','int',2)
c = ast.VariableDeclaration('c','char','c')
c2 = ast.VariableDeclaration('c2','char','c2')
b = ast.VariableDeclaration('b','bool',"true")
b2 = ast.VariableDeclaration('b2','bool',"false")
stable = SymbolTable()
stable.buildSymbolTableNode(a)
stable.buildSymbolTableNode(c)
stable.buildSymbolTableNode(c2)
stable.buildSymbolTableNode(a2)
stable.buildSymbolTableNode(b)
stable.buildSymbolTableNode(b2)
stable.tabela_simbolos
stable.printSymbolTable()
