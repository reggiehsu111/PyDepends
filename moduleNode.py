from util import print_tabs

"""
    Class ObjectNode as a sub-node to moduleNode
    To store imported function/class/filename after parsing through Import/ImportFrom AST nodes
"""

class ObjectNode():
    def __init__(self, file, alias=None, *depends):
        # file points to the moduleNode that contains the obj node
        self.file= file
        self.alias = alias
        self.depends = set(depends)

    def __repr__(self):
        return self.file + '.' + self.alias

    def addDependency(self, node):
        self.depends.add(node)

    def print(self, depth):
        if len(self.depends) > 0:
            print_tabs(depth)
            print("Object:", self.alias) 
            print_tabs(depth)
            print("\tObject dependencies: ")
            print_tabs(depth)
            for elem in self.depends:
                print("\t\t",elem)
        else:
            print_tabs(depth) 
            print("Object "+self.alias+" no dependencies")

"""
    Class ModuleNode as a node in the ast dependency graph
    Store in FGC
"""
class ModuleNode():
    def __init__(self, module, alias, obj=None, *depends):
        """
            Params:
                module:     String type arg
                obj:  List of string or strings
            Attributes:
                self.objs:     List of funcNodes
                self.objectNames: List of strings containing obj names
        """
        self.module = module
        self.depends = set(depends)
        self.objs = []
        self.objectNames = []
        self.alias = alias
        self.addObjects(obj)



    def addDependency(self, node):
        self.depends.add(node)

    def addObjects(self, obj):
        if obj is not None:
            if isinstance(obj, list):
                for func in obj:
                    self.objectNames.append(func)
                    func = ObjectNode(self.module, func)
                    assert isinstance(func, ObjectNode)
                    self.objs.append(func)
            else:
                self.objectNames.append(obj)
                obj = ObjectNode(self.module, obj)
                assert isinstance(obj, ObjectNode)
                self.objs.append(obj)


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

    def printObjects(self,depth):
        depth += 1
        for func in self.objs:
            func.print(depth)

    def print(self, depth):
        """
            Params:
                depth:  depth of the function to print out
        """
        self.printDependencies(depth)
        self.printObjects(depth)
        print('')