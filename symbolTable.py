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
            if tamanho % 4 == 0:
                while self.endereco % 4 != 0:
                    self.endereco += 1

            #se já existe uma variável com o mesmo nome, chama uma exception
            for name in node.names:
                if self.tabela_simbolos.get(name) == None:
                    self.tabela_simbolos[name] = (node.type_expr, tamanho, self.endereco)
                    self.endereco += tamanho
                else:
                    raise Exception("Dual statement occured!")
            
    def printSymbolTable(self):
        print("|-------------------------------------------------|")
        print("|                   Symbol Table                  |")
        print("|-------------------------------------------------|")
        print("|          nomevar         tipo  tamanho endereço |")
        print("|-------------------------------------------------|")
        for x in self.tabela_simbolos:
            print("|" ,  "%16s" % str(x[0]),  "%12s" % str(self.tabela_simbolos[x][0]) ,
                  "%8s" % str(self.tabela_simbolos[x][1]) , "%8s" % str(self.tabela_simbolos[x][2]) ,"|")
        print("|-------------------------------------------------|")
