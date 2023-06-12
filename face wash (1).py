import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep


headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
'Accept-Language': 'en-US, en;q=0.5'
}

search_query = 'Face Wash'.replace(' ', '+')
base_url = 'https://www.amazon.in/s?k={0}'.format(search_query)

items = []
for i in range (1,20):
	print('Processing {0}...'.format(base_url +'&page = {0}'.format(i)))
	response = requests.get(base_url+'&page={0}'.format(i), headers = headers)
	soup = BeautifulSoup(response.content, 'html.parser')

	results = soup.find_all('div',{'class': 's-result-item', 'data-component-type':'s-search-result'})
	
	for results in results:
		product_category = 'Face Wash'
		try:
			#rating = results.find('i',{'class':"a-icon"}).text
			product_URL = 'https://amazon.in'+ results.a['href']

			items.append([product_URL, product_category])

		except AttributeError:
			continue
	sleep(0.5)

print(len(product_URL))

df = pd.DataFrame(items,columns = ['product_URL','product_category'])
df.to_csv('{0}.csv'.format(search_query),index = False)