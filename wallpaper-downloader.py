from requests_cache import CachedSession
from bs4 import BeautifulSoup
from datetime import datetime
import time
import os
# import requests


categories: list = [
"abstract",
"animals",
"anime",
"car",
"celebration",
"city",
"fantasy",
"flowers",
"food",
"funny",
"life",
"military",
"music",
"nature",
"quotes",
"romantic",
"space",
"sport",
"technics",
"AIgenerated"
]
# categories = ['']

for selected_category in categories:

	# if selected_category in ['abstract','nature','anime','technics',"car","celebration","animals"]:
	# 	continue
	# selected_category = categories[2]
	base_url: str = "https://backiee.com/categories/"

	stored_links: set = set()
	download_links: set = set()
	print(f"Dwnloading {selected_category} wallpapers...")
	def get_links(page,category):
		
		target_url: str = f"{base_url}{category}?page={page}"
		if selected_category == 'AIgenerated':
			if page == 1:

				target_url: str = "https://backiee.com/ai-generated-wallpapers"
			else:
				target_url: str = f"https://backiee.com/ai-generated-wallpapers?page={page}"
		session = CachedSession(
			cache_name=f"cache/{selected_category}_{page}",
			expire_after=864000)
		
		res = session.get(f"{target_url}")

		soup = BeautifulSoup(res.text,'html.parser')

		links = soup.find_all('div',class_='col-sm-4 col-md-4')

		for href in links:
			href_value = href.find('a')
			redirect_link = href_value['href']
			stored_links.add(redirect_link)


	for page in range(5,22):
		# print(page)
		print(f"Scrapping from page : {page}",end='\r')
		get_links(page=page,category=selected_category)

	# print('\r')
	print("All page Scrapped")
	print(f"Total links found : {len(stored_links)}")

	print("Scrapping downloadable links...")
	for i,each_url in enumerate(stored_links):
		# print(each_url)
		
		session2 = CachedSession(
			cache_name=f"cache/{each_url}",
			expire_after=86400)
		res2 = session2.get(each_url)
		soup = BeautifulSoup(res2.text,'html.parser')
		raw_html = soup.find('a',class_="dropdown-item")
		href_value = raw_html['href']
		fname = raw_html['download']
		download_links.add((href_value,fname))
		print(f"No. of links scrapped : {i+1}",end='\r')

	# print("\r")
	print(f"Total download links scrapped = {len(stored_links)}")
	i=0
	print("Downloading images...")
	for link,filename in download_links:
		
		i+=1
		print(f"Downloading {i}/{len(stored_links)}",end='\r')
		session3 = CachedSession(
			cache_name=f"cache/{link}",
			expire_after=864000)
		res3 = session3.get(link)
		# curr_datetime = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
		
		if not os.path.exists(f"wallpapers/{selected_category}"):
			os.makedirs(f"wallpapers/{selected_category}")
		file_path = f"wallpapers/{selected_category}/{filename}"
		if not os.path.exists(file_path):
			with open(file_path,'wb') as file:
				# for chunk in res3.iter_content(chunk_size=2048):
					# file.write(chunk)
				file.write(res3.content)
		# time.sleep(1)
		

	print(f"{selected_category} - Download completed")
	time.sleep(40)

