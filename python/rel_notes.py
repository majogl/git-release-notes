import sys
import os
import subprocess
import json

#a = datetime.strptime("Mon Jan 2 14:29:21 2017 +0200", '%a %b %d %H:%M:%S %Y %z')

class GetLog:
	class Commit:
		def __init__(self,data):
			self.raw = data
			for key in data:
				if data[key] != '':
					command = 'self.{} = "{}"'.format(key,data[key].replace('"','*'))
					exec(command)

		def __str__(self):
			out = ''
			for key in self.raw:
				out += '{} -> {}\n'.format(key, self.raw[key])
			return out

	def __init__(self):
		_COMMAND = ['git','log','--decorate']
		self.raw = subprocess.check_output(_COMMAND)
		self.raw = self.raw.decode('utf-8')
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
			elif line.split(' ')[0][:-1] in ['Merge','Author','Date','Change-Id','Signed-off-by']:
				temp = line.split(' ')
				key,data = temp[0][:-1],' '.join(temp[1:])
				key = key.replace('-','_')
				if not key in new_commit.keys():
					new_commit[key] = data.strip()
				else:
					new_commit[key.strip()] += '||' + data.strip()
			else:
				commit_text += str(line)
	def get_raw_output(self):
		return self.raw

	def dump(self):
		with open('result.json','w') as f:
			for commit in self.commit_list:
				f.write(json.dumps(commit.raw, indent=2, sort_keys=True))

com = GetLog()
print(com.commit_list[0])
com.dump()
#print(com.get_raw_output())
