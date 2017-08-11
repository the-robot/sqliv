import argparse
import os
import stat
import pip
from shutil import copy2
from distutils.dir_util import copy_tree


__author__ = "Ghost"
__email__ = "official.ghost@tuta.io"
__license__ = "GPL"
__version__ = "2.0"


# script dependencies
dependencies = ["bs4", "termcolor", "terminaltables"]

# installation directory PATH
FILE_PATH = "/usr/share/sqliv"
EXEC_PATH = "/usr/bin/sqliv"

# executable script
exec_script = """
#!/bin/bash

python2 /usr/share/sqliv/sqliv.py "$@"
"""


def metadata():
    print "SQLiv <2.0> by {}".format(__author__)
    print "Massive SQL injection vulnerability scanner"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="install sqliv in the system",  action='store_true')
    args = parser.parse_args()

    if os.name == "nt":
        print "windows platform is not supported for installation"
        exit(1)

    if os.getuid() != 0:
        print "root access is required for the installation"
        exit(1)

    if os.path.exists(FILE_PATH):
        print "sqliv is already installed under /usr/share/sqliv"
        exit(1)

    if os.path.isfile(EXEC_PATH):
        print "executable file exists under /usr/bin/sqliv"
        exit(1)

    # full installation
    if args.i:
        # file installation process
        os.mkdir(FILE_PATH)
        copy2("sqliv.py", FILE_PATH)
        copy2("requirements.txt", FILE_PATH)
        copy2("LICENSE", FILE_PATH)
        copy2("README.md", FILE_PATH)

        os.mkdir(FILE_PATH + "/src")
        copy_tree("src", FILE_PATH + "/src")

        os.mkdir(FILE_PATH + "/libs")
        copy_tree("libs", FILE_PATH + "/libs")

        # install dependencies
        for lib in dependencies:
            pip.main(["install", lib])

        # add executable
        with open(EXEC_PATH, 'w') as installer:
            installer.write(exec_script)
        # S_IRWXU = rwx for owner
        # S_IRGRP | S_IXGRP = rx for group
        # S_IROTH | S_IXOTH = rx for other
        os.chmod(EXEC_PATH, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

        print "installation finished"
        print "files are installed under " + FILE_PATH
        print "run: sqliv --help"

    else:
        print "python2 setup.py --help"
