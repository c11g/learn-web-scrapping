import os
from babel.numbers import format_currency
from scrape_iban import get_country_and_currency
from scrape_transfer_wise import get_exchage_rate

# Display list
os.system("clear")
country_list = get_country_and_currency()

for i in range(len(country_list)):
  print(f"# {i} {country_list[i][0]}")

# Get two countries
country_pair = []
print("\nWhere are you from? Choose a country number.")

def ask_country():
  try:
    n = int(input("\n#: "))
    print(country_list[n][0])
    country_pair.append(country_list[n])
  except ValueError:
    print("That wasn't a number.")
    ask_country()
  except IndexError:
    print("Choose a number from the list.")
    ask_country()

while True:
  ask_country()
  if len(country_pair) >= 2: break
  print("\nNow choose another country.")

country_a, country_b = country_pair

# Get Amount
def ask_amount():
  try:
    print(f"\nHow many {country_a[1]} do you want convert {country_b[1]}?")
    return int(input())
  except:
    print("That wasn't a number.")
    ask_amount()

amount = ask_amount()

# Scrape TransferWise
try:
  rate = get_exchage_rate(country_a[1], country_b[1])
  
  print(f"{format_currency(amount, country_a[1])} is {format_currency(rate*amount, country_b[1])}")
except:
  print("Do not support currency code")
