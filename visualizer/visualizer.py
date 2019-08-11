import pygraphviz as pgv
import networkx as nx
import matplotlib.pyplot as plt
class graphVisualizer(pgv.AGraph):
    def __init__(self, graph_file_path):
        super().__init__(strict=False,directed=True)
        self.graph_file_path = graph_file_path
        self.allnodes = set()
        self.alledges = set()

    def add_node(self, Node, *args, **kwargs):
        super().add_node(Node, *args, **kwargs)
        self.allnodes.add(Node)


    def add_edge(self, Node1, Node2, *args, **kwargs):
        if Node1+'/'+Node2 not in self.alledges:
            super().add_edge(Node1, Node2, *args, **kwargs)
            self.allnodes.add(Node1)
            self.allnodes.add(Node2)
            self.alledges.add(Node1+'/'+Node2)
        else:
            return

    def addFile(self,FileNode):
        assert FileNode.customType() == 'File'
        self.add_node(FileNode.FileName, color='blue')

    def addDir(self,DirNode):
        assert DirNode.customType() == 'Directory'
        self.add_node(DirNode.DirName, color='black')
        for childDir in DirNode.childDir:
            self.add_edge(DirNode.DirName,childDir.DirName)
        for childFile in DirNode.childFile:
            self.add_edge(DirNode.DirName,childFile.FileName)

    def addDependencies(self, currentfile, tracenode):
        assert currentfile.customType() == 'File'
        assert tracenode.customType() == 'File'
        self.add_edge(currentfile.FileName, tracenode.FileName, color='red')

    def addExternals(self, currentfile, extern):
        assert currentfile.customType() == 'File'
        self.add_edge(currentfile.FileName, extern, color='green')

    def showGraph(self):
        for base in self.__class__.__bases__:
            if base.__name__ == 'AGraph':
                self.showGraphPGV()
            elif base.__name__ == 'DiGraph':
                self.showGraphNX()
    """ Use when using pgv as dependency """
    def showGraphPGV(self):
        self.layout(prog='dot')
        self.draw(self.graph_file_path+'.png')
        self.write(self.graph_file_path+'.dot')

    """ Use when using nx as dependency """
    def showGraphNX(self):
        pos=nx.spring_layout(self)
        nx.draw(self,pos,with_labels=True)
        plt.show()