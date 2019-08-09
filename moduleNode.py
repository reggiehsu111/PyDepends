from funcNode import FuncNode
from util import print_tabs
"""
    Class ModuleNode as a node in the ast dependency graph
    Store in FGC
"""
class ModuleNode():
    def __init__(self, module, alias, functions=None, *depends):
        """
            Params:
                module:     String type arg
                alias:      String type arg
                functions:  List of string or strings
            Attributes:
                self.functions:     List of funcNodes
                self.functionNames: List of strings
        """
        self.module = module
        self.alias = alias
        self.depends = set(depends)
        self.functions = []
        self.functionNames = []
        self.addFunctions(functions)


    def addDependency(self, node):
        self.depends.add(node)

    def addFunctions(self, functions):
        if functions is not None:
            if isinstance(functions, list):
                for func in functions:
                    self.functionNames.append(func)
                    func = FuncNode(self.module, func)
                    assert isinstance(func, FuncNode)
                    self.functions.append(func)
            else:
                self.functionNames.append(functions)
                functions = FuncNode(self.module, functions)
                assert isinstance(functions, FuncNode)
                self.functions.append(functions)

    def printDependencies(self,depth):
        if len(self.depends) > 0:
            print_tabs(depth)
            print("Module:", self.module) 
            print_tabs(depth)
            print("\tFile", self.module ,"Dependencies: ")
            for elem in self.depends:
                print_tabs(depth)
                print("\t\t",elem)
        else:
            print_tabs(depth)
            print("Module:", self.module)
            print_tabs(depth)
            print("File "+self.module+" no dependencies")

    def printFunctions(self,depth):
        depth += 1
        for func in self.functions:
            func.print(depth)

    def print(self, depth):
        self.printDependencies(depth)
        print_tabs(depth)
        print("alias:",self.alias)
        self.printFunctions(depth)
        print('')