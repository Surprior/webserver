
class httpReq(self):
	def httpParseHeader(self, str):
		lines, self.body = splitReq(str)
		
		self.metode, self.path, self.version = lines[0].split(' ')
		self.fields = {}
		
		for line in lines[1:]:
			line = line.decode()
			field, value = line.split(": ", 1)
			self.fields[field] = value
	
	def httpParseBody(self, str)
		self.body += str
		
	def splitReq(str):
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
	
	def httpParse(self, reqStr):
		lines = reqStr.splitlines()
		
		self.metode, self.path, self.version = lines[0].split(' ')
		self.fields = {}
		self.body = ""
		
		self.moreBody = False
		
		for line in lines[1:]:
			if line not in ('\n', '\r\n'):
				if not self.moreBody:
					field, value = line.split(": ", 1)
					self.fields[field] = value
				else:
					self.body += line
			else:
				self.moreBody = True
		if len(self.body) < int(fields['Content-Length']):
			self.body = self.body.decode()
			self.moreBody = False				# hva skal den returnere når content-length er feil eller mangler?

class httpRes(self):
	def __init__(self):
		self.code = ""

class httpHandler(threading.Thread):
	def __init__(self, rsoc, raddr):
		threading.Thread.__init__(self)
		self.rsoc = rsoc
		self.raddr = raddr
		
		self.httpreq = httpReq()
		self.httpres = httpRes()
		
	
	def run(self):
		self.reqStr = recvAll()
		self.httpreq = httpReq(self.reqStr)
		#Do the right stuff (TM)
		self.httpres = httpRes(self."The right stuff (TM)")
		sendAll(httpres)
		
	
	def recvAll(self):
		str = self.rsoc.recv(4096)
		self.httpreq.httpParseHeader(str)
		if self.httpreq.metode == 'POST':
			if self.httpreq.fields['Content-Length']:
				while self.httpreq.body < self.httpreq.fields['Content-Length']:
					part = self.rsoc.recv(4096)
					if not part:
						break
					self.httpreq.httpParseBody(part)
				self.body = self.body.decode()
			else:
				self.httpres.code = "411"
	
	def sendAll(self):
		#placeholder
		
