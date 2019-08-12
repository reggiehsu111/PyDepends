from visualizer.visualizer import graphVisualizer

def dep_resolve(file, included, subGraphVis):
	if file.FullName in included:
		return
	else:
		included.add(file.FullName)
		subGraphVis.addFile(file)
		for dep in file.dependFiles:
			subGraphVis.addDependencies(file, dep)
			dep_resolve(dep, included, subGraphVis)
"""
	MGC method to find Subgraph dependencies specifying fileNames
"""
def SubGraph(self, fileNames, subGraphPath):
	"""
		Params:
			fileNames:		List of file names to be considered (file names are paths relative to self.module_root)
			subGraphPath:	Path to save the subgraph
	"""
	subGraphVis = graphVisualizer(subGraphPath)
	included = set()
	assert type(fileNames) == list
	print("Constructing Subgraph with files:")
	for file in fileNames:
		print("\t"+file)
		# construct full path
		file = self.module_root + '/' + file
		try:
			assert file in self.files
		except AssertionError as e:
			print("\nFile path:", file, "can't be found while constructing subgraph. \nPlease make sure the relative path to module_root exists")
			exit()
		file = self.files[file]
		dep_resolve(file, included, subGraphVis)
		for extern in file.externals:
			subGraphVis.addExternals(file, extern)
	subGraphVis.showGraph()