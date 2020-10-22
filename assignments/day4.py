import os
import requests
from validator_collection import checkers # validate url

reload = True # False is Quit

def add_http_to_url(url):
  if not url.startswith("http"):
    url = "http://" + url
  return url

while reload:
  print("Welcome to IsItDown.py!")
  print("Please write a URL or URLs you want to check. (seperated by comma)")
  urls = input().split(",")
  
  # remove whitespace and transform to lowercase
  urls = [url.strip().lower() for url in urls]

  for url in urls:
    http_url = add_http_to_url(url)

    if not checkers.is_url(http_url):
      print(f"{url} is not a valid URL.")
      continue

    try:
      res = requests.get(url)
    except:
      print(f"{http_url} is down!")
    else:
      print(f"{http_url} is up!")

  while True:
    print("Do you want to start over? y/n", end=" ")
    answer = input().lower()
    
    if answer == "y":
      os.system('clear')
      break
    elif answer == "n":
      print("Ok. bye!")
      reload = False # Quit
      break
    else:
      print("That's not a valid answer.")