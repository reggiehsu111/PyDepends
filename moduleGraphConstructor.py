import os
from moduleClasses import *
from fileGraphConstructor import FileGraphConstructor
from visualizer import graphVisualizer
import re
from util import print_tabs

"""
    Class ModuleGraphConstructor to construct module directory tree
"""
class ModuleGraphConstructor():
    def __init__(self, module_root):
        """
            Params: 
                module_root:    path to the root of the module
        """
        self.module_root = module_root
        self.FGC = FileGraphConstructor()
        self.directories = {}
        self.files = {}
        self.graphVis = graphVisualizer()
        self.ignore_files = []
        self.ignore_dirs = []
        with open(self.module_root+'/'+'.gitignore','r') as f:
            ignore_files = f.read().splitlines() 
        for file in ignore_files:
            if file.endswith('/'):
                self.ignore_dirs.append(file[:-1])
            else:
                self.ignore_files.append(file)
        

    def constructFileNode(self, root, fileName, onlyPython=False):
        """
            Params:
                root:       root path of the file with respect to the module_root
                fileName:   name of the file
                onlyPython: bool variable determine if only python files are included
        """
        parent_dir = root
        newFile = File(fileName, parent_dir)
        self.files[fileName] = newFile
        def process(self):
            # Add key in self.directories if parent_dir not exist
            if parent_dir not in self.directories:
            #     # Set parent of the parent_dir to none if parent_dir is module_root
                if parent_dir == self.module_root:
                    self.directories[parent_dir] = Directory(parent_dir, None, None, newFile)
                else:
                    pass
            #         parent_of_parent = root.split('/')[:-1]
            #         parent_of_parent = '/'.join(parent_of_parent)
            #         self.directories[parent_dir] = Directory(parent_dir,parent_of_parent, None, newFile)
            # Else add file to childFile of parent_dir
            else:
                self.directories[parent_dir].addChildFile(newFile)
            

        if onlyPython:
            if fileName.endswith('.py'):
                process(self)
        else:
            process(self)

    def constructDirNode(self, root, dirName):
        """
            Params:
                root:       root path of the file with respect to the module_root
                dirName:   name of the directory
        """
        parent_dir = root
        newDir = Directory(dirName, parent_dir)
        self.directories[dirName] = newDir
        # Add key in self.directories if parent_dir not exist
        if parent_dir not in self.directories:
            pass
            # # Set parent of the parent_dir to none if parent_dir is module_root
            if parent_dir == self.module_root:
                self.directories[parent_dir] = Directory(parent_dir, None, newDir, None)
            else:
                pass
            #     parent_of_parent = root.split('/')[:-1]
            #     parent_of_parent = '/'.join(parent_of_parent)
            #     self.directories[parent_dir] = Directory(parent_dir,parent_of_parent, newDir, None)
        # Else add file to childFile of parent_dir
        else:
            self.directories[parent_dir].addChildDir(newDir)
        


    def traverse_module(self, construct=False, onlyPython=False):
        """
            Params:
                construct:  whether to construct file structure graph
                onlyPython: whether to construct only python files
        """
        print("Traversing Module... ")
        print("Starting from root:", self.module_root)
        for root, dirs, files in os.walk(self.module_root, topdown=True):
            for name in dirs:
                full_name = os.path.join(root,name)
                # Checks if dir is in .gitignore
                flag = False
                for elem in self.ignore_dirs:
                    pattern = re.compile(elem)
                    if re.match(pattern, name):
                        flag = True
                        break
                if flag == True:
                    continue

                if construct:
                    self.constructDirNode(root, full_name)
        """Clean up directory nodes that don't have a parent"""
        self.cleanDir()

        for root, dirs, files in os.walk(self.module_root, topdown=True):
            for name in files:
                full_name = os.path.join(root,name)
                # Checks if file is in .gitignore
                flag = False
                for elem in self.ignore_files:
                    pattern = re.compile(elem)
                    if re.match(pattern, name):
                        flag = True
                        break
                if root not in self.directories:
                    flag = True
                if flag == True:
                    continue
                if construct:
                    self.constructFileNode(root, full_name, onlyPython)

    """Recursively traverse upwards to find the root"""
    def traverseDirUp(self, directory, success):
        try:
            parent = self.directories[directory].parentDir
        except KeyError as e:
            parent = None
            success = False
        if parent == None:
            return directory, success
        else:
            return self.traverseDirUp(parent, success)

    """Clean up directory nodes that don't have a parent"""
    def cleanDir(self):
        deletes = []
        for directory in self.directories.keys():
            success = True
            root, find_success = self.traverseDirUp(directory, success)
            if not find_success:
                deletes.append(directory)
        for delete in deletes:
            del self.directories[delete]

    """
        Print module structure on the terminal and draw graph
    """
    def printModule(self):
        currentnode = self.directories[self.module_root]
        self.traversePrint(currentnode, -1)
        self.graphVis.layout(prog='dot')
        self.graphVis.draw('file_structure.png')

    def traversePrint(self, currentnode, depth):
        depth += 1
        if currentnode.customType() == 'File':
            # Print file node with indentation
            print_tabs(depth)
            print(currentnode)
            # Add file to graph
            self.graphVis.addFile(currentnode)
        elif currentnode.customType() == 'Directory':
            # Print dir node with indentation
            print_tabs(depth)
            print('/',end='')
            print(currentnode)
            # Add dir to graph
            self.graphVis.addDir(currentnode)
            if len(currentnode.childDir) > 0:
                for dirNode in currentnode.childDir:
                    self.traversePrint(dirNode, depth)
            if len(currentnode.childFile) > 0:
                for fileNode in currentnode.childFile:
                    self.traversePrint(fileNode, depth)
    """
        Traverse files in self.files and find their dependencies
    """
    def traverse_pythonFiles(self):
        for file in self.files:
            if file.endswith('.py'):
                print("File:", file)
                self.FGC.readFile(file)
                self.FGC.visitTree()
                self.FGC.print_nodes(depth=1)
