## @namespace officegenerator.odf2xml
## @brief Function to convert a ODF file to xml output
## 
## Executes the following code in bash
## @code
## odf2xml -o "$1.no.xml" "$1"
## cat "$1.no.xml" | xmllint --format -
## @endcode


import argparse
import datetime
import gettext
import os
import pkg_resources
import platform
import subprocess

from .__init__ import __version__, __versiondate__

try:
    t=gettext.translation('officegenerator',pkg_resources.resource_filename("officegenerator","locale"))
    _=t.gettext
except:
    _=str

def main():
    parser=argparse.ArgumentParser(prog='officegenerator', description=_('Convert a ODF file into an indented xml'), epilog=_("Developed by Mariano Muñoz 2018-{}").format(__versiondate__.year), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--file', action='store', help=_('Odf file to convert'), required=True)
    args=parser.parse_args()

    if platform.system()!="Linux":
        print(_("officegenerator_odf2xml only works on Linux"))
        sys.exit(1)

    p=subprocess.run(["odf2xml", "-o", args.file + ".xml", args.file], stdout=subprocess.PIPE)
    q=subprocess.run(['xmllint', '--format', args.file +".xml"], stdout=subprocess.PIPE, input=p.stdout)
    r=subprocess.run(['rm', args.file + ".xml"])
    print(q.stdout.decode('UTF-8'))

if __name__ == "__main__":
    main()