import os
from .moduleClasses import File, Directory
from FGC.fileGraphConstructor import FileGraphConstructor
from visualizer.visualizer import graphVisualizer
import re
from utils.util import print_tabs
from FGC.moduleNode import ModuleNode
import sys
import imp


"""
    Class ModuleGraphConstructor to construct module directory tree
"""
class ModuleGraphConstructor():
    from .SubGraph import SubGraph
    def __init__(self, module_root, ignoreConfig, graph_file_path, visualgraph):
        """
            Params: 
                module_root:    path to the root of the module
                ignoreConfig:   path to the ignoreConfig file
                graph_file_path:path to save the graph
                visualgraph:    whether to visaulize the graph
        """
        self.module_root = module_root
        self.FGC = FileGraphConstructor()
        self.directories = {}
        self.files = {}
        # Dict type to store possible ClassDefs defined in __init__.py
        self.possibleClassDefs = {}
        # Dict type to store resolved ClassDefs defined in __init__.py
        self.resolvedClassDefs = {}
        # For plotting file structure graph
        self.visualgraph = visualgraph
        if self.visualgraph:
            self.graphVis = graphVisualizer(graph_file_path)
        self.ignore_files = []
        self.ignore_dirs = []
        self.ignoreConfig = ignoreConfig
        # Set to store all external dependencies of a module
        self.allExterns = set()
        # Determine if ignoreConfig is specified
        if ignoreConfig is not '':
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
        


    def traverse_module(self, onlyPython=False):
        """
            Params:
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
                    # for elem starting with *, re.match can't parse
                    if elem.startswith('*'):
                        pattern = elem.split('*')[-1]
                        if name.endswith(pattern):
                            flag = True
                            break
                    else:
                        pattern = re.compile(elem)
                        if re.match(pattern, name):
                            flag = True
                            break
                if flag == True:
                    continue

                self.constructDirNode(root, full_name)
        # Clean up directory nodes that don't have a parent
        self.cleanDir()

        for root, dirs, files in os.walk(self.module_root, topdown=True):
            for name in files:
                full_name = os.path.join(root,name)
                # Checks if file is in .gitignore
                flag = False
                for elem in self.ignore_files:
                    # for elem starting with *, re.match can't parse
                    if elem.startswith('*'):
                        pattern = elem.split('*')[-1]
                        if name.endswith(pattern):
                            flag = True
                            break
                    else:
                        pattern = re.compile(elem)
                        if re.match(pattern, name):
                            flag = True
                            break
                if root not in self.directories:
                    flag = True
                if flag == True:
                    continue
                self.constructFileNode(root, full_name, onlyPython)

    """
        Recursively traverse upwards to find the root
    """
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

    """
        Clean up directory nodes that don't have a parent
    """
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
    def printModule(self, show_graph=True):
        currentnode = self.directories[self.module_root]
        print(".....File Structure.....")
        self.traversePrint(currentnode, -1)
        if show_graph and self.visualgraph:
            self.graphVis.showGraph()

    def traversePrint(self, currentnode, depth):
        depth += 1
        if currentnode.customType() == 'File':
            # Print file node with indentation
            print_tabs(depth)
            print(currentnode)
            # Add file to graph
            if self.visualgraph:
                self.graphVis.addFile(currentnode)
        elif currentnode.customType() == 'Directory':
            # Print dir node with indentation
            print_tabs(depth)
            print('/',end='')
            print(currentnode)
            # Add dir to graph
            if self.visualgraph:
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
    def parseFGC(self, currentfile, verbose):
        currentfile = self.files[currentfile]
        if verbose:
            print("\tAll modules:")
        # Iterate all module nodes to parse through
        for node in self.FGC.moduleNodes.values():
            # Relative import or import is either . or .. or ...
            if node.module == None or node.level>0:
                level = node.level
                tracenode = currentfile
                for lv in range(level):
                    tracenode = self.directories[tracenode.parentDir]
                if node.module is not None:
                    delegates = node.module.split('.')
                    if verbose:
                        print('\t\t'+node.module)
                else:
                    delegates = []
                    if verbose:
                        print('\t\t', end='')
                        for lv in range(level):
                            print('.', end='')
                    for obj in node.objs:
                            temp_file = '/'.join([tracenode.FullName, obj.alias+'.py'])
                            # If successfully find temp_file in self.files, obj is a file
                            try:
                                tracenode = self.files[temp_file]
                                currentfile.dependFiles.add(tracenode)
                                if self.visualgraph:
                                    self.graphVis.addDependencies(currentfile,tracenode)
                            # Else obj is a class defined in __init__.py or there is an error
                            except KeyError as e:
                                key = currentfile.FullName+'|'+tracenode.FullName+'/'+obj.alias
                                if key not in self.possibleClassDefs:
                                    self.possibleClassDefs[key] = obj
            # Absolute import
            else:
                if verbose:
                    print('\t\t'+node.module)
                # tracenode to determine the path of the module relative to module_root
                tracenode = self.directories[self.module_root]
                delegates = node.module.split('.')
            # Variable count to store how many delegates processed
            count = 0
            # delegate must be a file/directory/external_dependency
            for dg in delegates:
                count += 1
                if count == 1:
                    delegate = '/'.join([tracenode.FullName,dg])
                else:
                    delegate = '/'.join([delegate, dg])
                # If delegate is a directory, update tracenode and see if delegates are all processed
                if delegate in self.directories:
                    # If walk to the end, dependent file is either in node.objs or in __init__.py
                    if count == len(delegates):
                        for obj in node.objs:
                            tracenode = self.directories[delegate]
                            temp_file = '/'.join([tracenode.FullName, obj.alias+'.py'])
                            # If successfully find temp_file in self.files, obj is a file
                            try:
                                tracenode = self.files[temp_file]
                                currentfile.dependFiles.add(tracenode)
                                if self.visualgraph:
                                    self.graphVis.addDependencies(currentfile,tracenode)
                            # Else obj is a class defined in __init__.py or there is an error
                            except KeyError as e:
                                key = currentfile.FullName+'|'+tracenode.FullName+'/'+obj.alias
                                if key not in self.possibleClassDefs:
                                    self.possibleClassDefs[key] = obj

                else:
                    delegate += '.py'
                    # if delegate is a file
                    if delegate in self.files:
                        tracenode = self.files[delegate]
                        if self.visualgraph:
                            self.graphVis.addDependencies(currentfile,tracenode)
                        currentfile.dependFiles.add(tracenode)
                    # else delegate is an external dependency
                    else:
                        # Add external dependency
                        currentfile.externals.add(delegates[0])
                        if self.visualgraph:
                            self.graphVis.add_node(delegates[0], color='green')
                            self.graphVis.addExternals(currentfile, delegates[0])
                        self.allExterns.add(delegates[0])
                        continue
        if verbose:
            print('')
            # for mn in self.FGC.moduleNodes:
            #     self.FGC.moduleNodes[mn].print(2)
            currentfile.print_externals()
            currentfile.print_dependencies()
            currentfile.print_classes()
            currentfile.print_functions()


    """
        Construct classDefs and functionDefs into the file nodes after running self.FGC.visitTree()
    """
    def constructDefs(self, file):
        """
            Params:
                file:   fileName
        """
        assert file.endswith('.py')
        print("Constructing definitions in file:", file)
        for clss in self.FGC.classes:
            self.files[file].classes[clss] = self.FGC.classes[clss]
        for func in self.FGC.functions:
            self.files[file].functions[func] = self.FGC.functions[func]

    """
        Determine whether objects in self.possibleClassDefs are actually class definitions
        Must run this method after running parseFGC
    """
    def resolvePCD(self):
        for pcd in self.possibleClassDefs:
            currentfile, pcd = pcd.split('|')
            # cf is of type File
            cf = self.files[currentfile]
            temp_root_dir = '/'.join(pcd.split('/')[:-1])
            obj = pcd.split('/')[-1]
            # if obj == "*", import all files under the directory  
            if obj == "*":
                for file in self.directories[temp_root_dir].childFile:
                    cf.dependFiles.add(file)
                    if self.visualgraph:
                        self.graphVis.addDependencies(cf, file)
                for file in self.directories[temp_root_dir].childFile:
                    # try:
                    if "__init__.py" == file.FileName:
                        if obj in file.classes:
                            self.resolvedClassDefs[currentfile+'|'+pcd] = obj
                            cf.dependFiles.add(file)
                            if self.visualgraph:
                                self.graphVis.addDependencies(cf,file)
                    # except KeyError as e:
                    #     print("temp_root_dir:", temp_root_dir)
                    #     raise(e)
                    #     exit()
    """
        Traverse files in self.files and find their dependencies
    """
    def findDepends(self, verbose=True):
        for file in self.files:
            if file.endswith('.py'):
                print("\nFile:", file)
                self.FGC.readFile(file)
                self.FGC.visitTree()
                self.constructDefs(file)
                self.parseFGC(file, verbose)
                self.resolvePCD()
        print("......All external dependencies......")
        for extern in self.allExterns:
            print(extern)

    """
        Function to write requirements.txt without specifying package versions
        Use this function after running findDepends!!!
    """
    def writeRequirements(self):
        externs = set()
        not_yet_installs = set()
        built_ins = set()
        with open('requirements.txt','w') as f:
            python_path = os.path.dirname(sys.executable)
            for extern in self.allExterns:
                try:
                    module_path = imp.find_module(extern)[1]
                    if module_path:
                        if 'site-packages' in module_path:
                            f.write(extern+'\n')
                            externs.add(extern)
                        else:
                            built_ins.add(extern)
                    else:
                        built_ins.add(extern)
                except ImportError as e:
                    not_yet_installs.add(extern)
                    f.write(extern+'\n')
            print("Are builtin packages")
        print(".....External dependencies that are installed.....")
        for ext in externs:
            print('\t',ext)
        print('')
        print(".....External dependencies that are not installed.....")
        for ext in not_yet_installs:
            print('\t',ext)
        print('')
        print(".....Built in dependencies.....")
        for ext in built_ins:
            print('\t',ext)
        print('')
        return