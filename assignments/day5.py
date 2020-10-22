import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"

country_list = []

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
rows = soup.select("tbody > tr")

for i in range(len(rows)):
  name = rows[i].select_one("td:first-child").string
  code = rows[i].select_one("td:nth-child(3)").string

  if code is None: continue
  country_list.append((name, code))

for i in range(len(country_list)):
  print(f"# {i} {country_list[i][0]}")

while True:
  try:
    print("#: ", end="")
    n = int(input())
    print(f"You choose {country_list[n][0]}")
    print(f"The currency code is {country_list[n][1]}")
    break
  except ValueError:
    print("That wasn't a number.")
  except IndexError:
    print("Choose a number from the list.")