import argparse
from fileGraphConstructor import FileGraphConstructor
from moduleGraphConstructor import ModuleGraphConstructor
from fileNode import FileNode
from test_module.tester import test_func

def main():
    parser = argparse.ArgumentParser(description="Find File Dependencies")
    parser.add_argument('-f','--filename', type=str, default='main.py', help='Specify which file to find dependencies on')
    parser.add_argument('-op','--onlyPython', action='store_false', help='Specify if only python files are considered')
    parser.add_argument('-ic','--ifnoreConfig', type=str, default='.gitignore', help='Config file to specify which files to ignore')
    args = parser.parse_args()

    filename = args.filename

    MGC = ModuleGraphConstructor('.')
    MGC.traverse_module(construct=True, onlyPython=args.onlyPython)
    MGC.printModule()
    MGC.traverse_pythonFiles()
if __name__ == '__main__':
    main()