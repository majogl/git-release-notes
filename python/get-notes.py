import argparse
from rel_notes import *

parser = argparse.ArgumentParser()

parser.add_argument('-b', '-branch',help='Name of branch to make the log\
					from. Default branch master', dest='branch', default='master')
parser.add_argument('-t', '-template', help='A template in the templates folder\
					that you wish to use. Full name.', dest='tmpl', default='html')
parser.add_argument('working_directory',help='Full path to working\
					directory directory. Default current directory',
					metavar='wcd', nargs='?', default = os.getcwd())
parser.add_argument('tags', help='The tags denoting range from which \
					to list commits  e.g. tag1..tag2')
args = parser.parse_args()
tags = args.tags.split('..')

handle = GetLog(pth = args.working_directory,
				branch = args.branch,
				tag1 = tags[0],
				tag2 = tags[1])

handle.make_jinja(args.tmpl)
