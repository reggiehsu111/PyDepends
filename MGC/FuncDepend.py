"""
	MGC method to construct function level dependency graph
"""
def FuncDepend(self):
	print(".....Constructing Function Level Dependency.....")
	for file in self.files.values():
		for clss in file.classes.values():
			self.graphVis.addClass(file, clss)
		for func in file.functions:
			# func is not a class method
			if len(func.split('/')) == 1:
				function = file.functions[func]
				self.graphVis.addFunc(file, function)
	self.graphVis.showGraph()