import os
li = os.listdir('tran_scrapy/spiders')
failed = ''
for i in range(len(li)-2):
	try:
		os.system('scrapy crawl %s'%li[i][:-3])
	except:
		failed += li[i][:-3] + '\t'
if failed:
	print('%s Failed.'%failed)