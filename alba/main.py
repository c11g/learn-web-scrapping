import os
import unicodedata
import math
import time
import csv
import requests
from bs4 import BeautifulSoup

def get_brand(url):
  result = []
  r = requests.get(url)
  soup = BeautifulSoup(r.text, "html.parser")
  li = soup.select("#MainSuperBrand .impact")

  for soup in li:
    name = soup.select_one(".company").string
    url = soup.select_one(".goodsBox-info").get("href")
    result.append((name,url))
  return result

def get_last_page(url, max_page):  
  url = f"{url}?pagesize=50"
  r = requests.get(url)
  soup = BeautifulSoup(r.text, "html.parser")

  total = 0
  if soup.select_one(".jobCount strong"):
    total = soup.select_one(".jobCount strong").string.replace(",", "")
  else:
    total = soup.select_one(".listCount strong").string.replace(",", "")

  last_page = math.ceil(int(total) / 50)
  return max_page if last_page >= max_page else last_page

# place, title, time, pay, date
def get_jobs(url, last_page):
  result = []
  places = []
  titles = []
  times = []
  pays = []
  dates = []

  for i in range(last_page):
    print(f"{i+1}/{last_page} scrapping...")
    url = f"{url}job/brand/" if url.endswith("co.kr/") else url
    
    r = requests.get(f"{url}?page={i+1}")
    soup = BeautifulSoup(r.text, "html.parser")
    tbody = soup.select_one("#NormalInfo tbody")
    
    places += tbody.select("td.local")
    titles += tbody.select("td.title .company")
    times += tbody.select("td.data")
    pays += tbody.select("td.pay")
    dates += tbody.select("td.regDate")

  for i in range(len(places)):
    try:
      result.append([
        unicodedata.normalize("NFKD", places[i].get_text()),
        titles[i].get_text(),
        times[i].get_text(),
        pays[i].get_text(),
        dates[i].get_text()
      ])
    except:
      print(f"Error: {titles[i]}")

  return result
  
start = time.time()

os.system("clear")
alba_url = "http://www.alba.co.kr"

brands = get_brand(alba_url)

brands_job = []
max_page = 5

for i in range(len(brands)):
  url = brands[i][1]
  print(f"[{i+1}/{len(brands)}] {url} ...")
  last_page = get_last_page(url, max_page)
  print(f"last_page is {last_page}")
  if last_page == 0: continue
  jobs = get_jobs(url, last_page)

  name = brands[i][0]
  brands_job.append((name, jobs))

# write csv files
for i in range(len(brands_job)):
  try:
    print(f"Writing {brands_job[i][0]}.csv")
    with open(f"{brands_job[i][0]}.csv", "w") as file:
      writer = csv.writer(file)
      writer.writerow(["place", "title", "time", "pay", "date"])
      
      for row in brands_job[i][1]:
        writer.writerow(row)
  except:
    print(f"Error: Writing {brands_job[i][0]}.csv")
    continue

# time
print(f"소요 시간: {time.time() - start} 초")