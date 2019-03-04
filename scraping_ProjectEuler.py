# https://projecteuler.net/archives

import requests
from bs4 import BeautifulSoup
from csv import writer

response = requests.get("https://projecteuler.net/archives")
data = BeautifulSoup(response.text, "html.parser")
problems = data.find_all("tr")

with open("project_euler_data.csv", "w") as csv_file:
	csv_writer = writer(csv_file)
	csv_writer.writerow(["ID", "Title","published_on", "Solved_By"])

	for problem in problems:
		a_tag = problem.find("a")
		div = problem.find("div")
		if a_tag == None:
			continue
		title = a_tag.get_text()
		url  = a_tag['href']
		published_on = a_tag['title']
		solved_by = div.get_text()
		csv_writer.writerow([url, title, published_on, solved_by])