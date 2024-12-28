# import required modules
from bs4 import BeautifulSoup
import requests

# get URL
page = requests.get("https://en.wikipedia.org/wiki/JCPenney")

# scrape webpage
soup = BeautifulSoup(page.content, 'html.parser')

list(soup.children)

print(page.content)
