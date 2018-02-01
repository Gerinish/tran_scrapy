import os
li = os.listdir('tran_scrapy/spiders')
for i in range(len(li)-2):
	try:
		os.system('scrapy crawl %s'%li[i][:-3])
	except:
		pass