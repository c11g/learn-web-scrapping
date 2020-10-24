import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def get_stackoverflow(term):
  print(f"fetching {term} from stackoverflow...")
  url = f"https://stackoverflow.com/jobs?r=true&q={term}"
  result = []
  html = requests.get(url, headers=headers).text
  soup = BeautifulSoup(html, "html.parser")
  items = soup.select(".previewable-results .-job")
  
  for item in items:
    try:
      title = item.select_one("h2 a").get_text()
      href = item.select_one("h2 a").get("href")
      company = item.select_one("h3 > span:first-child").string.split("\r\n")[0]
    except:
      continue
    
    result.append({
      "title": title,
      "href": f"https://stackoverflow.com{href}",
      "company": company
    })

  return result

def get_wwr(term):
  print(f"fetching {term} from wwr...")
  url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
  result = []
  html = requests.get(url, headers=headers).text
  soup = BeautifulSoup(html, "html.parser")
  items = soup.select("#category-2 li")
  
  for item in items:
    try:
      title = item.select_one(".title").get_text()
      href = item.select_one("a").get("href")
      company = item.select_one(".company").get_text()
    except:
      continue
    
    result.append({
      "title": title,
      "href": f"https://weworkremotely.com{href}",
      "company": company
    })

  return result

def get_remote(term):
  print(f"fetching {term} from remoteok...")
  url = f"https://remoteok.io/remote-dev+{term}-jobs"
  result = []
  html = requests.get(url, headers=headers).text
  soup = BeautifulSoup(html, "html.parser")
  items = soup.select("#jobsboard tr.job td:nth-child(2)")
  
  for item in items:
    try:
      title = item.select_one("h2").get_text()
      href = item.select_one("a[itemprop=url]").get("href")
      company = item.select_one("h3").get_text()
    except:
      continue
    
    result.append({
      "title": title,
      "href": f"https://remoteok.io{href}",
      "company": company
    })

  return result