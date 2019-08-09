import argparse
from fileGraphConstructor import FileGraphConstructor
from moduleGraphConstructor import ModuleGraphConstructor
from moduleNode import ModuleNode
from test_module.tester import test_func
# from test_module import test_init

def main():
    parser = argparse.ArgumentParser(description="Find File Dependencies")
    parser.add_argument('-mr','--moduleRoot', type=str, default='.', help='Specify the root of the module to inspect')
    # For fgc usage
    parser.add_argument('-f','--filename', type=str, default='main.py', help='Specify which file to find dependencies on')
    parser.add_argument('-af','--allFiles', action='store_false', help='Specify if only python files are considered')
    parser.add_argument('-ic','--ignoreConfig', type=str, default='.gitignore', help='Config file to specify which files to ignore')
    parser.add_argument('-vb','--verbose', action='store_true', help='determine if verbosely find dependencies')
    args = parser.parse_args()


    MGC = ModuleGraphConstructor(args.moduleRoot, args.ignoreConfig)
    MGC.traverse_module(construct=True, onlyPython=args.allFiles)
    MGC.findDepends(verbose=args.verbose)
    MGC.printModule()
    MGC.writeRequirements()
if __name__ == '__main__':
    main()