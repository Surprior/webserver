import threading
import urllib.parse as urlparse
from importlib import import_module

class httpReq:
	def httpParseHeader(self, str):
		print("=> " + str)
		lines, self.body = self.splitReq(str)
		
		#print("\n".join(lines))
		
		self.metode, self.path, self.version = lines[0].split(" ")
		self.fields = {}
		self.kwargs = {}
		
		if "?" in self.path:
			self.path, self.kwargs = self.path.split("?", 1)
			self.kwargs = dict(urlparse.parse_qsl(urlparse.urlsplit("?" + self.kwargs).query))
		
		if self.path == "/" or self.path == "":
			self.path = "/index.html"
		
		for line in lines[1:]:
			field, value = line.split(": ", 1)
			self.fields[field] = value
	
	def httpAppendBody(self, str):
		self.body += str
	
	def append():
		self.kwargs["body"] = self.body
	
	def splitReq(self, str):
		lines = str.splitlines()
		before = True
		h = []
		b = []
		for line in lines:
			if line != '':
				if before:
					h.append(line)
				else:
					b.append(line)
			else:
				before = False
		return h, "".join(b)


class httpRes:
	def __init__(self):
		self.version = "HTTP/1.1"
		self.code = ""
		self.shortDisc = {200: "OK", 404: "Not Found", 400: "Bad Request"}
		self.body = ""
		self.server = "magServHTTP v 0.1"
	
	def str(self):
		r = ""
		r += self.version + " " + self.code + " " + self.shortDisc[int(self.code)] + "\r\n"
		r += "Server: " + self.server + "\r\n"
		r += "Content-Type: text/html\r\n"
		r += "Connection: Closed\r\n"
		if self.body:
			r += "Content-Length: " + str(len(self.body)) + "\r\n"
			r += "\r\n" + self.body
		return r

class httpHandler(threading.Thread):
	def __init__(self, rsoc, raddr):
		threading.Thread.__init__(self)
		self.rsoc = rsoc
		self.raddr = raddr
		
		self.httpreq = httpReq()
		self.httpres = httpRes()
	
	def run(self):
		if self.recvAll():
			self.openFile()
			self.sendAll()
		self.rsoc.close()
	
	def recvAll(self):
		str = self.rsoc.recv(4096).decode()
		if str == "":
			return False
		self.httpreq.httpParseHeader(str)
		if self.httpreq.metode == 'POST':
			if self.httpreq.fields['Content-Length']:
				while self.httpreq.body < self.httpreq.fields['Content-Length']:
					part = self.rsoc.recv(4096).decode()
					if not part:
						break
					self.httpreq.httpAppendBody(part)
				self.hrrpreq.append()
			else:
				self.httpres.code = "411"
		return True
	
	def sendAll(self):
		s = self.httpres.str().encode('utf-8')
		self.rsoc.send(s)
	
	def openFile(self):
		try:
			if ".py" in self.httpreq.path[-3:]:
				mpath = "www" + "%s" % self.httpreq.path.replace(".py", "").replace("/", ".")		#fix later
				reply = __import__(mpath, globals(), locals(), fromlist=["www"], level=0).run( {**self.httpreq.kwargs, **self.httpreq.fields} )	#må lage en test for "503"
			else:
				f = open("www" + self.httpreq.path, 'r')
				reply = f.read()
				f.close()
			self.httpres.code = "200"
		except (FileNotFoundError, ImportError) as err:
			reply = open("www" + "404.html", 'rb')
			self.httpres.code = "404"
			
		self.httpres.body = reply
		
		
		
