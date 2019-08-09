import os
from moduleClasses import File, Directory
from fileGraphConstructor import FileGraphConstructor
from visualizer import graphVisualizer
import re
from util import print_tabs
from moduleNode import ModuleNode
import sys
import imp

"""
    Class ModuleGraphConstructor to construct module directory tree
"""
class ModuleGraphConstructor():
    def __init__(self, module_root, ignoreConfig):
        """
            Params: 
                module_root:    path to the root of the module
        """
        self.module_root = module_root
        self.FGC = FileGraphConstructor()
        self.directories = {}
        self.files = {}
        # For plotting file structure graph
        self.graphVis = graphVisualizer(self.module_root)
        self.ignore_files = []
        self.ignore_dirs = []
        self.ignoreConfig = ignoreConfig
        # Set to store all external dependencies of a module
        self.allExterns = set()
        with open(self.module_root+'/'+self.ignoreConfig,'r') as f:
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
                # Set parent of the parent_dir to none if parent_dir is module_root
                if parent_dir == self.module_root:
                    self.directories[parent_dir] = Directory(parent_dir, None, None, newFile)
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
            # # Set parent of the parent_dir to none if parent_dir is module_root
            if parent_dir == self.module_root:
                self.directories[parent_dir] = Directory(parent_dir, None, newDir, None)
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
        print(".....File Structure.....")
        self.traversePrint(currentnode, -1)
        self.graphVis.showGraph()

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
        Walk through all dependent modules in currentfile and store external and dependencies in the currentfile node
        Update moduleNodes in FGC while parsing
    """
    def parseFGC(self, currentfile):
        currentfile = self.files[currentfile]
        print("\tAll modules:")
        temp_dict = {}
        # Iterate through all module nodes to parse
        for node in self.FGC.moduleNodes.values():
            print('\t\t'+node.module)
            delegates = node.module.split('.')
            # Relative import
            if node.module.startswith('.'):
                print(node.module,"is a relative import, the parsing utility is not supported yet")
            # Absolute import
            else:
                tracenode = self.directories[self.module_root]
                # Variable count to store how many delegates processed
                count = 0
                # delegate must be a file or directory
                for delegate in delegates:
                    count += 1
                    delegate = '/'.join([tracenode.FullName,delegate])
                    # if delegate is a directory
                    if delegate in self.directories:
                        tracenode = self.directories[delegate]
                        # If walk to the end, dependent file is in node.functions or in __init__.py
                        if count == len(delegates):
                            for func in node.functions:

                                if "__init__.py" in tracenode.childFile:
                                    pass
                                temp_file = '/'.join([tracenode.FullName, func.alias])
                                temp_file += '.py'
                                tracenode = self.files[temp_file]
                                currentfile.dependFiles.add(tracenode)
                                self.graphVis.addDependencies(currentfile,tracenode)
                                # Update moduleNode
                                temp_dict[func] = ModuleNode(func.alias,func.alias)
                    else:
                        delegate += '.py'
                        # if delegate is a file
                        if delegate in self.files:
                            tracenode = self.files[delegate]
                            self.graphVis.addDependencies(currentfile,tracenode)
                            currentfile.dependFiles.add(tracenode)
                            # Update moduleNode
                            temp_dict[node] = ModuleNode(delegate.split('.')[-2].strip('/').replace('/','.'), node.alias, node.functionNames)
                        # else delegate is an external dependency
                        else:
                            currentfile.externals.add(node.module)
                            # Update moduleNode
                            temp_dict[node] = ModuleNode(node.module,node.alias, node.functionNames)
                            self.allExterns.add(delegates[0])
                            continue
                        
        del self.FGC.moduleNodes
        self.FGC.moduleNodes = temp_dict
        print('')
        currentfile.print_externals()
        currentfile.print_dependencies()

    """
        Traverse files in self.files and find their dependencies
    """
    def findDepends(self, verbose=True):
        for file in self.files:
            if file.endswith('.py'):

                print("\nFile:", file)
                self.FGC.readFile(file)
                self.FGC.visitTree()
                if verbose:
                    print("\n\t....Before parsing....")
                    self.FGC.print_nodes(depth=1)
                    print("\t......................\n")
                self.parseFGC(file)
                if verbose:
                    print("\n\t....After parsing....")
                    self.FGC.print_nodes(depth=1)
                    print("\t......................\n")
        print("......All external dependencies......")
        for extern in self.allExterns:
            print(extern)

    """
        Function to write requirements.txt without specifying package versions
        Use this function after running findDepends!!!
    """
    def writeRequirements(self):
        with open('requirements.txt','w') as f:
            python_path = os.path.dirname(sys.executable)
            for extern in self.allExterns:
                module_path = imp.find_module(extern)[1]
                if module_path:
                    if 'site-packages' in module_path:
                        f.write(extern+'\n')
                    else:
                        print(extern)
                else:
                    print(extern)
            print("Are builtin packages")
        return

