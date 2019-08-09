import ast
from moduleNode import ModuleNode


"""
    Class FileGraphConstructor to construct graph for a single file
"""
class FileGraphConstructor(ast.NodeVisitor):
    def __init__(self, moduleName=None):
        super().__init__()
        if moduleName is not None:
            self.readFile(moduleName)
        # List to store moduleNodes once found
        # moduleNodes are the file dependencies of the file
        self.moduleNodes = {}

    def readFile(self, moduleName):
        self.moduleName = moduleName
        with open(self.moduleName, "r") as source:
            self.tree = ast.parse(source.read())
        self.moduleNodes = {}

    def visitTree(self):
        super().visit(self.tree)

    def visit_Import(self, node):
        for alias in node.names:
            temp_module = alias.name
            temp_alias = alias.asname
            temp_fn = ModuleNode(temp_module, temp_alias)
            self.moduleNodes[temp_module] = temp_fn
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            temp_func = alias.name
            temp_alias = alias.asname
            temp_module = node.module
            if temp_module in self.moduleNodes:
                self.moduleNodes[temp_module].addFunctions(temp_func)
            else:
                temp_mn = ModuleNode(temp_module, temp_alias, temp_func)
                self.moduleNodes[temp_module] = temp_mn

        self.generic_visit(node)

    def visit_ClassDef(self, node):
        print("ClassDef node:",node.name)

        self.generic_visit(node)


    def print_nodes(self,depth=0):
        for Nodes in self.moduleNodes.values():
            Nodes.print(depth)
