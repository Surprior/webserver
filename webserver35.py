import socket
#import sys
import threading

class ctrl_thr(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while True:
			a = threading.active_count()
			if a > 0:
				print(a)
			rsoc, raddr = soc.accept()
			t = accept_req(rsoc)
			t.start()

class accept_req(threading.Thread):
	def __init__(self, rsoc):
		threading.Thread.__init__(self)
		self.Rsoc = rsoc
	
	def run(self):
		r = self.Rsoc.recv(1024).decode()
		path = r.split(' ')[1]
		if path == "/":
			path += "index.html"
		print(threading.current_thread())
		print(r)
		#self.Rsoc.send(resp.encode())
		resp_f = open(base_folder + path, 'rb')
		self.Rsoc.sendfile(resp_f)
		#resp_f.seek(0)
		resp_f.close()
		self.Rsoc.close()


host = "localhost"
port = 8888

base_folder = "www"
#resp = "HTTP/1.0 200 OK\n\n Hello mag!"
#resp_f = open("index.html", 'rb')
#resp_path = sys.argv[1]
#resp_dict = {}

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind((host, port))
soc.listen(1)
print("Listening on port " + str(port))

#def gen_dict():
#	pass

t = ctrl_thr()
t.start()

s = input()
#resp_f.close()
exit()
