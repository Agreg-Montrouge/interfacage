import sys
import argparse

from . import __version__

parser = argparse.ArgumentParser(epilog='Available action: bode zip')

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('--version', action='store_true',
        help="show the version of tpmontrouge")

group.add_argument('action', type=str, nargs='?', help='the action to launch')


def create_zip():
    import os
    import zipfile
    import fnmatch
    def findFileGenerator(rootDirectory, ext='.py', rec=True):
        """ Liste un repertoire recursivement
        
        Generateur sortant la liste de tous les fichier du rootDirectory et ss repertoires
        tel que acceptanceFunction(fichier) == True 
        """
        acceptanceFunction = lambda filename: fnmatch.fnmatch(filename,'*'+ext)
        for x in os.listdir(rootDirectory):
            item = os.path.join(rootDirectory, x)
            if acceptanceFunction(item):
                yield x
            if rec and os.path.isdir(item):
                for y in findFileGenerator(item, ext=ext):
                    yield os.path.join(x,y)

    out_base = "tpmontrouge"

    zip_name = 'dist/tpmontrouge.zip'
    a = zipfile.ZipFile(zip_name,'w')

    dest = out_base
    base = "tpmontrouge"
    for x in findFileGenerator(base, rec=True):
        a.write(os.path.join(base, x), os.path.join(dest, x))

    a.writestr('__main__.py', "from tpmontrouge.main import main\nmain()")

    a.close()


def main():
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        action = sys.argv[1]
    else:
        args, opts = parser.parse_known_args()
        if args.version:
            print(__version__)
            return

    if not action:
        parser.print_usage(file=sys.stderr)
        sys.exit("subcommand is required")

    if action=='bode':
        from .interface.bode_plot import main
        args = sys.argv[0:1] + sys.argv[2:]
        main(args)
        return

    if action=='zip':
        create_zip()
