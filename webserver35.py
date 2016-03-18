import socket
import sys
import threading
import urllib.parse as urlparse
from importlib import import_module
from modules.maghttp import *

"""
Ulike trader akksessere samme ressurs.
	hver enkelt trad ma ha tilgang til conf_dict
	chaching av statiske filer for kortere responstid
	
	Felles omrade som alle trader har lesetilgang til
		liste med navn/id pa cachede filer	\
		liste med selve filene				 -> Dict{filnavn: innhold}
		
	mulighet til a skrive til cachen mens andre leser
	
	request for X -> er X statisk? -> ja -> se om X er i cache -> ja -> send X
								|							\-> nei -> apne fil X -> send X -> legg X til i cache
								\-> Nei -> opne og kjor X -> send X / resultat
		ting som kan ga galt: 	X eksister ikkje
								oppstar feil nar X kjorer
"""

class ctrl_thr(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while True:
			rsoc, raddr = soc.accept()
			t = httpHandler(rsoc, raddr)
			t.start()

def tf(s):
	if s == 'True':
		return True
	elif s == 'False':
		return False 
	else:
		return s

#Read conf file
with open('magws.conf', 'r') as cf:
	conf_dict = {key: tf(val) for line in cf for (key, val) in (line.rstrip().split(': '),)}
print(conf_dict)

host = "localhost"
port = 8888

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind((host, port))
soc.listen(1)
print("Listening on port " + str(port))

s = ""

t = ctrl_thr()
t.daemon = True
t.start()

while True:
	s = input()
	if s == "q":
		print("Quitting!")
		break
	elif s == "c":
		print(threading.active_count())
	elif s == "e":
		print(threading.enumerate())
	elif s == "dt":
		conf_dict['Dir_trav'] = True
		print(conf_dict['Dir_trav'])
	elif s == "df":
		conf_dict['Dir_trav'] = False
		print(conf_dict['Dir_trav'])

sys.exit(0)
