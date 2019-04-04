import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader

BASE_URL = "http://quotes.toscrape.com"

def read_quotes(filename):
	with open(filename, "r") as file:
		csv_reader = DictReader(file)
		return list(csv_reader)

def start_game(quotes):
	quote = choice(quotes)
	remaining_guesses = 4
	print("Here's a quote: ")
	print(quote["text"])
	#print(quote["author_name"])
	guess = ""
	while guess.lower() != quote["author_name"].lower() and remaining_guesses >0 :
		guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses}\n")
		if guess.lower() == quote['author_name'].lower():
			print("You got it RIGHT!")
			break
		remaining_guesses -= 1
		if remaining_guesses == 3:
			res = requests.get(f"{BASE_URL}{quote['bio_link']}")
			data = BeautifulSoup(res.text, "html.parser")
			birth_date = data.find(class_="author-born-date").get_text()
			birth_place = data.find(class_="author-born-location").get_text()
			print(f"Here's a hint: The Author was born on {birth_date} {birth_place}")
		elif remaining_guesses == 2:
			print(f"Here's a hint: The author's first name starts with: {quote['author_name'][0]}")
		elif remaining_guesses == 1:
			last = quote["author_name"].split(" ")[1][0]
			print(f"Here's a hint: The author's last name starts with: {last}")
		else:
			print(f"You ran out of guesses. Better luck next time. The answer was {quote['author_name']}")

	again = ""
	while again.lower() not in ('y', 'yes', 'n', 'no'):
		again = input("Would you like to play again (y/n)?")

	if again.lower() in ('yes', 'y'):
		return start_game(quotes)
	else:
		print("OK, GoodBye")
quotes = read_quotes("quotes.csv")
start_game(quotes)