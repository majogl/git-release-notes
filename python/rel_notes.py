#!/usr/bin/env python3
import sys
import os
import subprocess
import json
import datetime
from jinja2 import Environment, FileSystemLoader

#a = datetime.strptime(, '%a %b %d %H:%M:%S %Y %z')
months = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,
		  'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def days_seconds(t):
	time,d = t.split(' ')
	time = time.split(':')
	d = [int(x) for x in d.split('-')]
	now = datetime.datetime.now()
	d,dc = datetime.date(d[0],d[1],d[2]),datetime.date(now.year,now.month,now.day)
	delta = dc - d
	days = delta.days 
	seconds = int(time[2]) + 60*(int(time[1])) + 3600*(int(time[0]))
	return (days,seconds)

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
		self.raw = out.decode(sys.stdout.encoding)
		self.commit_list = []
		self.process_log()

	def process_log(self):
		print(self.raw)
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
					if self.t1 != '' and self.t1 in line:
						self.fro = new_commit['id']
					elif self.t2 != '' and self.t2 in line:
						self.til = new_commit['id']
			elif line.split(' ')[0][:-1] == 'Date':
				temp = line.split(' ')
				key,data = temp[0][:-1],' '.join(temp[1:])
				data = (data.strip()).split(' ')
				#H:M:S D-M-Y
				data = '{} {}-{}-{}'.format(data[3],data[4],months[data[1]],data[2])
				print(data)
				new_commit[key] = data
				new_commit['D_S'] = days_seconds(data)
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

	def make_jinja(self):
		j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
							 trim_blocks=True)
		print(j2_env.get_template('template.html').render(title='Hellow Gist from GutHub'))

com = GetLog(pth='/home/majo/vpp',branch='stable/1701',tag1='17.01.6',tag2='17.01.7')
com.make_jinja()
#print(com.commit_list[0])
#print(com.commit_list[1])
#print(com.fro, com.til)
#com.dump()
#print(com.get_raw_output())
#days_seconds("1:0:0 25-6-2017")
#proc = subprocess.Popen(['ls', '-al'],stdout=subprocess.PIPE,cwd='/home/majo/vpp')
#out, err = proc.communicate()
#print(out.decode(sys.stdout.encoding))
