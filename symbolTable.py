import ast
import type_inference

class SymbolTable:
    def __init__(self):
        self.tabela_simbolos = {} #(escopo, nomevar) : (tipo, tamanho, endereço)
        self.endereco = 0

    def buildSymbolTableNode(self, node):
        if isinstance( node, ast.VariableDeclaration):
            tamanho = type_inference.type_size(node.type_expr)

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

    def testCase(self):
        a = ast.VariableDeclaration('a', ast.BasicType.INT, 2)
        a2 = ast.VariableDeclaration('a2', ast.BasicType.INT, 2)
        c = ast.VariableDeclaration('c', ast.BasicType.CHAR, 'c')
        c2 = ast.VariableDeclaration('c2', ast.BasicType.CHAR, 'c2')
        b = ast.VariableDeclaration('b', ast.BasicType.BOOL, "true")
        b2 = ast.VariableDeclaration('b2', ast.BasicType.BOOL, "false")
        self.buildSymbolTableNode(a)
        self.buildSymbolTableNode(c)
        self.buildSymbolTableNode(c2)
        self.buildSymbolTableNode(a2)
        self.buildSymbolTableNode(b)
        self.buildSymbolTableNode(b2)
        self.tabela_simbolos
        self.printSymbolTable()
