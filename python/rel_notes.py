#!/usr/bin/env python3
import sys
import os
import subprocess
import json
from jinja2 import Environment, FileSystemLoader
from lib import *

#a = datetime.strptime(, '%a %b %d %H:%M:%S %Y %z')

class GetLog:
	class Commit:
		def __init__(self,data):
			self.raw = data
			for key in data:
				if data[key] != '':
					d,k = data[key], key
					if '"' in d:
						d = d.replace('"','*')
					command = 'self.{} = "{}"'.format(k,d)
					exec(command)

		def __str__(self):
			out = ''
			for key in self.raw:
				out += '{} -> {}\n'.format(key, self.raw[key])
			return out

	def __init__(self,pth='.',branch='master',tag1='',tag2=''):
		_COMMAND = ['git','log', branch,'--decorate']
		self.t1, self.t2 = tag1,tag2
		proc = subprocess.Popen(_COMMAND,stdout=subprocess.PIPE,cwd=pth)
		out,err = proc.communicate()
		self.raw = out
		self.commit_list = []
		self.process_log()

	def process_log(self):
		raw = self.raw.split('\n')
		new_commit = dict()
		commit_text = ''
		for line in raw:
			line = line.strip()
			if line == '':
				continue
			if line[:7] == 'commit ':
				if new_commit != dict():
					new_commit['commit_text'] = commit_text
					commit_text = ''
					self.commit_list.append(self.Commit(new_commit))
				new_commit = dict()
				new_commit['id'] = line.split(' ')[1]
				if '(' in line:
					new_commit['tag'] = '(' + line.split('(')[1]
					cont = self.t1+')' in line or self.t1+',' in line
					if self.t1 != '' and cont:
						self.fro = len(self.commit_list)
					cont = self.t2+')' in line or self.t2+',' in line
					if self.t2 != '' and cont:
						self.til = len(self.commit_list)
			elif line.split(' ')[0][:-1] == 'Date':
				temp = line.split(' ')
				key,data = temp[0][:-1],' '.join(temp[1:])
				data = (data.strip()).split(' ')
				#H:M:S D-M-Y
				data = '{} {}-{}-{}'.format(data[3],data[4],months[data[1]],data[2])
				new_commit[key] = data
			elif line.split(' ')[0][:-1] in ['Merge','Author','Change-Id','Signed-off-by']:
				temp = line.split(' ')
				key,data = temp[0][:-1],' '.join(temp[1:])
				key = key.replace('-','_')
				if not key in new_commit.keys():
					new_commit[key] = data.strip()
				else:
					new_commit[key.strip()] += '||' + data.strip()
			else:
				commit_text += line + '|N|'
	def get_raw_output(self):
		return self.raw
	def order_commits_by_id(self):
		res = dict()
		for commit in self.commit_list:
			res[commit.id] = commit.raw

	def dump(self):
		with open('result.json','w') as f:
			res = dict()
			for commit in self.commit_list:
				res[commit.id] = commit.raw
			f.write(json.dumps(res, indent=2, sort_keys=False) + '\n')

	def make_jinja(self,tmpl='template.html'):
		j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
							 trim_blocks=True)
		template = j2_env.get_template('templates/' + tmpl)
		CL = []
		for commit in self.commit_list:
			begin,end = self.commit_list[self.fro].Date, self.commit_list[self.til].Date
			if delta_time(commit.Date,(begin,end)):
				commit.commit_text = commit.commit_text.replace('|N|','\n')
				CL.append(commit)
		print(template.render(version = self.t2,commit_list = CL))

"""
print(com.commit_list[0])
print(com.commit_list[1])
print(com.fro, com.til)
com.dump()
temp = com.commit_list[0].raw
for key in temp:
	print(key,temp[key])
print(com.get_raw_output())
days_seconds("1:0:0 25-6-2017")
proc = subprocess.Popen(['ls', '-al'],stdout=subprocess.PIPE,cwd='/home/majo/vpp')
out, err = proc.communicate()
print(out.decode(sys.stdout.encoding))
"""
