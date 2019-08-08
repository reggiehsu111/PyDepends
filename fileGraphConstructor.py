import ast
from fileNode import FileNode


"""
    Class FileGraphConstructor to construct graph for a single file
"""
class FileGraphConstructor(ast.NodeVisitor):
    def __init__(self, fileName=None):
        super().__init__()
        if fileName is not None:
            self.readFile(fileName)
        # List to store fileNodes once found
        # fileNodes are the file dependencies of the file
        self.fileNodes = {}
        self.fileNames = set()

    def readFile(self, fileName):
        self.fileName = fileName
        with open(fileName, "r") as source:
            self.tree = ast.parse(source.read())
        self.fileNodes = {}
        self.fileNames = set()

    def visitTree(self):
        super().visit(self.tree)

    def visit_Import(self, node):
        for alias in node.names:
            temp_module = alias.name
            temp_alias = alias.asname
            temp_fn = FileNode(temp_module, temp_alias)
            self.fileNodes[temp_module] = temp_fn
            self.fileNames.add(temp_module)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            temp_func = alias.name
            temp_alias = alias.asname
            temp_module = node.module
            if temp_module in self.fileNames:
                self.fileNodes[temp_module].addFunctions(temp_func)
            else:
                temp_fn = FileNode(temp_module, temp_alias, temp_func)
                self.fileNodes[temp_module] = temp_fn
                self.fileNames.add(temp_module)

        self.generic_visit(node)

    def print_nodes(self,depth=0):
        for Nodes in self.fileNodes.values():
            Nodes.print(depth)
