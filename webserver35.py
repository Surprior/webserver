import socket
import sys
import threading
from importlib import import_module

class ctrl_thr(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while s is not "q":
			rsoc, raddr = soc.accept()
			t = accept_req(rsoc, raddr)
			t.start()

class accept_req(threading.Thread):
	def __init__(self, rsoc, raddr):
		threading.Thread.__init__(self)
		self.Rsoc = rsoc
		self.Raddr = raddr
	
	def run(self):	# Vurdere å splitte path
		r = self.Rsoc.recv(1024).decode()
		path = ""
		kwargs = ""
		
		try:
			path = r.split(' ')[1]
		except IndexError as ierr:
			1 == 1
			#print("MAG-IndexError: {0}".format(ierr), end="\t")
		
		if "?" in path:
			path, kwargs = path.split("?", 1)
		
		print(self.Raddr, end="\t")              
		print(path, end="\t")
		if path == "/" or path == "":
			path = "/index.html"
		
		if not conf_dict['Dir_trav'] and ".." in path:
			path = "/404.html"
		
		if ".py" in path:
			if kwargs:
				kwargs = parse_kwargs(kwargs)
			mpath = conf_dict['Base_folder'] + "%s" % path.replace(".py", "").replace("/", ".")
			reply = __import__(mpath, globals(), locals(), fromlist=[conf_dict['Base_folder']], level=0).run()
			print(reply)
			self.Rsoc.send(reply.encode('utf-8'))
		else:
			try:
				resp_f = open(conf_dict['Base_folder'] + path, 'rb')
			except FileNotFoundError as ferr:
				#print("MAG-404: {0}".format(ferr))
				path = "/404.html"
				resp_f = open(conf_dict['Base_folder'] + path, 'rb')
			self.Rsoc.sendfile(resp_f)
			resp_f.close()
			print(path, end="\n")
		
		self.Rsoc.close()

# Parse
def  parse_kwargs(kwargs):
	d_kwargs = {}
	
	
	return d_kwargs

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
