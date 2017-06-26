#!/usr/bin/python2
import sys
import os
import subprocess
import json
from datetime import *

#a = datetime.strptime(, '%a %b %d %H:%M:%S %Y %z')

months = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,
		  'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}

class GetLog:
	class Commit:
		def __init__(self,data):
			self.raw = data
			for key in data:
				if data[key] != '':
					d,k = data[key], key
					command = 'self.{} = "{}"'.format(k,d.replace('"','*'))
					exec(command)

		def __str__(self):
			out = ''
			for key in self.raw:
				out += '{} -> {}\n'.format(key, self.raw[key])
			return out

	def __init__(self):
		_COMMAND = ['git','log','--decorate']
		self.raw = subprocess.check_output(_COMMAND)
		self.raw = self.raw
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
			elif line.split(' ')[0][:-1] == 'Date':
				temp = line.split(' ')
				key,data = temp[0][:-1],' '.join(temp[1:])
				data = (data.strip()).split(' ')
				#H:M:S D-M-Y
				data = '{} {}-{}-{}'.format(data[3],data[2],months[data[1]],data[4])
				print(data)
				new_commit[key] = data.strip()
			elif line.split(' ')[0][:-1] in ['Merge','Author','Change-Id','Signed-off-by']:
				temp = line.split(' ')
				key,data = temp[0][:-1],' '.join(temp[1:])
				key = key.replace('-','_')
				if not key in new_commit.keys():
					new_commit[key] = data.strip()
				else:
					new_commit[key.strip()] += '||' + data.strip()
			else:
				commit_text += line
	def get_raw_output(self):
		return self.raw

	def dump(self):
		with open('result.json','w') as f:
			res = dict()
			for commit in self.commit_list:
				res[commit.id] = commit.raw
			f.write(json.dumps(res, indent=2, sort_keys=True) + '\n')
			

com = GetLog()
print(com.commit_list[0])
print(com.commit_list[0])
#com.dump()
#print(com.get_raw_output())
