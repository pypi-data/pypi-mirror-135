# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['pcurate']
install_requires = \
['docopt>=0.6.2,<0.7.0']

entry_points = \
{'console_scripts': ['pcurate = pcurate:main']}

setup_kwargs = {
    'name': 'pcurate',
    'version': '0.1.6',
    'description': 'utility for curating Arch Linux software package lists',
    'long_description': '## pcurate\n\nPcurate is a command line utility with the purpose of \'curating\' or carefully arranging lists of explicitly installed Arch Linux software packages.\n\nI created this because I was often updating text files with lists of installed software and notes concerning many packages.  It became a chore to manage that information for a number of uniquely configured hosts, and keeping it in sync with changes.\n\nThis utility provides a convenient way to organize software stacks into package lists which can either be fed back to the package manager for automatic installation, or simply used for reference and planning.\n\n### Features include\n\n - Tagging/categorization of curated packages, for easier filtering and sorting\n - Alternate package descriptions can be set, such as the reason for installation\n - Data is exportable to a simple package list or comma delimited (csv) format\n - Optional filter.txt file for specifying packages or package groups to be excluded\n - Option to limit display output to only include either native or foreign packages\n\nNote:  Package version information is untracked because Arch Linux is a rolling release distribution, and this utility is not meant to aid in maintaining partial upgrades.  If needed, notes on versioning can be stored in a package tag or description attribute.\n\n###  Installation\n\nInstall or upgrade to latest version using pip\n\n\t$ python -m pip install pcurate --user --upgrade\n\n### Usage\n\n\t$ pcurate -h\n\tpcurate\n\n\tUsage:\n\t  pcurate PACKAGE_NAME [-u | -s [-t TAG] [-d DESCRIPTION]]\n\t  pcurate ( -c | -r | -m ) [-n | -f] [-v]\n\t  pcurate ( -h | --help | --version)\n\n\tOptions:\n\t  -u --unset              Unset package curated status\n\t  -s --set                Set package curated status\n\t  -t tag --tag tag        Set package tag\n\t  -d desc --desc desc     Set package description\n\t  -c --curated            Display all curated packages\n\t  -r --regular            Display packages not curated\n\t  -m --missing            Display missing curated packages\n\t  -n --native             Limit display to native packages\n      -f --foreign            Limit display to foreign packages\n\t  -v --verbose            Display additional info (csv)\n\t  -h --help               Display help\n\t  --version               Display pcurate version\n\n### Examples\n\nDisplay information for a package\n\n\t$ pcurate firefox\n\nSet a package as curated status (a keeper)\n\n\t$ pcurate -s neovim\n\nUnset a package to revoke its curated status (and remove any tag or custom description)\n\n\t$ pcurate -u emacs\n\nSet a package with an optional tag and custom description\n\n\t$ pcurate -s mousepad -t editors -d "my cat installed this"\n\n\nThe following is a command I use to interactively mark multiple packages as curated.  **Tab** or **Shift**+**Tab** to mark or unmark, commit with **Enter** or cancel with **Esc**.  This requires [fzf](https://archlinux.org/packages/community/x86_64/fzf/) to be installed.\n\n\t$ pcurate -r | fzf -m | xargs -I % pcurate -s %\n\n#### Package List examples\n\nDisplay a list of regular packages (those which are installed but not yet curated)\n\n\t$ pcurate -r\n\nDisplay a list of curated packages that are missing (either no longer installed or their install reason has been changed to dependency).\n\n\t$ pcurate -m\n\nSet curated status for all packages listed in an existing pkglist.txt file (a simple text file containing a newline separated list of package names)\n\n\t$ cat pkglist.txt | xargs -I % pcurate -s %\n\nExport all curated native packages to a new pkglist.txt file\n\n\t$ pcurate -c -n > pkglist.txt\n\nSend the resulting pkglist.txt to package manager for automatic installation\n\n\t$ pacman -S --needed - < pkglist.txt\n\nWrite a detailed list of curated packages to csv format so you can view it as a spreadsheet, etc.\n\n\t$ pcurate -c -v > pkglist.csv\n\n#### Configuration\n\n**$XDG_CONFIG_HOME/pcurate** or **~/.config/pcurate** is the default location for the package database and filter.txt file.  The optional filter.txt file is a simple newline separated list of packages or package groups.  Single line comments can also be added.\n\nAny packages or members of package groups listed in the filter.txt will be purged from the pcurate database and excluded from command output.  Filter rules are only applied against regular packages.\n\n### License\nThe MIT License (MIT)\n\nCopyright © 2021 Scott Reed',
    'author': 'Scott Reed',
    'author_email': 'multivac@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thegibson/pcurate',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
