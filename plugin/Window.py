import vim

class Window:
	def __init__(self, instanceName, title, settings, height):
		'''name is the string of instance name, which is used for register events in vim
		   exmpale:  window = Window(instanceName="window", title="something", ...)
		   but current we have a problem at here. window can not be member of
		   other classs
		'''
		self.buffer = None
		self.window = None
		self.instanceName = instanceName
		self.settings = settings
		self.title = title
		self.height = height
		self.levelHandler = None
		self.unLoadHandler= None

	def show(self, position):
		if self.buffer:
			vim.command("silent! %s %dsbuffer"%(position, self.buffer.number))
			print "hi"
		else:
			#position can be 'topleft' or 'botright'
			vim.command("silent! %s 1split %s"%(position, self.title))
			#TODO:fix it
			#for setting in self.settings:
			#	vim.command("%s"%setting)
			self.buffer = vim.current.buffer

		self.window = vim.current.window
		self.window.height = self.height
		self.registerForKeyPress()
		#clean up when leave
		#vim.command('autocmd! * <buffer>')
		#if self.levelHandler:
		#	vim.command('autocmd BufLeave <buffer> py %s'(self.leveHandler))
		#if self.unLoadHandler:
		#	vim.command('autocmd BuferUnload  <buffer> py %s'(self.unLoadHandler))
	def handleKeyPress(key):
		print key

	def registerForKeyPress(self):
		numbers = charRange('0', '9')
		lowercase = charRange('a', 'z')
		uppercase = charRange('A', 'Z')
		for i in numbers + lowercase + uppercase:
			makeMap("<Char-%s>"%i, "%s.handleKeyPress"%self.instanceName, i)

	def close(self):
		if self.buffer is None:
			return
		#as command-T plugin said, on some platform
		#vim.current.buffer alway return 0.
		if vim.current.buffer.number is 0:
			vim.command("bwipeout! %s"%self.title)
		else:
			vim.command("bunload! %d"%self.buffer.number)
	
	def unload(self):
		pass

	def leave(self):
		pass
	
	def setContents(self, contents):
		self.unlock()
		self.buffer[:] = contents
		self.lock()

	def setProperty(self, prop):
		if prop not in self.settings:
			self.settings.append(prop)
		vim.command("setlocal %s" %prop)

	def lock(self):
		lockCommand = 'setlocal nomodifiable' 
		if lockCommand in self.settings:
			vim.command(lockCommand)

	def unlock(self):
		vim.command('setlocal modifiable')

	def saveExistWindowsLayout(self):
		self.windows = {}
		#FIEXME: do we need  -1 at here ?
		for i in range(len(vim.windows)):
			self.windows.append((i, vim.windows[i].height, vim.windows[i].width))
		
	def restoreWindowLayout(self):
		for i in range(len(vim.windows)):
			if vim.windows[i]:
				vim.windows[i].height = self.windows[i].height
				vim.windows[i].width = self.windows[i].width


def makeMap(key, function, param = None):
	vim.command("noremap <silent> <buffer> %s : py %s(%s)"%(key, function, param))

def charRange(start, end):
		return [chr(i) for i in range(ord(start), ord(end))]

