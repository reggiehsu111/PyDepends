from visualizer.visualizer import graphVisualizer
def dep_resolve(file, included, subGraphVis):
	included.add(file.FullName)
	subGraphVis.addFile(file)
	for dep in file.dependFiles:
		subGraphVis.addDependencies(file, dep)
		dep_resolve(dep, included, subGraphVis)
"""
	MGC method to find Subgraph dependencies specifying fileNames
"""
def SubGraph(self, fileNames):
	"""
		Params:
			fileNames:	List of file fullnames to be considered
	"""
	subGraphVis = graphVisualizer('Subgraph')
	included = set()
	assert type(fileNames) == list
	for file in fileNames:
		assert file in self.files
		file = self.files[file]
		dep_resolve(file, included, subGraphVis)
		for extern in file.externals:
			subGraphVis.addExternals(file, extern)
	subGraphVis.showGraph()