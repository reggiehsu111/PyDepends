import pygraphviz as pgv
import networkx as nx
import matplotlib.pyplot as plt
class graphVisualizer(pgv.AGraph):
    def __init__(self, module_root):
        super().__init__(strict=False,directed=True)
        self.module_root = module_root

    def addFile(self,FileNode):
        assert FileNode.customType() == 'File'
        self.add_node(FileNode.FileName, color='blue')

    def addDir(self,DirNode):
        assert DirNode.customType() == 'Directory'
        for childDir in DirNode.childDir:
            self.add_edge(DirNode.DirName,childDir.DirName)
        for childFile in DirNode.childFile:
            self.add_edge(DirNode.DirName,childFile.FileName)

    def addDependencies(self, currentfile, tracenode):
        assert currentfile.customType() == 'File'
        assert tracenode.customType() == 'File'
        self.add_edge(currentfile.FileName, tracenode.FileName, color = 'red')

    def showGraph(self):
        for base in self.__class__.__bases__:
            if base.__name__ == 'AGraph':
                self.showGraphPGV()
            elif base.__name__ == 'DiGraph':
                self.showGraphNX()
    """ Use when using pgv as dependency """
    def showGraphPGV(self):
        self.layout(prog='dot')
        self.draw(self.module_root+'_file_structure.png')

    """ Use when using nx as dependency """
    def showGraphNX(self):
        pos=nx.spring_layout(self)
        nx.draw(self,pos)
        plt.show()