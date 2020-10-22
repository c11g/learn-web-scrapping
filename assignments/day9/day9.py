import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

db = {}
app = Flask("DayNine")

# get_news
def get_news(order_by):
  print(f"{order_by} fetching...")
  url =  popular if order_by == "popular" else new  
  data_list = requests.get(url).json().get("hits")
  
  result = []
  for data in data_list:
    result.append({
      "id": data.get("objectID"),
      "title": data.get("title"),
      "url": data.get("url"),
      "points": data.get("points"),
      "author": data.get("author"),
      "num_comments": data.get("num_comments")
    })

  return result

@app.route("/")
def main():
  order_by = request.args.get("order_by") if request.args.get("order_by") else "popular"
  
  key = "new_db" if order_by == "new" else "popular_db"

  if db.get(key):
    news_list = db.get(key)
  else:
    news_list = get_news(order_by)
    db[key] = news_list
  
  return render_template("index.html",
    order_by=order_by,
    news_list=news_list
  )

@app.route("/<id>")
def detail(id):
  url = make_detail_url(id)
  data = requests.get(url).json()
  
  return render_template("detail.html",
    title=data.get("title"),
    author=data.get("author"),
    points=data.get("points"),
    url=data.get("url"),
    children=data.get("children")
  )

app.run(host="0.0.0.0")