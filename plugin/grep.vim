python <<EOF
def getCurrentWord():
	seps = [' ', ',','(',')',':','+', '-', '*', '/','\\','[',']','{','}','.','`','!','@','#','$','%','^', '&','*','=', '|','?','<','>', ';']	
	(row, col) = vim.current.window.cursor
	if vim.current.line[col] in seps:
		return vim.current.line[col]
	left = col
	right = col
	while left >=0 and vim.current.line[left] not in seps:
		left = left - 1
	while right < len(vim.current.line) and vim.current.line[right] not in seps:
		right = right + 1
	left = max(0, left)
	right = min(right, len(vim.current.line) -1)
	return vim.current.line[left:right]

def grepWordInCurrentBuffer():
	word = getCurrentWord()	
	lineNum = 1
	results = []
	for line in vim.current.buffer:
		if line.find(word) != -1:
			results.append("%d:%s"%(lineNum, line))
		lineNum = lineNum + 1

	if results:
		showResults("findResults:", results, "grepWordInCurrentBufferHandler")

def grepWordInCurrentBufferHandler(windowId, hideCurrent):
	content = vim.current.line
	temp = content.split(":")
	try:
		lineNum = int(temp[0])
	except:
		return
	if hideCurrent:
		vim.command("hide")
	vim.command("%d wincmd w"%windowId) #move focus to windowId
	vim.command("%d"%lineNum) #jump to that line

def grepWordInBundle():
	word = getCurrentWord()
	(onlyfindInBufferList, fileNamePattern) = getFindFileArgs()
	if not fileNamePattern:
		return
	fileNames = []
	fileNames.extend(MyFinder.findFileInBufferList(fileNamePattern))
	if not onlyfindInBufferList:
		fileNames.extend(MyFinder.findFileInPaths(fileNamePattern, paths))
	results = grepWordInFiles(word, fileNames)
	if results:
		showResults("findResults:", results, "grepWordInBundleHandler")

def grepWordInBundleHandler(windowId, hideCurrent):
	content = vim.current.line
	temp = content.split(":")
	try:
		(lineNum, filePath) = (int(temp[0]), temp[1])
	except:
		return
	if hideCurrent:
		vim.command("hide")
	vim.command("%d wincmd w"%windowId) #move focus to windowId
	vim.command("e %s"%filePath)
	vim.command("%d"%lineNum) #jump to that line
	
def grepWordInFiles(word, filePaths):
	results = []
	for filePath in filePaths:
		lineNum = 1
		for line in open(filePath).readlines():
			if line.find(word) != -1:
				results.append("%d:%s:%s"%(lineNum,filePath,line))
			lineNum = lineNum + 1
	return results
EOF
