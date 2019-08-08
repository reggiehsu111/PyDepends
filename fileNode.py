from funcNode import FuncNode
from util import print_tabs
"""
    Class FileNode as a node in the dependency graph
"""
class FileNode():
    def __init__(self, module, alias, functions=None, *depends):
        self.module = module
        self.alias = alias
        self.depends = set(depends)
        self.functions = []
        self.addFunctions(functions)


    def addDependency(self, node):
        self.depends.add(node)

    def addFunctions(self, functions):
        if functions is not None:
            if isinstance(functions, list):
                for func in functions:
                    func = FuncNode(self.module, func)
                    assert isinstance(func, FuncNode)
                    self.functions.append(func)
            else:
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
            print(self.module+" no dependencies")

    def printFunctions(self,depth):
        depth += 1
        for func in self.functions:
            func.print(depth)

    def print(self, depth):
        self.printDependencies(depth)
        self.printFunctions(depth)
        print('')