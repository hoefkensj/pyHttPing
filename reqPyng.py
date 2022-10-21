#!/usr/bin/env python
import sys,requests,socket,urllib.request
from time import perf_counter_ns,time_ns,sleep
from datetime import datetime as t
from multiprocessing import Process,Value
from timeit import default_timer

logg_startblock="""
###############################################################
# Starting...\n\n\n
###############################################################
DATE:\t{dte()}
ADDRESSES:
\tLocal:\tIPv4:{l}\tHOST:{r}
\tPublic:\tIPv4:{p}
\tRemote:\tIPv4:{r}\tTLD:{url}\n\n
###############################################################
"""

def tt():
	return [*str(t.now()).split()[0].split('-'),*[ int(s) for s in str(t.now()).split()[1].split('.')[0].split(':')]]

def next_hour(saved=[]):
	h=tt()[3]
	sh=saved.pop() if saved else h
	saved+=[h]
	return sh != h

def logg(t,c='a',buffer=[]):
	if c =='a':
		buffer+=[t]
	elif c == 'w':
		lines = ''.join(buffer)
		sys.stdout.write(lines)
		sys.stdout.flush()
		with open('pong.log', 'a') as file:
			llines= lines.split('\n')
			for line in llines:
				file.write(line)

def http(**k):
	host='http://{addr}'.format(addr=k.get('addr'))
	code=k.get('code')
	stime=k.get('stime')
	rtime=k.get('rtime')
	stime.value=time_ns()
	try:
		head=requests.head(host, timeout=3000)
		code.value=head.status_code
	except requests.exceptions.ConnectionError:
		code.value=-1
	except requests.exceptions.ReadTimeout:
		code.value=-2
	rtime.value=time_ns()
	ret={
		'code' : code,
		'stime': stime,
		'rtime': rtime,	}
	return ret

def reslv(addr):
	def reslv():
		r		=	addrs(addr)
		return r
	return reslv

def addrs(url):
	def local():
		logg(f'Getting local IP:\t')
		l = socket.gethostbyname(socket.gethostname())
		logg(f'OK\n' if l	else f'ERROR\n')
		return l
	def public():
		logg(f'Getting Public IP:\t')
		p = urllib.request.urlopen('https://ident.me').read().decode('utf8')
		logg(f'OK\n' if p	else f'ERROR\n')
		return p
	def remoteip():
		logg(f'Getting Remote IP:\t')
		r 	= socket.gethostbyname(url)
		logg(f'OK\n' if r	else f'ERROR\n')
		return r
	def remotehn():
		n		=	socket.gethostname()
		return n
	a={
	'l':local(),
	'p':public(),
	'r':remoteip(),
	'n':remoteip(),
		}
	return a

def main():

	while True:
			now=tt()
			sex = now[2]

			logtme=f'{now[3]}:{now[4]}:{now[5]:02} - '
			ret_code  = Value("i", 0, lock=False)
			ret_stime	= Value("i", 0, lock=False)
			ret_rtime	= Value("i", 0, lock=False)
			code=ret_code
			stime=ret_stime
			rtime=ret_rtime
			addr=addr
			proc=Process(target=http, args=(code,stime,rtime,addr))
			tstart=time_ns()
			stats=proc.start()

			while True:
				tpass=time_ns()-tstart
				if ret_code!=0:
					break
				else:
					sleep(1*10**-1)


				line = 'online' if ret_value in [200,301] else 'offline'
				timed = ret_time.value
				if timed > ttl:
					logg(f'{logtme} - \x1b[31m{line}\x1b[0m -  \x1b[31m>timeout ({ttl *1*10**-6 :.0f}ms)\x1b[0m\n')
				else:
					logg(f'{logtme} {line} - +{timed*1*10**-6 :.0f}ms\n')
				sleep(d - divmod(int(sex), d)[1])  # get seconds past minute , find remaining till next 1/6min (10secs) sleep that amount

# def cnt_retry():
# 	logg('REMOTE NOT REACHABLE\nRETRYING IN ')
# 	ss=[00,10,5,2,1,1];	cs=[20,10,5,3,2,1]
# 	for c,s in zip(cs,ss):
# 		sleep(s)
# 		logg(f'{c}s ... ')
