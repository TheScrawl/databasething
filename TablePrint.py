#This module was written by The Scrawl
#Please check out it's github repo: https://github.com/TheScrawl/TablePrint

def table(*argv):
	longestStr = 0
	longestData = 0
	for data in argv:
		if len(data) > longestData:
			longestData = len(data)
		for i in data:
			if len(str(i)) >= longestStr:
				longestStr = len(str(i))
	dataSetCount = 0
	for dataSet in argv:
		dataSetCount = dataSetCount + 1
		itemCount = 0
		if itemCount == 0:
			print('\n' + '-'*(longestStr * longestData + longestData + len(dataSet) + 1))
		else:
			print('-'*(longestStr * longestData + longestData + 1))
		print('|', end='')
		for item in dataSet:
			itemCount = itemCount + 1
			if itemCount <= len(dataSet):
				print(str(item) + ' ' * (longestStr - len(str(item)) + 1), end = '|')

		x = len(dataSet)
		while x < longestData:
			print(' ' * longestStr, end = '|')
			x = x + 1
	print('\n' + '-'*(longestStr * longestData + longestData + len(dataSet) + 1))