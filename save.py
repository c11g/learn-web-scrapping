import csv

def save_to_csv(list):
  print("Writing to result.csv")
  with open("result.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["title", "date", "link"])
    for row in list:
      writer.writerow(row.values())