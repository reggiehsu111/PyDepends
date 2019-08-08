import pygraphviz as pgv

class graphVisualizer(pgv.AGraph):
	def __init__(self):
		super().__init__(strict=False,directed=True)

	def addFile(self,FileNode):
		assert FileNode.customType() == 'File'
		self.add_node(FileNode.FileName, color='blue')

	def addDir(self,DirNode):
		assert DirNode.customType() == 'Directory'
		for childDir in DirNode.childDir:
			self.add_edge(DirNode.DirName,childDir.DirName)
		for childFile in DirNode.childFile:
			self.add_edge(DirNode.DirName,childFile.FileName)