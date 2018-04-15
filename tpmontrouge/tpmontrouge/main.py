import sys
import argparse
from . import __version__
from .interface import main as full_main
from .interface.scope import main as scope_main
from .interface.bode_plot import main as bode_main
from .interface.plotter import main as plotter_main

parser = argparse.ArgumentParser()

parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)


parser.add_argument('-v', '--version', action='store_true',
        help="show the version of tpmontrouge and exit")

#parser.add_argument('action', nargs='?', choices=['full', 'bode', 'scope', 'zip'], help='the action to launch', default='interface')

subparsers = parser.add_subparsers(help='sub-command help')

def create_zip(args):
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

zip_parser = subparsers.add_parser('zip', help='Zip file')
zip_parser.set_defaults(func=create_zip)

full_parser = subparsers.add_parser('all', help='Full GUI interface')
full_main.create_parser(full_parser)
full_parser.set_defaults(func=full_main.main)

scope_parser = subparsers.add_parser('scope', help='Scope GUI')
scope_main.create_parser(scope_parser)
scope_parser.set_defaults(func=scope_main.main)

bode_parser = subparsers.add_parser('bode', help='Bode GUI')
bode_main.create_parser(bode_parser)
bode_parser.set_defaults(func=bode_main.main)

plotter_parser = subparsers.add_parser('plotter', help='Plotter GUI')
bode_main.create_parser(plotter_parser)
plotter_parser.set_defaults(func=plotter_main.main)

def main():
#    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
#        action = sys.argv[1]
#    else:
    args = parser.parse_args()
    if args.version:
        print(__version__)
        return

    try:
        args.func(args)
    except AttributeError:
        print(parser.parse_args(['--help']))
        return


