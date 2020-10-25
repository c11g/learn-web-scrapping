from flask import Flask, request, render_template, send_file, redirect
from scrapper import get_stackoverflow, get_wwr, get_remote
import csv

"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
app = Flask("Final Assignment")

db = {}

@app.route('/')
def main():
  return render_template('main.html')
    
@app.route('/search')
def search():
  term = request.args.get('term').lower()
  if not term:
    return redirect("/")
  fromDb = db.get(term)
  if fromDb:
    so_list = fromDb
  else:
    so_list = get_stackoverflow(term)
    wwr_list = get_wwr(term)
    remote_list = get_remote(term)
    db[term] = so_list+wwr_list+remote_list

  return render_template('search.html',
    term=term,
    result=db[term],
    count=len(db[term])
  )

@app.route('/export')
def export():
  term = request.args.get('term').lower()
  fromDb = db.get(term)

  if not fromDb:
    return redirect("/")
  
  with open(f"{term}.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["TITLE", "COMPANY", "LINK"])

    for row in fromDb:
      writer.writerow([
        row.get("title"),
        row.get("company"),
        row.get("href")
      ])

  return send_file(
    f"{term}.csv",
    mimetype="application/x-csv",
    attachment_filename= f"{term}.csv",
    as_attachment=True
  )
  
app.run(host="0.0.0.0")