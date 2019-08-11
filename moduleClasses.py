from classNode import ClassNode

"""
    Class File to store a file under the root directory
"""
class File():
    def __init__(self, FullName, parentDir):
        self.FullName = FullName
        self.FileName = self.FullName.split('/')[-1]
        self.parentDir = parentDir
        self.dependFiles = set()
        self.externals = set()
        self.functions = {}
        self.classes = {}

    def __repr__(self):
        return self.FileName

    def print_dependencies(self):
        if len(self.dependFiles) > 0:
            print("\tDepend Files:")
            for dep in self.dependFiles:
                print("\t\t" + dep.FileName)
        else:
            print("\tNo depend files")

    def print_externals(self):
        if len(self.externals) > 0:
            print("\tExternals:")
            for extern in self.externals:
                print("\t\t" + extern)
        else:
            print("\tNo external dependencies")


    def print_classes(self):
        if len(self.classes) > 0:
            print("\tClasses:")
            for clss in self.classes:
                print("\t\t" + clss)
        else:
            print("\tNo class definitions")

    def print_functions(self):
        if len(self.functions) > 0:
            print("\tFunctions:")
            for func in self.functions:
                print("\t\t" + func)
        else:
            print("\tNo function definitions")

    @classmethod
    def customType(self):
        return "File"


"""
    Class Directory to store a directory instance under the root directory
"""
class Directory():
    def __init__(self, FullName, parentDir, childDir = None, childFile = None):
        self.FullName = FullName
        self.DirName = self.FullName.split('/')[-1]
        self.parentDir = parentDir
        self.childDir = []
        self.childFile = []
        self.addChildFile(childFile)
        self.addChildDir(childDir)

    def __repr__(self):
        return self.DirName

    @classmethod
    def customType(self):
        return "Directory"

    def addChildDir(self, childDir):
        if childDir is not None:
            # if childDir is an instance of list
            if isinstance(childDir, list):
                for Dir in childDir:
                    Dir = Directory(Dir, self.FullName)
                    assert isinstance(Dir, Directory)
                    self.childDir.append(Dir)
            # else if childDir is an instance of str
            elif isinstance(childDir,str):
                childDir = Directory(childDir, self.FullName)
                assert isinstance(childDir, Directory)
                self.childDir.append(childDir)
            # else if childDir is an instance of Directory
            elif isinstance(childDir, Directory):
                self.childDir.append(childDir)


    def addChildFile(self, childFile):
        if childFile is not None:
            # if childFile is an instance of list
            if isinstance(childFile, list):
                for file in childFile:
                    file = File(file, self.FullName)
                    assert isinstance(file, File)
                    self.childFile.append(file)
            # else if childFile is an instance of str
            elif isinstance(childFile, str):
                childFile = File(childFile, self.FullName)
                assert isinstance(childFile, File)
                self.childFile.append(childFile)
            # else if childDir is an instance of Directory
            elif isinstance(childFile, File):
                self.childFile.append(childFile)
    
