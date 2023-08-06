from .createPkg import *
import argparse
__author__ = 'xiongtianshuo'
__version__ = '0.0.8'
__all__ = [
    'NameNotSpecificationError',
    'PathNotFoundError',
    'PathNotFoundError',
    'create'
]
parser = argparse.ArgumentParser(prog='cPkg')
parser.add_argument('-v', "--version", action="store_true",
                    help="echo the this version")
parser.add_argument('-p', "--path",
                    help="path")
parser.add_argument('-n', "--dirName",
                    help="dirName")
parser.add_argument('-P', "--pkgName",
                    help="pkgName")
parser.add_argument('-a', "--author",
                    help="author")
parser.add_argument('-A', "--author_email",
                    help="author_email")
parser.add_argument('-d', "--description",
                    help="description")
parser.add_argument('-u', "--url",
                    help="url")
parser.add_argument('-Pu', "--project_urls",
                    help="project_urls", type=dict)
parser.add_argument('-c', "--classifiers",
                    help="classifiers", type=list)
parser.add_argument('-Pr', "--python_requires",
                    help="python_requires")
parser.add_argument('-i', "--install_requires",
                    help="install_requires")
args = parser.parse_args()
if args.path and args.dirName and args.pkgName and args.author and args.author_email and args.description and args.url and args.project_urls and args.classifiers and args.python_requires and args.install_requires:
    create(
        path=args.path,
        dirName=args.dirName,
        pkgName=args.pkgName,
        author=args.author,
        author_email=args.author_email,
        description=args.description,
        url=args.url,
        project_urls=args.project_urls,
        classifiers=args.classifiers,
        python_requires=args.python_requires,
        install_requires=args.install_requires
    )
