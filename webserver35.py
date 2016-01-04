import socket
import sys
import threading

class ctrl_thr(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while s is not "q":
			#a = threading.active_count()
			#if a > 0:
			#	print(a)
			rsoc, raddr = soc.accept()
			t = accept_req(rsoc)
			t.start()

class accept_req(threading.Thread):
	def __init__(self, rsoc):
		threading.Thread.__init__(self)
		self.Rsoc = rsoc
	
	def run(self):
		r = self.Rsoc.recv(1024).decode()
		path = ""
		#print(r)
		try:
			path = r.split(' ')[1]
		except IndexError as ierr:
			print("MAG-IndexError: {0}".format(ierr))
		
		if path == "/" or path == "":
			path = "/index.html"
		#self.Rsoc.send(resp.encode())
		print(path)
		
		if not conf_dict['Dir_trav'] and ".." in path:
			path = "/404.html"
		
		try:
			resp_f = open(conf_dict['Base_folder'] + path, 'rb')
		except FileNotFoundError as ferr:
			print("MAG-404: {0}".format(ferr))
			#print(threading.current_thread())
			#Reply with 404
			resp_f = open(conf_dict['Base_folder'] + "/404.html", 'rb')
		
		self.Rsoc.sendfile(resp_f)
		#resp_f.seek(0)
		resp_f.close()
		self.Rsoc.close()

def tf(s):
	if s == 'True':
		return True
	elif s == 'False':
		return False
	else:
		return s

# Read conf file
with open('magws.conf', 'r') as cf:
	#conf_dict = dict([line.rstrip().split(': ') for line in cf])
	conf_dict = {key: tf(val) for line in cf for (key, val) in (line.rstrip().split(': '),)}
print(conf_dict)

host = "localhost"
port = 8888

#base_folder = "www"
#resp = "HTTP/1.0 200 OK\n\n Hello mag!"
#resp_f = open("index.html", 'rb')
#resp_path = sys.argv[1]
#resp_dict = {}

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

#resp_f.close()
sys.exit(0)
