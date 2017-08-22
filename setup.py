import argparse
import os
import stat
import pip
from sys import platform
from shutil import copy2, rmtree
from distutils.dir_util import copy_tree


__author__ = "Ghost"
__email__ = "official.ghost@tuta.io"
__license__ = "GPL"
__version__ = "2.0"


# installation directory PATHs
FILE_PATH_LINUX = "/usr/share/sqliv"
EXEC_PATH_LINUX = "/usr/bin/sqliv"

FILE_PATH_MAC = "/usr/local/bin"
EXEC_PATH_MAC = "/usr/local/bin"


def metadata():
    print "SQLiv (2.0) by {}".format(__author__)
    print "Massive SQL injection vulnerability scanner"


def dependencies(option):
    """install script dependencies with pip"""

    try:
        with open("requirements.txt", "r") as requirements:
            dependencies = requirements.read().splitlines()
    except IOError:
        print "requirements.txt not found, please redownload or do pull request again"
        exit(1)

    for lib in dependencies:
        pip.main([option, lib])


def install(file_path, exec_path):
    """full installation of SQLiv to the system"""

    os.mkdir(file_path)
    copy2("sqliv.py", file_path)
    copy2("requirements.txt", file_path)
    copy2("LICENSE", file_path)
    copy2("README.md", file_path)

    os.mkdir(file_path + "/src")
    copy_tree("src", file_path + "/src")

    os.mkdir(file_path + "/libs")
    copy_tree("libs", file_path + "/libs")

    # python dependencies with pip
    dependencies("install")

    # add executable
    with open(exec_path, 'w') as installer:
        installer.write('#!/bin/bash\n')
        installer.write('\n')
        installer.write('python2 {}/sqliv.py "$@"\n'.format(file_path))

    # S_IRWXU = rwx for owner
    # S_IRGRP | S_IXGRP = rx for group
    # S_IROTH | S_IXOTH = rx for other
    os.chmod(exec_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)


def uninstall(file_path, exec_path):
    """uninstall sqliv from the system"""

    if os.path.exists(file_path):
        rmtree(file_path)
        print "Removed " + file_path

    if os.path.isfile(exec_path):
        os.remove(exec_path)
        print "Removed " + exec_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="install sqliv in the system",  action='store_true')
    parser.add_argument("-r", "--reinstall", help="remove old files and reinstall to the system", action="store_true")
    parser.add_argument("-u", "--uninstall", help="uninstall sqliv from the system", action="store_true")
    args = parser.parse_args()

    if platform == "linux" or platform == "linux2":
        # Linux require root
        if os.getuid() != 0:
            print "linux system requires root access for the installation"
            exit(1)

        FILE_PATH = FILE_PATH_LINUX
        EXEC_PATH = EXEC_PATH_LINUX

    elif platform == "darwin":
        FILE_PATH = FILE_PATH_MAC
        EXEC_PATH = EXEC_PATH_MAC

    else:
        print "Windows platform is not supported for installation"
        exit(1)

    if args.install and not (args.reinstall or args.uninstall):
        #full installation to the system

        if os.path.exists(FILE_PATH):
            print "sqliv is already installed under " + FILE_PATH
            exit(1)

        if os.path.isfile(EXEC_PATH):
            print "executable file exists under " + FILE_PATH
            exit(1)

        install(FILE_PATH, EXEC_PATH)
        print "Installation finished"
        print "Files are installed under " + FILE_PATH
        print "Run: sqliv --help"

    elif args.uninstall and not (args.install or args.reinstall):
        # uninstall from the system

        uninstall(FILE_PATH, EXEC_PATH)
        option = raw_input("Do you want to uninstall python dependencies? [Y/N]: ").upper()
        while option != "Y" and option != "N":
            option = raw_input("Do you want to uninstall python dependencies? [Y/N]: ").upper()

        if option == "Y":
            dependencies("uninstall")
            print "Python dependencies removed"

        print "Uninstallation finished"

    elif args.reinstall and not (args.install or args.uninstall):
        # reinstall to the system

        uninstall(FILE_PATH, EXEC_PATH)
        print "Removed previous installed files"

        install(FILE_PATH, EXEC_PATH)
        print "Reinstallation finished"
        print "Files are installed under " + FILE_PATH
        print "Run: sqliv --help"

    else:
        metadata(); print ""
        parser.print_help()
