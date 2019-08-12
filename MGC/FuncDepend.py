"""
	MGC method to construct function level dependency graph
"""
def FuncDepend(self, funcGraphPath):
	print(".....Constructing Function Level Dependency.....")
	# Copy self.graphVis to self.funcGraphVis if self.funcGraphVis is not yet initialized
	if self.funcGraphVis == None:
		self.funcGraphVis = self.graphVis
	self.funcGraphVis.graph_file_path = funcGraphPath

	for file in self.files.values():
		for clss in file.classes.values():
			self.funcGraphVis.addClass(file, clss)
		for func in file.functions:
			# func is not a class method
			if len(func.split('/')) == 1:
				function = file.functions[func]
				self.funcGraphVis.addFunc(file, function)
	self.funcGraphVis.showGraph()