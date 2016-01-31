import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import operator
import pandas as pd
import matplotlib.pyplot as plt

def getJobs():
	#url for software engineer intern in New York,NY
	url = 'http://www.indeed.com/jobs?q=software+engineer+intern&l=New+York%2C+NY'
	#read the website
	source = urllib.request.urlopen(url).read()
	
	bs_tree = BeautifulSoup(source,'html.parser')
	
	#We get the number of jobs that have been searched
	searchCount = bs_tree.find(id = 'searchCount').get_text().split()[-1]
	searchCount = searchCount.split(sep=',')
	searchCount = ''.join(searchCount)
	searchCount = int(searchCount)
	
	num_pages = int(np.ceil(searchCount/10.0))
	print ("No of jobs is {} and no. of pages is {}".format(searchCount, num_pages))
	base_url = 'http://www.indeed.com/'
	job_links = []
	for i in range(num_pages):
		url = "http://www.indeed.com/jobs?q=software+engineer+intern&l=New+York%2C+NY&start=" + str(i*10)
		html_page = urllib.request.urlopen(url).read()
		bs_tree = BeautifulSoup(source,'html.parser')
		job_area = bs_tree.find(id='resultsCol')
		job_postings = job_area.findAll('div')
		job_postings = [jobs for jobs in job_postings if not jobs.get('class') is None and 'row' in ''.join(jobs.get('class')) and 'result' in ''.join(jobs.get('class')) ]
		job_links += [base_url+jp.a.get('href') for jp in job_postings]
		print ("Got links from page "+ str(i+1))
	print ("No of job links found is " + str(len(job_links)))
	return job_links
	
def main():
	skill_set = {'java':0, 'c++':0, 'python':0, 'php':0, 'sql':0, 'html':0, 'javascript':0, 'css':0, 'mysql':0, 'c#':0, 'ruby':0, 'matlab':0, 'nosql':0, 'mongodb':0, 'linux':0, 'unix':0, 'node.js':0, 'android':0, 'objective c':0, 'swift':0, 'ios':0, 'git':0}
	job_links = getJobs()
	for jl in job_links:
		try:	
			html_page = urllib.request.urlopen(jl).read()
		except:
			print ("Unexpected error")
			continue
		
		bs_tree = BeautifulSoup(html_page, 'html.parser')
		
		html_text = bs_tree.get_text().lower()
		html_text = html_text.replace(',',' ').replace('/', ' ').split()
		for skill in skill_set.keys():
			if skill in html_text:
				skill_set[skill] += 1;

	lst_skill_set = sorted(skill_set.items(), key = operator.itemgetter(1), reverse = True)
		
	print (lst_skill_set)
	
	skill_series = pd.Series(skill_set)
	skill_series.sort(ascending = False)
	skill_series.plot(kind='bar')
	plt.title('Software Engineer intern skills')
	plt.xlabel('Skills')
	plt.ylabel('count')
	plt.show()
				
if __name__ == "__main__":
	main()
	
	
