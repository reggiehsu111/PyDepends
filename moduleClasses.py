"""
    Class File to store a file under the root directory
"""
class File():
    def __init__(self, FullName, parentDir):
        self.FullName = FullName
        self.FileName = self.FullName.split('/')[-1]
        self.parentDir = parentDir

    def __repr__(self):
        return self.FileName

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
    
