import socket
import thread

host = "localhost"
port = 8888

resp = "HTTP/1.0 200 OK\n\n Hello mag!"

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind((host, port))
soc.listen(1)
print "Listening on port " + str(port)

def ctrl_thr():
	while True:
		rsoc, raddr = soc.accept()
		thread.start_new_thread(accept_req, (rsoc,))

def accept_req(rsoc):
	r = rsoc.recv(1024)
	print r
	rsoc.send(resp)
	rsoc.close()

thread.start_new_thread(ctrl_thr, ())

raw_input()
