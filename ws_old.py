class accept_req(threading.Thread):
	def __init__(self, rsoc, raddr):
		threading.Thread.__init__(self)
		self.Rsoc = rsoc
		self.Raddr = raddr
	
	def run(self):	# Vurdere a splitte path
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
			kwargs = "?" + kwargs
		
		print_(self.Raddr, "\t")
		print_(path, "\t")
		print_(kwargs, "\t")
		if path == "/" or path == "":
			path = "/index.html"
		
		if not conf_dict['Dir_trav'] and ".." in path:
			path = "/404.html"
		
		if ".py" in path:
			if kwargs:
				kwargs = parse_kwargs(kwargs)
			else:
				kwargs = {}
			mpath = conf_dict['Base_folder'] + "%s" % path.replace(".py", "").replace("/", ".")
			reply = __import__(mpath, globals(), locals(), fromlist=[conf_dict['Base_folder']], level=0).run(kwargs)
			print_(reply, "\n")
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
			print_(path, "\n")
		
		self.Rsoc.close()

# Parse
def parse_kwargs(kwargs):
	return dict(urlparse.parse_qsl(urlparse.urlsplit(kwargs).query))

def tf(s):
	if s == 'True':
		return True
	elif s == 'False':
		return False 
	else:
		return s

def print_(p, e):
	if p:
		print(p, end=e)
	else:
		print("-", end=e)
