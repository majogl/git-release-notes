import os
import datetime
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

def delta_time(Dat,rangeD):
	DS_begin,DS_end = days_seconds(rangeD[0]),days_seconds(rangeD[1])
	D = days_seconds(Dat)
	if DS_end[0] < DS_begin[0]:
		DS_begin,DS_end = DS_end,DS_begin
	if D[0] in range(DS_begin[0]+1,DS_end[0]):
		return True
	elif D[0] == DS_begin[0] and D[1] >= DS_begin[1]:
		return True
	elif D[0] == DS_end[0] and D[1] <= DS_end[1]:
		return True
	else:
		return False
"""
print(delta_time('12:00:00 2017-01-05',('12:00:00 2017-01-04','12:00:00 2017-01-06')))
print(delta_time('12:00:00 2017-01-05',('12:00:00 2016-12-04','12:00:00 2017-02-06')))
print(delta_time('12:00:00 2017-01-05',('12:00:00 2017-01-05','12:00:00 2017-01-05')))
print(delta_time('12:00:00 2017-01-05',('11:00:00 2017-01-05','13:00:00 2017-01-05')))
print(delta_time('12:00:00 2017-01-05',('11:59:00 2017-01-05','12:01:00 2017-01-05')))
print(delta_time('12:00:00 2017-01-05',('12:00:00 2017-01-05','12:05:00 2017-01-05')))
"""
