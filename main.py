import argparse
from FGC.fileGraphConstructor import FileGraphConstructor
from MGC import ModuleGraphConstructor
from FGC.moduleNode import ModuleNode


def main():
    parser = argparse.ArgumentParser(description="Find File Dependencies")
    parser.add_argument('-mr','--moduleRoot', type=str, default='.', help='Specify the root of the module to inspect')
    # For fgc usage
    parser.add_argument('-f','--filename', type=str, default='main.py', help='Specify which file to find dependencies on')
    parser.add_argument('-af','--allFiles', action='store_false', help='Specify if only python files are considered')
    parser.add_argument('-ic','--ignoreConfig', type=str, default='.gitignore', help='Config file path relative to module root to specify which files to ignore.\n Provide "None" or "none" if no ignoreConfig is specfied.')
    parser.add_argument('-vb','--verbose', action='store_true', help='determine if verbosely find dependencies')
    parser.add_argument('-vg', '--visualgraph', action='store_true', help='Specify whether to visualize graph')
    parser.add_argument('-gp', '--graphpath', type=str, default='file_structure', help='path to save the file structure graph')
    args = parser.parse_args()

    """
        Uncomment the following to test the FGC
    """
    # FGC = FileGraphConstructor('moduleClasses.py')
    # FGC.visitTree()
    # FGC.print_nodes()

    """
        Initialize the MGC by specifying moduel root and ignore file
        Args:
            module_root:    Root path of the module being inspected
            ignoreConfig:   Config file to specify which files to ignore, default to .gitignore
            graphpath:      Path to save the file structure graph
    """
    if args.ignoreConfig.lower() == "none":
        args.ignoreConfig = ''
    MGC = ModuleGraphConstructor(args.moduleRoot, args.ignoreConfig, args.graphpath, args.visualgraph)

    """
        Traverse the module under args.moduleRoot
        Args:
            onlyPython: Determines whether to include non-python files
    """
    MGC.traverse_module(onlyPython=args.allFiles)
    

    """
        Find file dependencies in the module
        Args:
            verbose:    Determines whether to print out parsing results verbosely

    """
    MGC.findDepends(verbose=args.verbose)

    """
        Print file structure on the terminal
        Args:
            show_graph: Determines whether to plot file structure graph,
                        the graph is saved as {args.moduleRoot}_file-structure.png
    """
    # args.visualgraph must be true to show graph
    show_graph = True and args.visualgraph
    MGC.printModule(show_graph=show_graph)

    """
        Write external dependencies found by findDepends() into requirements.txt for pip to install
    """
    MGC.writeRequirements()
    """
        Get subgraph by specifying a list of file path relative to the module_root
        Full Name of the file must be of relative path to module_root
    """
    # MGC.SubGraph(['test_module/test2.py','test_module/tester.py'])

    """
        Construct class/function level dependency grpah
    """
    MGC.FuncDepend()
if __name__ == '__main__':
    main()