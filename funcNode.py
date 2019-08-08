from util import print_tabs
"""
    Class FuncNode as a sub-node to fileNode
"""

class FuncNode():
    def __init__(self, file, alias=None, *depends):
        # file points to the fileNode that contains the function node
        self.file= file
        self.alias = alias
        self.depends = set(depends)


    def addDependency(self, node):
        self.depends.add(node)

    def print(self, depth):
        if len(self.depends) > 0:
            print_tabs(depth)
            print("Function:", self.alias) 
            print_tabs(depth)
            print("\tFunction dependencies: ")
            print_tabs(depth)
            for elem in self.depends:
                print("\t\t",elem)
        else:
            print_tabs(depth)
            print("Function:", self.alias)
            print_tabs(depth) 
            print(self.alias+" no dependencies")